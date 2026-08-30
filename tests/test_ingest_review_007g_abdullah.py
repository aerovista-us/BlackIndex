import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-review-007g-abdullah-official-fbi-bundles.sh"


class Review007GAbdullahIngestTests(unittest.TestCase):
    def test_sprint_is_exactly_two_official_fbi_parent_bundles(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("9-11-investigation-2002-04-apr", text)
        self.assertIn("9-11-investigation-2004-05-may", text)
        self.assertEqual(text.count('run_one "FBI 9/11 Investigation'), 2)
        self.assertEqual(text.count('--source "FBI"'), 2)
        self.assertNotIn("cia.gov", text.lower())
        self.assertNotIn("govinfo.gov", text.lower())

    def test_sprint_does_not_promote_children_or_run_ocr(self):
        text = SCRIPT.read_text(encoding="utf-8").lower()
        self.assertNotIn("tesseract", text)
        self.assertNotIn("ocrmypdf", text)
        self.assertNotIn("promote-candidate", text)
        self.assertNotIn("--apply", text)

    def test_ledger_reconciliation_is_after_durable_report_publication(self):
        text = SCRIPT.read_text(encoding="utf-8")
        published = text.index("Published sanitized Review 007G run report.")
        reconciler = text.index("reconcile-review-007-ledger.py")
        self.assertGreater(reconciler, published)
        self.assertIn("The acquired records, verifier result, and durable run report remain valid.", text)
        self.assertIn("Only corpus verification governs the sprint exit status", text)

    def test_report_preserves_unresolved_exact_records(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("July 23, 2002", text)
        self.assertIn("May 19, 2004", text)
        self.assertIn("May 17 and May 18, 2004", text)
        self.assertIn("duplicate-release/source-dependency", text)

    def test_run_report_is_sanitized(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Contains normalized-text previews:** `false`", text)
        self.assertIn("Child-record promotions:** `0`", text)
        self.assertIn("Evidence-state mutations:** `none`", text)


if __name__ == "__main__":
    unittest.main()
