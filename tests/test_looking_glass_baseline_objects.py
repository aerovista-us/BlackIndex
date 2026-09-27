import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJ = ROOT / "objects" / "research_classifications"


class LookingGlassBaselineObjectTests(unittest.TestCase):
    def _load(self, name):
        return json.loads((OBJ / name).read_text(encoding="utf-8"))

    def test_official_histories_are_synthesis_layers_not_canon(self):
        names = [
            "RC-LOOKING-GLASS-sac-alert-ops-synthesis.json",
            "RC-LOOKING-GLASS-winged-shield-vol2-synthesis.json",
        ]
        for name in names:
            obj = self._load(name)
            self.assertEqual(obj["subject_type"], "document")
            self.assertEqual(obj["canonical_status"], "deuterocanon")
            self.assertTrue(obj["review_required"])
            self.assertNotEqual(obj.get("source_independence"), "independent")

    def test_authority_limits_are_explicit(self):
        sac = self._load("RC-LOOKING-GLASS-sac-alert-ops-synthesis.json")
        text = (sac["reason"] + " " + sac["corroboration_status"]).lower()
        self.assertIn("operational order", text)
        self.assertIn("nuclear-use authorization", text)
        self.assertIn("underlying-record", text)


if __name__ == "__main__":
    unittest.main()
