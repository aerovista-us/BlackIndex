import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate-evidence-objects.py"
LINEAGE = ROOT / "tools/source-lineage.py"
AUDIT = ROOT / "tools/dependency-audit.py"
LINEAGE_UI = ROOT / "tools/source-lineage-ui.py"
WORK_QUEUE_UI = ROOT / "tools/work-queue-ui.py"
SCHEMA = ROOT / "objects/schema-v1.json"


class EvidenceObjectTests(unittest.TestCase):
    def make_root(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "metadata").mkdir()
        (root / "extractions").mkdir()
        for d in [
            "record_integrity", "missing_evidence", "version_families",
            "version_comparisons", "source_dependencies", "statement_comparisons",
            "investigator_reviews",
        ]:
            (root / "objects" / d).mkdir(parents=True, exist_ok=True)
        (root / "objects/schema-v1.json").write_text(SCHEMA.read_text(encoding="utf-8"), encoding="utf-8")
        return td, root

    def add_doc(self, root, doc_id, **extra):
        payload = {
            "schema_version": 1, "doc_id": doc_id, "title": doc_id,
            "source": "FBI", "collection": "Test", "sha256": "0" * 64,
        }
        payload.update(extra)
        (root / "metadata" / f"{doc_id}.json").write_text(json.dumps(payload), encoding="utf-8")

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

    def test_dependency_audit_reports_reference_without_asserting_dependency(self):
        td, root = self.make_root()
        try:
            a = "FBI-2021-alpha-001"
            b = "FBI-2021-beta-001"
            self.add_doc(root, a, related_documents=[b])
            self.add_doc(root, b)
            (root / "extractions" / f"{a}.md").write_text(f"Related record: {b}\n", encoding="utf-8")
            p = subprocess.run([sys.executable, str(AUDIT), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads((root / "local/index/dependency-audit.json").read_text(encoding="utf-8"))
            self.assertEqual(data["candidate_count"], 1)
            self.assertEqual(data["candidates"][0]["status"], "REVIEW_REQUIRED")
            self.assertIn("not yet a source-dependency assertion", data["candidates"][0]["note"])
        finally:
            td.cleanup()

    def test_lineage_ui_renders_compiled_edges(self):
        td, root = self.make_root()
        try:
            obj = {
                "schema_version": 1, "object_type": "source_dependency", "object_id": "SD-1",
                "assertion_id": "claim-1", "source_id": "Report-A",
                "depends_on": "Underlying-1", "dependency_type": "summary-derived-from",
                "independence": "dependent",
            }
            (root / "objects/source_dependencies/SD-1.json").write_text(json.dumps(obj), encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, str(LINEAGE), "--root", str(root)]).returncode, 0)
            p = subprocess.run([sys.executable, str(LINEAGE_UI), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            page = (root / "local/dashboard/source-lineage.html").read_text(encoding="utf-8")
            self.assertIn("Report-A", page)
            self.assertIn("Underlying-1", page)
            self.assertIn("Missing edges mean", page)
        finally:
            td.cleanup()

    def test_work_queue_renders_unresolved_states_without_promoting_them(self):
        td, root = self.make_root()
        try:
            doc_id = "FBI-2021-queue-001"
            self.add_doc(root, doc_id, title="Queue Test Record", evidence_status="unreviewed")
            missing = {
                "schema_version": 1, "object_type": "missing_evidence", "object_id": "ME-QUEUE-1",
                "doc_id": doc_id, "category": "UNMAPPED_REFERENCED_EVIDENCE",
                "summary": "Referenced attachment not yet mapped", "status": "unresolved",
            }
            (root / "objects/missing_evidence/ME-QUEUE-1.json").write_text(json.dumps(missing), encoding="utf-8")
            (root / "local/index").mkdir(parents=True)
            (root / "local/index/research-reference-audit.json").write_text(json.dumps({
                "pairs": [{
                    "doc_a": doc_id, "doc_b": "FBI-2021-other-001", "cooccurrence_files": 1,
                    "files": ["docs/reviews/example.md"], "status": "REVIEW_REQUIRED"
                }]
            }), encoding="utf-8")
            (root / "local/review/911-fbi-p0").mkdir(parents=True)
            (root / "local/review/911-fbi-p0/manifest.json").write_text(json.dumps({
                "count": 2,
                "packets": [
                    {"container_doc_id": "FBI-2022-parent-001", "candidate_id": "CAND-0001"},
                    {"container_doc_id": "FBI-2022-parent-001", "candidate_id": "CAND-0002"},
                ]
            }), encoding="utf-8")
            (root / "local/review/911-fbi-p0/review-ledger.json").write_text(json.dumps({
                "reviews": [{
                    "container_doc_id": "FBI-2022-parent-001", "candidate_id": "CAND-0001",
                    "disposition": "HOLD", "confirmed_pages": None, "note": "Needs source review"
                }]
            }), encoding="utf-8")
            p = subprocess.run([sys.executable, str(WORK_QUEUE_UI), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            summary = json.loads(p.stdout)
            self.assertEqual(summary["unreviewed"], 1)
            self.assertEqual(summary["missing_evidence"], 1)
            self.assertEqual(summary["lineage_pairs"], 1)
            self.assertEqual(summary["fbi_p0"], 2)
            self.assertEqual(summary["fbi_pending"], 1)
            page = (root / "local/dashboard/work-queue.html").read_text(encoding="utf-8")
            self.assertIn("Queue Test Record", page)
            self.assertIn("Referenced attachment not yet mapped", page)
            self.assertIn("REVIEW REQUIRED", page)
            self.assertIn("HOLD", page)
            self.assertIn("process labels, not historical conclusions", page)
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()
