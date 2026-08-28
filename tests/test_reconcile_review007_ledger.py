import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "reconcile-review-007-ledger.py"
spec = importlib.util.spec_from_file_location("reconcile_review_007_ledger", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Review007LedgerReconcilerTests(unittest.TestCase):
    def test_replace_once_is_idempotent_when_new_value_present(self):
        old = "| Physical PDF page mapper | `QUEUED` | required |"
        new = "| Physical PDF page mapper | `COMPLETE` | verified |"
        self.assertEqual(mod.replace_once(new, old, new), new)

    def test_replace_once_updates_expected_marker(self):
        old = "| Physical PDF page mapper | `QUEUED` | required |"
        new = "| Physical PDF page mapper | `COMPLETE` | verified |"
        self.assertEqual(mod.replace_once(old, old, new), new)

    def test_replace_once_fails_safe_if_marker_missing(self):
        with self.assertRaises(RuntimeError):
            mod.replace_once("different text", "missing", "new")

    def test_reconciler_does_not_reference_evidence_object_paths(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("objects/", text)
        self.assertIn("BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md", text)


if __name__ == "__main__":
    unittest.main()
