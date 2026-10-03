import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/evidence_map.py"
VALIDATOR = ROOT / "tools/validate-evidence-objects.py"
DISCOVERY_UI = ROOT / "tools/discovery-ui.py"
CAPABILITY_UI = ROOT / "tools/capability-registry-ui.py"
SCHEMA = ROOT / "objects/schema-v1.json"


class DiscoveryCapabilityTests(unittest.TestCase):
    def make_root(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "metadata").mkdir()
        (root / "objects").mkdir()
        (root / "objects/schema-v1.json").write_text(SCHEMA.read_text(), encoding="utf-8")
        return td, root

    def add_doc(self, root, doc_id="DOD-2026-test-001"):
        payload = {"schema_version": 1, "doc_id": doc_id, "title": "Test", "source": "DOD", "collection": "Test", "sha256": "0" * 64}
        (root / "metadata" / f"{doc_id}.json").write_text(json.dumps(payload), encoding="utf-8")
        return doc_id


    def test_cli_creates_discovery_and_validator_accepts_it(self):
        td, root = self.make_root()
        try:
            doc = self.add_doc(root)
            p = subprocess.run([
                sys.executable, str(CLI), "--root", str(root), "discovery",
                "--title", "Candidate source", "--summary", "Needs follow-up",
                "--type", "source", "--linked-doc-id", doc,
                "--source-ref", "https://example.test/source",
                "--evidence-boundary", "Lead only; no claim promoted."
            ], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            obj = json.loads(next((root / "objects/discoveries").glob("*.json")).read_text())
            self.assertEqual(obj["status"], "new")
            self.assertEqual(obj["linked_doc_ids"], [doc])
            v = subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(v.returncode, 0, v.stdout + v.stderr)
        finally:
            td.cleanup()

    def test_capability_never_infers_event_use(self):
        td, root = self.make_root()
        try:
            doc = self.add_doc(root)
            p = subprocess.run([
                sys.executable, str(CLI), "--root", str(root), "capability",
                "--name", "Remote sensor access", "--holder", "Example Org",
                "--holder-type", "organization", "--domain", "camera-iot",
                "--description", "Documented ability to access supported sensor systems.",
                "--status", "documented", "--observed-at", "2026-01-01",
                "--time-scope-note", "Observed in the cited 2026 source.",
                "--source-ref", doc, "--linked-doc-id", doc,
                "--limitation", "Does not establish use in any event."
            ], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            obj = json.loads(next((root / "objects/capabilities").glob("*.json")).read_text())
            self.assertIs(obj["use_in_event_inferred"], False)

            v = subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(v.returncode, 0, v.stdout + v.stderr)
            obj["use_in_event_inferred"] = True
            target = next((root / "objects/capabilities").glob("*.json"))
            target.write_text(json.dumps(obj), encoding="utf-8")
            v = subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(v.returncode, 1)
            self.assertIn("must remain false", v.stdout)
        finally:
            td.cleanup()

    def test_local_uis_render_safety_boundaries(self):
        td, root = self.make_root()
        try:
            (root / "objects/discoveries").mkdir(parents=True)
            (root / "objects/capabilities").mkdir(parents=True)
            disc = {"schema_version": 1, "object_type": "discovery", "object_id": "DISC-1", "title": "Lead", "summary": "Follow up", "discovery_type": "lead", "discovered_at": "2026-01-01", "status": "new", "source_refs": [], "linked_doc_ids": [], "linked_object_ids": [], "evidence_boundary": "Not evidence yet."}
            cap = {"schema_version": 1, "object_type": "capability", "object_id": "CAP-1", "capability_name": "Capability", "holder": "Example Org", "holder_type": "organization", "domain": ["camera-iot"], "description": "Example", "capability_status": "documented", "observed_at": "2026-01-01", "valid_from": None, "valid_to": None, "time_scope_note": "Observed in 2026.", "source_refs": ["source"], "linked_doc_ids": [], "linked_object_ids": [], "limitations": [], "use_in_event_inferred": False}
            (root / "objects/discoveries/DISC-1.json").write_text(json.dumps(disc), encoding="utf-8")
            (root / "objects/capabilities/CAP-1.json").write_text(json.dumps(cap), encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, str(DISCOVERY_UI), "--root", str(root)]).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, str(CAPABILITY_UI), "--root", str(root)]).returncode, 0)
            discovery_page = (root / "local/dashboard/discovery-inbox.html").read_text()
            capability_page = (root / "local/dashboard/capability-registry.html").read_text()
            self.assertIn("does not promote a claim to evidence or fact", discovery_page)
            self.assertIn("Capability ≠ use.", capability_page)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
