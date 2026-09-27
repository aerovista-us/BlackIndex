import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-looking-glass-dod-fy1966.sh"


class LookingGlassDodFY1966Tests(unittest.TestCase):
    def test_sprint_is_one_official_govinfo_record(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertEqual(text.count('"$INGEST"'), 1)
        self.assertIn("www.govinfo.gov/content/pkg/GOVPUB-D-ed021da2d13644089b28ae2bdeffefd8", text)
        self.assertIn('--source "DOD"', text)
        self.assertNotIn("--document-date", text)
        self.assertIn('--publish', text)

    def test_source_limits_are_explicit(self):
        text = SCRIPT.read_text(encoding="utf-8").lower()
        self.assertIn("not an emergency war order", text)
        self.assertIn("nuclear-use authorization", text)
        self.assertIn("complete ewo/siop authority chain", text)
        self.assertNotIn("tesseract", text)
        self.assertNotIn("ocrmypdf", text)
        self.assertNotIn("promote-candidate", text)


if __name__ == "__main__":
    unittest.main()
