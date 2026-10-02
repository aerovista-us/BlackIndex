import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Nc3ExecutionMilestoneTests(unittest.TestCase):
    def test_execution_records_are_preserved_and_scoped(self):
        cases = [
            ("metadata/DOD-2024-contract-announcements-002.json", "2024-04-26",
             "objects/research_classifications/RC-NC3-dod-saoc-contract-award-2024.json"),
            ("metadata/USAF-2025-air-force-global-strike-command-news-001.json", "2025-03-28",
             "objects/research_classifications/RC-NC3-usaf-95th-wing-activation-2025.json"),
            ("metadata/USSTRATCOM-2019-news-releases-001.json", "2019-04-03",
             "objects/research_classifications/RC-NC3-usstratcom-nec-ioc-2019.json"),
        ]
        for meta_rel, date, rc_rel in cases:
            meta = load(meta_rel)
            self.assertEqual(meta["document_date"], date)
            self.assertEqual(meta["normalization_status"], "html-visible-text")
            self.assertEqual(load(rc_rel)["canonical_status"], "canon")

    def test_95th_wing_and_saoc_award_are_not_collapsed(self):
        edge = load("objects/source_dependencies/SD-NC3-usaf-95th-wing-to-saoc-program-lineage.json")
        self.assertEqual(edge["independence"], "partially-independent")
        self.assertIn("not be collapsed", edge["notes"])

    def test_review_and_ledger_record_67_record_state(self):
        review = (ROOT / "docs/reviews/phase2-nc3-006-execution-milestones.md").read_text(encoding="utf-8")
        ledger = (ROOT / "docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md").read_text(encoding="utf-8")
        self.assertIn("67 checked / 0 failures", review)
        self.assertIn("NC3 execution-milestone baseline", ledger)
        self.assertIn("corpus 67/0", ledger)
        self.assertIn("expected", review)
        self.assertIn("forecast", review)

    def test_snc_test_activity_is_contractor_primary_not_government_acceptance(self):
        meta = load("metadata/SNC-2025-saoc-program-press-releases-001.json")
        rc = load("objects/research_classifications/RC-NC3-snc-saoc-flight-test-2025.json")
        edge = load("objects/source_dependencies/SD-NC3-snc-2025-saoc-test-to-dod-award-lineage.json")
        self.assertEqual(meta["evidence_status"], "reviewed")
        self.assertEqual(rc["canonical_status"], "deuterocanon")
        self.assertIn("not U.S. Air Force acceptance", rc["reason"])
        self.assertEqual(edge["independence"], "partially-independent")
        self.assertIn("does not provide an independent U.S. Air Force acceptance", edge["notes"])


if __name__ == "__main__":
    unittest.main()
