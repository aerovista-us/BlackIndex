import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "run-review-007-physical-page-map.sh"


class Review007PhysicalPageCheckpointTests(unittest.TestCase):
    def test_checkpoint_is_read_only_and_sanitized(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("map-review-007-physical-pages.py", text)
        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn("No evidence-state mutation or record promotion", text)
        self.assertIn("contains_text_previews", text)
        self.assertNotIn("evidence_map.py", text)
        self.assertNotIn("qpdf", text)
        self.assertNotIn("pdfseparate", text)

    def test_report_preserves_boundary_guard(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("does not itself establish the start/end boundary", text)
        self.assertIn("OCR used", text)
        self.assertIn("Fuzzy matching used", text)


if __name__ == "__main__":
    unittest.main()
