import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Nc3HtmlProgramObjectTests(unittest.TestCase):
    def test_navair_html_records_and_classifications(self):
        product_meta = load("metadata/NAVAIR-2026-product-pages-001.json")
        news_meta = load("metadata/NAVAIR-2024-news-releases-001.json")
        self.assertEqual(product_meta["normalization_status"], "html-visible-text")
        self.assertEqual(news_meta["normalization_status"], "html-visible-text")
        self.assertEqual(product_meta["mime_hint"], "html")
        self.assertEqual(news_meta["mime_hint"], "html")

        product_rc = load("objects/research_classifications/RC-NC3-navair-e130j-product-page.json")
        news_rc = load("objects/research_classifications/RC-NC3-navair-e130j-2024-announcement.json")
        self.assertEqual(product_rc["canonical_status"], "deuterocanon")
        self.assertEqual(news_rc["canonical_status"], "deuterocanon")

    def test_shared_lineage_is_not_independent(self):
        product_edge = load("objects/source_dependencies/SD-NC3-navair-product-to-pma271-public-lineage.json")
        budget_edge = load("objects/source_dependencies/SD-NC3-navair-2024-announcement-to-fy26-navy-budget-lineage.json")
        self.assertEqual(product_edge["independence"], "dependent")
        self.assertEqual(budget_edge["independence"], "partially-independent")

    def test_review_and_ledger_record_completed_html_gate(self):
        review = (ROOT / "docs/reviews/phase2-nc3-004-html-program-pages.md").read_text(encoding="utf-8")
        ledger = (ROOT / "docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md").read_text(encoding="utf-8")
        self.assertIn("62 checked / 0 failures", review)
        self.assertIn("HTML-CAPTURE / PROGRAM-PUBLICATION MILESTONE", review)
        self.assertIn("NC3 HTML program-page capture", ledger)
        self.assertIn("corpus 62/0", ledger)


if __name__ == "__main__":
    unittest.main()
