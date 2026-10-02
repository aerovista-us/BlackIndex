from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text())

class NC3ProgramGenealogyObjectTests(unittest.TestCase):
    def test_program_index_classifications_are_deuterocanon(self):
        for rel in [
            "objects/research_classifications/RC-NC3-dod-fy26-r1-saoc-program-index.json",
            "objects/research_classifications/RC-NC3-navy-fy26-ba1-3-tacamo-index.json",
        ]:
            self.assertEqual(load(rel)["canonical_status"], "deuterocanon")

    def test_cross_layer_edges_do_not_claim_independence(self):
        for rel in [
            "objects/source_dependencies/SD-NC3-usstratcom-2026-saoc-to-fy26-budget-lineage.json",
            "objects/source_dependencies/SD-NC3-usstratcom-2026-tacamo-to-fy26-navy-budget-lineage.json",
        ]:
            self.assertEqual(load(rel)["independence"], "partially-independent")
    def test_public_program_source_gaps_remain_unresolved(self):
        d = load("objects/missing_evidence/ME-NC3-public-program-source-gaps.json")
        self.assertEqual(d["status"], "unresolved")
        joined = "\n".join(d["named_records"])
        self.assertIn("AFGSCMD 63-101", joined)
        self.assertIn("RDT&E BA5", joined)
        self.assertIn("SAOC", joined)
        self.assertIn("transport/retrieval failures", d["stated_reason_missing"])
        self.assertNotIn("capture-format limitations", d["stated_reason_missing"])

    def test_navy_classification_preserves_ba1_3_boundary(self):
        d = load("objects/research_classifications/RC-NC3-navy-fy26-ba1-3-tacamo-index.json")
        self.assertIn("not the detailed BA5", d["reason"])

    def test_detailed_ba5_parent_is_preserved_without_double_counting_index(self):
        detail = load("objects/research_classifications/RC-NC3-navy-fy26-ba5-tacamo-detail.json")
        edge = load("objects/source_dependencies/SD-NC3-navy-fy26-ba1-3-index-to-ba5-detail.json")
        self.assertEqual(detail["canonical_status"], "canon")
        self.assertIn("planned milestone windows are not proof", detail["reason"])
        self.assertEqual(edge["independence"], "dependent")
        self.assertIn("must not be counted as independent corroboration", edge["notes"])

if __name__ == "__main__":
    unittest.main()
