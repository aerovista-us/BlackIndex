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

    def test_ensure_after_is_idempotent(self):
        anchor = "anchor"
        line = "result"
        self.assertEqual(mod.ensure_after(f"{anchor}\n{line}", anchor, line), f"{anchor}\n{line}")
        self.assertEqual(mod.ensure_after(anchor, anchor, line), f"{anchor}\n{line}")

    def test_ensure_after_fails_safe_without_anchor(self):
        with self.assertRaises(RuntimeError):
            mod.ensure_after("different", "anchor", "line")

    def test_current_review007_outcomes_are_encoded(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn("CAND-0005 / CAND-0013 bracketed pending visual confirmation", text)
        self.assertIn("Benomrane exact scan 138-210 found no strong boundary signals", text)
        self.assertIn("2007 executive-summary vs 2015 full-report release distinction clarified", text)
        self.assertIn("search/index text is navigation-only", text)
        self.assertIn("boundary recovery is on HOLD", text)

    def test_reconciler_does_not_reference_evidence_object_paths(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("objects/", text)
        self.assertIn("BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md", text)


if __name__ == "__main__":
    unittest.main()
