import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools/inject-favicon.py"


class FaviconTests(unittest.TestCase):
    def test_favicon_is_embedded_and_injected_once(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "blackindex-dashboard.html"
            page.write_text("<!doctype html><html><head></head><body></body></html>", encoding="utf-8")
            for _ in range(2):
                p = subprocess.run([sys.executable, str(INJECT), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_FAVICON"), 1)
            self.assertIn('rel="icon"', text)
            self.assertIn("data:image/svg+xml", text)
            self.assertNotIn("favicon.ico", text)
            self.assertNotIn("http://", text)
            self.assertNotIn("https://", text)


if __name__ == "__main__":
    unittest.main()
