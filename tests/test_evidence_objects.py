import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate-evidence-objects.py"
LINEAGE = ROOT / "tools/source-lineage.py"
SCHEMA = ROOT / "objects/schema-v1.json"


class EvidenceObjectTests(unittest.TestCase):
    def make_root(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "metadata").mkdir()
        for d in [
            "record_integrity", "missing_evidence", "version_families",
            "version_comparisons", "source_dependencies", "statement_comparisons",
            "investigator_reviews",
        ]:
            (root / "objects" / d).mkdir(parents=True, exist_ok=True)
        (root / "objects/schema-v1.json").write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")
        return td, root

    def add_doc(self, root, doc_id):
        (root / "metadata" / f"{doc_id}.json").write_text(json.dumps({
            "schema_version": 1, "doc_id": doc_id, "title": doc_id,
            "source": "FBI", "collection": "Test", "sha256": "0" * 64,
        }), encoding="utf-8")

    def test_validator_accepts_minimal_integrity_object(self):
        td, root = self.make_root()
        try:
            self.add_doc(root, "FBI-2021-test-001")
            obj = {
                "schema_version": 1, "object_type": "record_integrity",
                "object_id": "RI-FBI-2021-test-001", "doc_id": "FBI-2021-test-001",
                "completeness": None, "redaction_concern": None,
                "known_destruction": "unknown", "missing_referenced_records": [],
                "archive_confidence": None,
            }
            (root / "objects/record_integrity/FBI-2021-test-001.json").write_text(json.dumps(obj), encoding="utf-8")
            p = subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertTrue(json.loads(p.stdout)["ok"])
        finally:
            td.cleanup()

    def test_validator_rejects_investigator_conclusion_as_fact(self):
        td, root = self.make_root()
        try:
            obj = {
                "schema_version": 1, "object_type": "investigator_review", "object_id": "IR-1",
                "report_or_finding": "finding", "investigator": "office", "exact_wording": "none found",
                "scope": "test", "conclusion_adopted_as_fact": True,
            }
            (root / "objects/investigator_reviews/IR-1.json").write_text(json.dumps(obj), encoding="utf-8")
            p = subprocess.run([sys.executable, str(VALIDATOR), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 1)
            self.assertIn("must remain false", p.stdout)
        finally:
            td.cleanup()

    def test_lineage_groups_shared_upstream_source(self):
        td, root = self.make_root()
        try:
            for source in ("Report-A", "Report-B"):
                obj = {
                    "schema_version": 1, "object_type": "source_dependency", "object_id": f"SD-{source}",
                    "assertion_id": "claim-1", "source_id": source,
                    "depends_on": "Underlying-Interview-1", "dependency_type": "summary-derived-from",
                    "independence": "dependent",
                }
                (root / "objects/source_dependencies" / f"{source}.json").write_text(json.dumps(obj), encoding="utf-8")
            p = subprocess.run([sys.executable, str(LINEAGE), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads((root / "local/index/source-lineage.json").read_text(encoding="utf-8"))
            self.assertEqual(len(data["shared_lineage_families"]), 1)
            self.assertEqual(data["shared_lineage_families"][0]["member_count"], 2)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
