import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class Nc3GaoE130jOversightTests(unittest.TestCase):
    def test_gao_reviewed_and_canon(self):
        self.assertEqual(load("metadata/GAO-2026-weapon-systems-annual-assessment-001.json")["evidence_status"],"reviewed")
        self.assertEqual(load("objects/research_classifications/RC-NC3-gao-2026-e130j-oversight.json")["canonical_status"],"canon")
    def test_partial_independence(self):
        self.assertEqual(load("objects/source_dependencies/SD-NC3-gao-2026-e130j-to-msar-program-lineage.json")["independence"],"partially-independent")
    def test_temporal_boundary(self):
        c=load("objects/statement_comparisons/SC-NC3-gao-e130j-risk-to-msar-execution-state.json")
        self.assertIn("one-year",c["public_statement"])
        self.assertIn("full-system PDR as future",c["internal_content"])
    def test_review_keeps_pdr_open(self):
        r=(ROOT/"docs/reviews/phase2-nc3-010-gao-e130j-oversight.md").read_text()
        self.assertIn("does not prove or disprove",r)
        self.assertIn("full-system PDR",r)
if __name__=="__main__": unittest.main()
