import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class Nc3E130jMsarExecutionTests(unittest.TestCase):
    def test_msar_reviewed_canon(self):
        self.assertEqual(load("metadata/DOD-2026-pb-2027-modernized-selected-acquisition-reports-001.json")["evidence_status"],"reviewed")
        self.assertEqual(load("objects/research_classifications/RC-NC3-dod-e130j-msar-pb2027.json")["canonical_status"],"canon")
    def test_lineage_partial_independence(self):
        self.assertEqual(load("objects/source_dependencies/SD-NC3-dod-e130j-msar-to-navy-fy27-budget-lineage.json")["independence"],"partially-independent")
    def test_av1_only_partially_resolves_pdr(self):
        c=load("objects/statement_comparisons/SC-NC3-e130j-msar-av1-pdr-and-delivery-state.json")
        self.assertIn("AV1 configuration PDR",c["internal_content"])
        self.assertIn("full-system/final weapon-system PDR",c["internal_content"])
        self.assertIn("zero delivered",c["internal_content"])
    def test_gap_targets_full_system_pdr(self):
        g=load("objects/missing_evidence/ME-NC3-tacamo-execution-confirmation.json")
        unresolved=chr(10).join(g["unresolved_named_records"]); recovered=chr(10).join(g["recovered_named_records"])
        self.assertIn("full-system/final weapon-system Preliminary Design Review",unresolved)
        self.assertIn("AV1 configuration Preliminary Design Review",recovered)
        self.assertIn("Integrated Baseline Review",recovered)
    def test_review_keeps_zero_delivery_bounded(self):
        r=(ROOT/"docs/reviews/phase2-nc3-009-e130j-msar-execution.md").read_text()
        self.assertIn("0 actual development",r); self.assertIn("dated state",r)
if __name__=="__main__": unittest.main()
