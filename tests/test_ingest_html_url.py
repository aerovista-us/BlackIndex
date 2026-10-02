import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-html-url.sh"
FETCHER = ROOT / "tools" / "fetch-browser-tls.py"


class HtmlUrlIngestGuardTests(unittest.TestCase):
    def test_html_fallback_is_narrow_and_rejects_interstitials(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("https://www.navair.navy.mil/*", text)
        self.assertIn("https://www.stratcom.mil/*", text)
        self.assertIn("https://www.navy.mil/*", text)
        self.assertIn("https://www.defense.gov/*", text)
        self.assertIn("ALLOW_BROWSER_FALLBACK=0", text)
        self.assertIn("--expect html", text)
        self.assertIn("attention required! | cloudflare", text)
        self.assertIn("/cdn-cgi/challenge-platform", text)
        self.assertIn("html_guard", text)
        self.assertNotIn("https://example.com/*", text)

    def test_browser_fetch_defaults_to_pdf_and_html_is_explicit(self):
        text = FETCHER.read_text(encoding="utf-8")
        self.assertIn('choices=("pdf", "html")', text)
        self.assertIn('default="pdf"', text)
        self.assertIn('args.expect == "pdf"', text)
        self.assertIn("blocked/interstitial HTML", text)


if __name__ == "__main__":
    unittest.main()
