import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "review-007-boundary-diagnostic.py"
spec = importlib.util.spec_from_file_location("review_007_boundary_diagnostic", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Review007BoundaryDiagnosticTests(unittest.TestCase):
    def test_source_is_review_only_and_text_free(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn("contains_text_previews", text)
        self.assertIn("boundary_claims", text)
        self.assertIn("record_promotions", text)
        self.assertNotIn("record_promoted\": True", text)

    def test_self_contained_requires_both_boundary_signals(self):
        transition = {
            "extends_left_signal": False,
            "extends_right_signal": False,
            "left_boundary_signal": True,
            "right_boundary_signal": True,
        }
        self.assertEqual(
            mod.disposition("heuristic_candidate_review", transition, True),
            "STRUCTURALLY_SELF_CONTAINED_CANDIDATE",
        )

    def test_extension_signal_blocks_self_contained(self):
        transition = {
            "extends_left_signal": False,
            "extends_right_signal": True,
            "left_boundary_signal": True,
            "right_boundary_signal": True,
        }
        self.assertEqual(
            mod.disposition("heuristic_candidate_review", transition, True),
            "LIKELY_EXTENDS_OUTSIDE_PROPOSED_RANGE",
        )

    def test_gap_window_never_becomes_self_contained(self):
        transition = {
            "extends_left_signal": False,
            "extends_right_signal": False,
            "left_boundary_signal": True,
            "right_boundary_signal": True,
        }
        self.assertEqual(
            mod.disposition("segmentation_gap_diagnostic", transition, True),
            "SEGMENTATION_GAP_WINDOW_REVIEW",
        )

    def test_unresolved_mapping_wins(self):
        transition = {
            "extends_left_signal": False,
            "extends_right_signal": False,
            "left_boundary_signal": True,
            "right_boundary_signal": True,
        }
        self.assertEqual(
            mod.disposition("heuristic_candidate_review", transition, False),
            "UNRESOLVED_PAGE_MAPPING",
        )


if __name__ == "__main__":
    unittest.main()
