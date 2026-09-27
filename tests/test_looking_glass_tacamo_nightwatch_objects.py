import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LookingGlassTacamoNightwatchObjectTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_classification_split(self):
        posture = self.load("objects/research_classifications/RC-LOOKING-GLASS-usstratcom-2024-posture.json")
        navy = self.load("objects/research_classifications/RC-LOOKING-GLASS-usnavy-2017-program-guide.json")
        e4b = self.load("objects/research_classifications/RC-LOOKING-GLASS-usaf-2019-e4b-manual.json")
        self.assertEqual(posture["canonical_status"], "deuterocanon")
        self.assertEqual(navy["canonical_status"], "deuterocanon")
        self.assertEqual(e4b["canonical_status"], "canon")

    def test_review_keeps_procedures_out_of_findings(self):
        text = (ROOT / "docs/reviews/phase2-looking-glass-005-tacamo-nightwatch-baseline.md").read_text(encoding="utf-8")
        self.assertIn("does **not** extract, summarize, or promote detailed", text)
        self.assertIn("not counted as three independent proofs", text)
        self.assertIn("actual use in a particular incident", text)


if __name__ == "__main__":
    unittest.main()
