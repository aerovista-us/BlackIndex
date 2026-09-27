import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LookingGlassAuthorityFamilyObjectTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_recovered_directives_are_document_canon(self):
        for rel in [
            "objects/research_classifications/RC-LOOKING-GLASS-afpd13-5-policy.json",
            "objects/research_classifications/RC-LOOKING-GLASS-afi13-520-successor.json",
        ]:
            obj = self.load(rel)
            self.assertEqual(obj["canonical_status"], "canon")
            self.assertEqual(obj["subject_type"], "document")

    def test_successor_dependency_and_missing_predecessor_are_explicit(self):
        dep = self.load("objects/source_dependencies/SD-2018-afi13-520-to-afpd13-5.json")
        self.assertEqual(dep["independence"], "dependent")
        gap = self.load("objects/missing_evidence/ME-LOOKING-GLASS-2017-alcs-authority-source-family.json")
        self.assertEqual(gap["historical_predecessor_status"]["status"], "superseded-historical-source-unrecovered")
        self.assertIn("public_declassified_availability_scan_2026_09_27", gap)


if __name__ == "__main__":
    unittest.main()
