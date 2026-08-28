import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "build-fbi-source-review-bundle.py"


class FBISourceBundlePageGuardTests(unittest.TestCase):
    def test_heuristic_pdf_slicing_fails_closed_by_default(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("--legacy-unsafe-heuristic-pages", text)
        self.assertIn("refusing heuristic text-page -> physical-PDF slicing", text)
        self.assertIn("run the physical-page verification workflow first", text)


if __name__ == "__main__":
    unittest.main()
