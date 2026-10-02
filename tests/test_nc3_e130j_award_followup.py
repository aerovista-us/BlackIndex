import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Nc3E130jAwardFollowupTests(unittest.TestCase):
    def test_award_records_and_classifications(self):
        dod = load("metadata/DOD-2024-contract-announcements-001.json")
        navy = load("metadata/US_NAVY-2024-press-releases-001.json")
        self.assertEqual(dod["document_date"], "2024-12-18")
        self.assertEqual(navy["document_date"], "2024-12-19")
        self.assertEqual(dod["normalization_status"], "html-visible-text")
        self.assertEqual(navy["normalization_status"], "html-visible-text")

        dod_rc = load("objects/research_classifications/RC-NC3-dod-e130j-contract-award-2024.json")
        navy_rc = load("objects/research_classifications/RC-NC3-navy-e130j-award-announcement-2024.json")
        self.assertEqual(dod_rc["canonical_status"], "canon")
        self.assertEqual(navy_rc["canonical_status"], "deuterocanon")

    def test_shared_award_event_is_not_double_counted(self):
        edge = load("objects/source_dependencies/SD-NC3-navy-e130j-award-to-dod-contract-action.json")
        self.assertEqual(edge["independence"], "dependent")
        comparison = load("objects/statement_comparisons/SC-NC3-e130j-planned-to-awarded-2024.json")
        self.assertEqual(
            comparison["relationship"],
            "later-first-party-contract-action-resolves-earlier-planning-state",
        )

    def test_remaining_program_gaps_are_explicit(self):
        gap = load("objects/missing_evidence/ME-NC3-public-program-source-gaps.json")
        self.assertEqual(gap["status"], "unresolved")
        self.assertIn("navair-html-and-award-state-resolved", gap["recovery_status"])

        unresolved = "\n".join(gap["unresolved_named_records"])
        recovered = "\n".join(gap["recovered_named_records"])
        self.assertIn("SAOC", unresolved)
        self.assertIn("AFGSCMD 63-101", unresolved)
        self.assertNotIn("Navy FY2026 RDT&E BA5", unresolved)
        self.assertIn("Navy FY2026 RDT&E BA5", recovered)

        ba5_success = [
            item for item in gap["retrieval_attempts"]
            if "Navy FY2026 RDT&E BA5" in item["record"] and item["artifact_preserved"]
        ]
        self.assertTrue(ba5_success)

    def test_review_and_ledger_record_64_record_state(self):
        review = (ROOT / "docs/reviews/phase2-nc3-005-e130j-award-and-detailed-parent-retry.md").read_text(encoding="utf-8")
        ledger = (ROOT / "docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md").read_text(encoding="utf-8")
        self.assertIn("64 checked / 0 failures", review)
        self.assertIn("NC3 E-130J award-state resolution", ledger)
        self.assertIn("corpus 64/0", ledger)


if __name__ == "__main__":
    unittest.main()
