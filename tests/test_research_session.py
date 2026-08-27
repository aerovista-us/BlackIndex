import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools/inject-research-session.py"


class ResearchSessionTests(unittest.TestCase):
    def test_session_is_local_only_and_injected_once(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "blackindex-dashboard.html"
            page.write_text("<!doctype html><html><body><section id='view'></section></body></html>", encoding="utf-8")
            for _ in range(2):
                p = subprocess.run([sys.executable, str(INJECT), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_RESEARCH_SESSION"), 1)
            self.assertIn("Research Session", text)
            self.assertIn("localStorage", text)
            self.assertIn("Pin record", text)
            self.assertIn("Recent records", text)
            self.assertIn("blackindex.pins.v1", text)
            self.assertNotIn("fetch(", text)
            self.assertNotIn("<script src=", text)
            self.assertNotIn("https://cdn", text)


if __name__ == "__main__":
    unittest.main()
