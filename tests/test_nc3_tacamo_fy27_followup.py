import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Nc3TacamoFy27FollowupTests(unittest.TestCase):
    def test_fy27_primary_source_is_reviewed_and_canon(self):
        meta = load("metadata/US_NAVY-2026-fy-2027-rdt-e-budget-justification-books-001.json")
        rc = load("objects/research_classifications/RC-NC3-navy-fy27-ba5-tacamo-followup.json")
        self.assertEqual(meta["evidence_status"], "reviewed")
        self.assertEqual(meta["normalization_status"], "pdftotext")
        self.assertEqual(rc["canonical_status"], "canon")
        self.assertIn("not promoted as completed", rc["reason"])

    def test_fy26_fy27_are_longitudinal_not_independent_corroboration(self):
        edge = load("objects/source_dependencies/SD-NC3-navy-fy27-ba5-to-fy26-ba5-lineage.json")
        self.assertEqual(edge["independence"], "dependent")
        self.assertEqual(edge["dependency_type"], "same-program-longitudinal-budget-state")

    def test_schedule_update_records_exact_execution_boundary(self):
        comp = load("objects/statement_comparisons/SC-NC3-tacamo-fy26-to-fy27-schedule-update.json")
        self.assertEqual(
            comp["relationship"],
            "later-first-party-budget-state-revises-prior-funding-and-schedule-windows",
        )
        changes = {item["event"]: item for item in comp["schedule_changes"]}
        self.assertEqual(changes["CSIL Test"]["fy2026_book"], "Q3-Q4 FY2026")
        self.assertEqual(changes["CSIL Test"]["fy2027_book"], "Q1 FY2027-Q4 FY2031")
        self.assertEqual(changes["Integrated Test 1"]["fy2026_book"], "Q2-Q4 FY2026")
        self.assertEqual(changes["Integrated Test 1"]["fy2027_book"], "Q1 FY2027-Q2 FY2028")
        self.assertIn("not milestone completion", comp["notes"])

    def test_execution_confirmation_remains_explicitly_missing(self):
        gap = load("objects/missing_evidence/ME-NC3-tacamo-execution-confirmation.json")
        self.assertEqual(gap["status"], "unresolved")
        joined = "\n".join(gap["unresolved_named_records"])
        self.assertIn("Preliminary Design Review", joined)
        self.assertIn("CSIL", joined)
        self.assertIn("Integrated Test 1", joined)
        self.assertIn("SDTA", joined)

    def test_review_preserves_schedule_update_language(self):
        review = (ROOT / "docs/reviews/phase2-nc3-008-fy27-tacamo-schedule-update.md").read_text(encoding="utf-8")
        self.assertIn("published program-state change", review)
        self.assertIn("schedule update/revision", review)
        self.assertNotIn("PDR was completed.", review)


if __name__ == "__main__":
    unittest.main()
