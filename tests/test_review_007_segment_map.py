import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "run-review-007-segment-map.sh"


class Review007SegmentMapTests(unittest.TestCase):
    def test_checkpoint_is_review_only_and_sanitized(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("recover-911-named-sources.py", text)
        self.assertIn("map-911-recovery-to-segments.py", text)
        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn('"evidence_state_mutated": False', text)
        self.assertIn('"record_promotion_performed": False', text)
        self.assertIn('"physical_page_claim": False', text)
        self.assertIn('"boundary_claim": False', text)
        self.assertIn("contains_raw_previews", text)
        self.assertNotIn("promote-911", text)
        self.assertNotIn("evidence_map.py", text)

    def test_only_sanitized_report_is_staged(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("git -C \"$ROOT\" add -- \"$REPORT\"", text)
        self.assertIn("PRESTAGED", text)
        self.assertNotIn("git -C \"$ROOT\" add -A", text)
        self.assertNotIn("git -C \"$ROOT\" add .", text)

    def test_report_preserves_boundary_and_page_warnings(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Physical page: `UNVERIFIED`", text)
        self.assertIn("Boundary verified: `false`", text)
        self.assertIn("Review the original parent PDF before promotion", text)


if __name__ == "__main__":
    unittest.main()
