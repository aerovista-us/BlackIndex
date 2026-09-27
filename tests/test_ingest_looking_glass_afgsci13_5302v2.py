import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-looking-glass-afgsci13-5302v2.sh"


class LookingGlassAfgsciIngestTests(unittest.TestCase):
    def test_ingest_is_bounded_to_official_afgsc_directive(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("static.e-publishing.af.mil", text)
        self.assertIn('AFGSCI13-5302V2', text)
        self.assertIn('--source "USAF"', text)
        self.assertIn('--document-date "2017-07-19"', text)
        self.assertIn('--publish', text)
        self.assertEqual(text.count('"$INGEST" "$URL"'), 1)

    def test_ingest_does_not_promote_or_ocr(self):
        text = SCRIPT.read_text(encoding="utf-8").lower()
        self.assertNotIn("tesseract", text)
        self.assertNotIn("ocrmypdf", text)
        self.assertNotIn("canonical_status", text)
        self.assertNotIn("promote", text)


if __name__ == "__main__":
    unittest.main()
