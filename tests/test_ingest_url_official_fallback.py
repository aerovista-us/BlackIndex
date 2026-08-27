import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-url.sh"


class OfficialSourceFallbackTests(unittest.TestCase):
    def test_browser_fallback_is_narrow_and_checks_soft_blocks(self):
        text = SCRIPT.read_text(encoding="utf-8")

        # Enhanced browser behavior stays constrained to known first-party
        # government hosts instead of being applied to arbitrary sources.
        self.assertIn("https://vault.fbi.gov/*", text)
        self.assertIn("https://www.cia.gov/*", text)
        self.assertIn("ALLOW_BROWSER_FALLBACK=0", text)
        self.assertIn("ALLOW_BROWSER_FALLBACK=1", text)

        # A WAF/interstitial may return HTTP 200 with HTML. The retry decision
        # therefore has to inspect PDF magic as well as curl's exit code.
        self.assertIn("pdf_magic_ok", text)
        self.assertIn("needs_browser_retry", text)
        self.assertIn("Direct request returned non-PDF content", text)

        # Both navigation and browser-TLS tiers remain direct-source fetches,
        # and the final PDF magic guard is still mandatory.
        self.assertIn("Sec-Fetch-Dest: document", text)
        self.assertIn("fetch-browser-tls.py", text)
        self.assertIn('[[ "$MAGIC" == "%PDF-" ]]', text)
        self.assertIn("No proxy/mirror", text)


if __name__ == "__main__":
    unittest.main()
