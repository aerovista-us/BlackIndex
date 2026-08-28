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

    def test_replace_row_updates_advanced_status_by_identity(self):
        text = "| Review 007 boundary diagnostic | `COMPLETE` | older wording |\n"
        new = "| Review 007 boundary diagnostic | `COMPLETE` | canonical wording |"
        result = mod.replace_row(text, "| Review 007 boundary diagnostic |", new)
        self.assertEqual(result, new + "\n")

    def test_replace_row_rejects_duplicate_identity(self):
        text = "| A | `ACTIVE` | one |\n| A | `COMPLETE` | two |\n"
        with self.assertRaises(RuntimeError):
            mod.replace_row(text, "| A |", "| A | `COMPLETE` | canonical |")

    def test_ensure_after_is_idempotent(self):
        anchor = "anchor"
        line = "result"
        self.assertEqual(mod.ensure_after(f"{anchor}\n{line}", anchor, line), f"{anchor}\n{line}")
        self.assertEqual(mod.ensure_after(anchor, anchor, line), f"{anchor}\n{line}")

    def test_ensure_after_fails_safe_without_anchor(self):
        with self.assertRaises(RuntimeError):
            mod.ensure_after("different", "anchor", "line")

    def test_ensure_row_after_does_not_duplicate_advanced_status(self):
        anchor = "| prior row | `COMPLETE` | x |"
        existing = "| Review 007 boundary diagnostic | `COMPLETE` | already advanced |"
        prepared = "| Review 007 boundary diagnostic | `PREPARED` | stale |"
        text = f"{anchor}\n{existing}"
        result = mod.ensure_row_after(text, anchor, "| Review 007 boundary diagnostic |", prepared)
        self.assertEqual(result, text)
        self.assertNotIn(prepared, result)

    def test_prefixed_line_update(self):
        text = "- Authoritative local verifier checkpoint: **36 checked / 0 failures**\n"
        updated = mod.replace_prefixed_line(
            text,
            "- Authoritative local verifier checkpoint:",
            "- Authoritative local verifier checkpoint: **37 checked / 0 failures**",
        )
        self.assertIn("37 checked / 0 failures", updated)

    def test_current_review007_outcomes_are_encoded(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn("CAND-0005 / CAND-0013 bracketed pending visual confirmation", text)
        self.assertIn("Benomrane exact scan 138-210 found no strong boundary signals", text)
        self.assertIn("official GPO/FDLP Executive Summary acquired", text)
        self.assertIn("search/index text remains navigation-only", text)
        self.assertIn("boundary recovery is on HOLD", text)

    def test_reconciler_does_not_reference_evidence_object_paths(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("objects/", text)
        self.assertIn("BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md", text)


if __name__ == "__main__":
    unittest.main()
