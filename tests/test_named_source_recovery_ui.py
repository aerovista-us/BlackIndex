import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "named-source-recovery-ui.py"
spec = importlib.util.spec_from_file_location("named_source_recovery_ui", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class NamedSourceRecoveryUITests(unittest.TestCase):
    def test_source_contains_safety_labels_and_local_route(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn("Candidate recovery only", text)
        self.assertIn("not verified physical PDF page numbers", text)
        self.assertIn("named-source-recovery.html", text)
        self.assertIn("/blackindex-dashboard.html", text)
        self.assertNotIn("https://", text)

    def test_scan_absent_is_safe_empty_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Exercise the same report-loading contract used by the page.
            report = mod.load(root / "local/index/911-named-source-recovery.json", None)
            self.assertIsNone(report)

    def test_candidate_contract_is_renderable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "local/index/911-named-source-recovery.json"
            path.parent.mkdir(parents=True)
            payload = {
                "generated_at": "2026-08-27T00:00:00+00:00",
                "target_count": 1,
                "targets_with_candidates": 1,
                "scanned_documents": 1,
                "scanned_text_pages": 2,
                "targets": [{
                    "target_id": "T1",
                    "label": "Named record",
                    "candidate_count": 1,
                    "candidates": [{
                        "doc_id": "FBI-TEST-001",
                        "source": "FBI",
                        "text_page_index": 2,
                        "physical_page_index": None,
                        "physical_page_verified": False,
                        "matched": ["name", "date"],
                        "preview": "candidate context",
                    }],
                }],
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            loaded = mod.load(path, None)
            self.assertEqual(loaded["targets"][0]["candidates"][0]["physical_page_index"], None)


if __name__ == "__main__":
    unittest.main()
