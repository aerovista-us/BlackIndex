import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class Nc3Gao2025E130jRiskTests(unittest.TestCase):
    def test_source_reviewed_and_canon(self):
        self.assertEqual(load("metadata/GAO-2025-weapon-systems-annual-assessment-001.json")["evidence_status"],"reviewed")
        self.assertEqual(load("objects/research_classifications/RC-NC3-gao-2025-e130j-oversight.json")["canonical_status"],"canon")
    def test_annual_gao_lineage_is_dependent(self):
        self.assertEqual(load("objects/source_dependencies/SD-NC3-gao-2026-to-gao-2025-e130j-oversight-lineage.json")["independence"],"dependent")
    def test_risk_progression_is_longitudinal(self):
        c=load("objects/statement_comparisons/SC-NC3-gao-e130j-2025-to-2026-risk-progression.json")
        self.assertIn("materialized",c["internal_content"])
        self.assertIn("not independent proof",c["notes"])
    def test_underlying_2024_assessment_is_explicit_gap(self):
        g=load("objects/missing_evidence/ME-NC3-e130j-2024-independent-technical-risk-assessment.json")
        self.assertEqual(g["status"],"unresolved")
        self.assertIn("September 2024 E-130J independent technical risk assessment",g["unresolved_named_records"])
if __name__=="__main__": unittest.main()
