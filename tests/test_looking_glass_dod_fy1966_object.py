import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJ = ROOT / "objects" / "research_classifications" / "RC-LOOKING-GLASS-dod-fy1966-program-report.json"
META = ROOT / "metadata" / "DOD-1967-department-of-defense-annual-reports-001.json"


class LookingGlassDodFY1966ObjectTests(unittest.TestCase):
    def test_program_report_is_not_promoted_to_canon(self):
        obj = json.loads(OBJ.read_text(encoding="utf-8"))
        self.assertEqual(obj["subject_type"], "document")
        self.assertEqual(obj["canonical_status"], "deuterocanon")
        self.assertTrue(obj["review_required"])
        self.assertNotEqual(obj.get("source_independence"), "independent")
        text = (obj["reason"] + " " + obj["corroboration_status"]).lower()
        self.assertIn("emergency war order", text)
        self.assertIn("nuclear-use authorization", text)

    def test_unknown_day_and_month_are_not_fabricated(self):
        meta = json.loads(META.read_text(encoding="utf-8"))
        self.assertEqual(meta["year_bucket"], "1967")
        self.assertIsNone(meta["document_date"])


if __name__ == "__main__":
    unittest.main()
