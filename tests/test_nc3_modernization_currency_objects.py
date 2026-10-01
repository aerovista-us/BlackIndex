from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text())

class NC3ModernizationCurrencyObjectTests(unittest.TestCase):
    def test_posture_version_family_prevents_double_count(self):
        d = load("objects/version_families/VF-NC3-usstratcom-posture-2024-2026.json")
        self.assertEqual(len(d["doc_ids"]), 3)
        self.assertIn("not independent corroboration", d["relationship_scope"])

    def test_new_document_classifications(self):
        for rel, status in [
            ("objects/research_classifications/RC-NC3-2022-npr-strategy-layer.json", "deuterocanon"),
            ("objects/research_classifications/RC-NC3-usstratcom-2025-posture.json", "deuterocanon"),
            ("objects/research_classifications/RC-NC3-usstratcom-2026-posture.json", "deuterocanon"),
            ("objects/research_classifications/RC-NC3-s510092-placeholder.json", "canon"),
        ]:
            self.assertEqual(load(rel)["canonical_status"], status)
    def test_posture_series_edges_are_dependent(self):
        for year in (2024, 2025, 2026):
            d = load(f"objects/source_dependencies/SD-NC3-usstratcom-{year}-posture-series.json")
            self.assertEqual(d["independence"], "dependent")

    def test_dnlcc_governance_edge_is_dependent(self):
        d = load("objects/source_dependencies/SD-NC3-dodi3741-to-dodi-s510092.json")
        self.assertEqual(d["independence"], "dependent")
        self.assertIn("S-5100.92", d["depends_on"])

    def test_currency_snapshot_keeps_access_states_distinct(self):
        d = load("objects/missing_evidence/ME-NC3-controlled-governance-family.json")
        self.assertEqual(d["currency_checked_at"], "2026-10-01")
        self.assertIn("no public first-party artifact", d["current_index_status"]["DoDD S-3730.02"])
        self.assertIn("public placeholder preserved", d["current_index_status"]["DoDI S-5100.92"])
        self.assertEqual(d["status"], "unresolved")

if __name__ == "__main__":
    unittest.main()
