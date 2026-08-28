from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "review-007-boundary-followup.py"


def load_module():
    spec = importlib.util.spec_from_file_location("review007_followup", MODULE_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Review007BoundaryFollowupTests(unittest.TestCase):
    def test_bracketed_candidate_is_still_unconfirmed(self):
        mod = load_module()
        payload = {
            "targets": [
                {
                    "target_id": "CAND-X",
                    "kind": "heuristic_candidate_review",
                    "parent_doc_id": "FBI-X",
                    "parent_sha256": "abc",
                    "proposed_start": 10,
                    "proposed_end": 12,
                    "all_diagnostic_pages_exact": True,
                    "transition": {
                        "start_record_signal": True,
                        "extends_left_signal": False,
                        "extends_right_signal": False,
                    },
                    "diagnostic_pages": [
                        {"physical_page": 10, "role": "candidate", "fbi_header": True, "case_or_file_label": True},
                        {"physical_page": 11, "role": "candidate", "fbi_header": False, "case_or_file_label": False},
                        {"physical_page": 12, "role": "candidate", "fbi_header": False, "case_or_file_label": False},
                        {"physical_page": 13, "role": "after", "fbi_header": True, "case_or_file_label": True},
                    ],
                }
            ]
        }
        rows = mod.candidate_boundary_hypotheses(payload)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["hypothesis_status"], "BRACKETED_BY_NEXT_RECORD_START_PENDING_VISUAL_CONFIRMATION")
        self.assertFalse(row["boundary_confirmed"])
        self.assertTrue(row["visual_confirmation_required"])
        self.assertFalse(row["record_promoted"])

    def test_no_next_record_signal_stays_unresolved(self):
        mod = load_module()
        payload = {
            "targets": [
                {
                    "target_id": "CAND-X",
                    "kind": "heuristic_candidate_review",
                    "all_diagnostic_pages_exact": True,
                    "transition": {
                        "start_record_signal": True,
                        "extends_left_signal": False,
                        "extends_right_signal": False,
                    },
                    "diagnostic_pages": [
                        {"physical_page": 10, "role": "candidate"},
                        {"physical_page": 11, "role": "after", "fbi_header": False, "case_or_file_label": False},
                    ],
                }
            ]
        }
        rows = mod.candidate_boundary_hypotheses(payload)
        self.assertEqual(rows[0]["hypothesis_status"], "UNRESOLVED_BOUNDARY_HYPOTHESIS")
        self.assertFalse(rows[0]["boundary_confirmed"])

    def test_strong_start_requires_structural_signal(self):
        mod = load_module()
        row = mod.structural_features(
            "FEDERAL BUREAU OF INVESTIGATION\nFILE NO. 123\n",
            "FEDERAL BUREAU OF INVESTIGATION\nFILE NO. 123\n",
            5,
        )
        self.assertTrue(row["exact_same_index"])
        self.assertTrue(row["strong_record_start_signal"])

        weak = mod.structural_features("INTERVIEW OF SOMEONE\n", "INTERVIEW OF SOMEONE\n", 6)
        self.assertTrue(weak["weak_record_start_signal"])
        self.assertFalse(weak["strong_record_start_signal"])

    def test_tool_declares_no_promotion_or_boundary_claims(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn('"contains_text_previews": False', source)
        self.assertIn('"boundary_claims": False', source)
        self.assertIn('"record_promotions": 0', source)
        self.assertIn('"proposed_range_is_boundary_claim": False', source)
        self.assertIn('"visual_confirmation_required": True', source)


if __name__ == "__main__":
    unittest.main()
