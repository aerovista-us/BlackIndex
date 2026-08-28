import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "map-review-007-physical-pages.py"
spec = importlib.util.spec_from_file_location("review_007_physical_pages", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Review007PhysicalPageMapperTests(unittest.TestCase):
    def test_unique_exact_match_verifies_page(self):
        result = mod.choose_exact(
            60,
            "Hello   world\nrecord text",
            {59: "different", 60: "Hello world record text", 61: "other"},
        )
        self.assertEqual(result["mapping_status"], "EXACT_SAME_INDEX")
        self.assertTrue(result["physical_page_verified"])
        self.assertEqual(result["physical_page_index"], 60)

    def test_unique_nearby_exact_match_is_reported(self):
        result = mod.choose_exact(
            60,
            "target text",
            {59: "target text", 60: "other", 61: "other two"},
        )
        self.assertEqual(result["mapping_status"], "EXACT_NEARBY")
        self.assertTrue(result["physical_page_verified"])
        self.assertEqual(result["physical_page_index"], 59)

    def test_ambiguous_exact_match_never_verifies(self):
        result = mod.choose_exact(
            60,
            "repeated footer only",
            {59: "repeated footer only", 60: "repeated footer only"},
        )
        self.assertEqual(result["mapping_status"], "AMBIGUOUS_EXACT_MATCH")
        self.assertFalse(result["physical_page_verified"])
        self.assertIsNone(result["physical_page_index"])

    def test_fuzzy_similarity_is_not_used(self):
        result = mod.choose_exact(60, "alpha beta gamma", {60: "alpha beta delta"})
        self.assertEqual(result["mapping_status"], "UNRESOLVED_NO_EXACT_MATCH")
        self.assertFalse(result["physical_page_verified"])

    def test_source_declares_no_ocr_or_promotion(self):
        text = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn('"ocr_used": False', text)
        self.assertIn('"fuzzy_match_used": False', text)
        self.assertIn('"record_promotions": 0', text)
        self.assertNotIn("evidence_map.py", text)


if __name__ == "__main__":
    unittest.main()
