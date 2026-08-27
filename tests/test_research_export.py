import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools/inject-research-export.py"


class ResearchExportTests(unittest.TestCase):
    def test_export_is_local_only_and_injected_once(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "blackindex-dashboard.html"
            page.write_text("<!doctype html><html><body><aside id='bi-session'><div id='bi-session-body'></div></aside></body></html>", encoding="utf-8")
            for _ in range(2):
                p = subprocess.run([sys.executable, str(INJECT), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_RESEARCH_EXPORT"), 1)
            self.assertIn("Copy pinned IDs", text)
            self.assertIn("Export JSON", text)
            self.assertIn("Export Markdown", text)
            self.assertIn("Clear recent", text)
            self.assertIn("blackindex-research-session-export-v1", text)
            self.assertIn("new Blob", text)
            self.assertIn("navigator.clipboard", text)
            self.assertIn("Browser-local convenience state only", text)
            self.assertNotIn("fetch(", text)
            self.assertNotIn("XMLHttpRequest", text)
            self.assertNotIn("<script src=", text)
            self.assertNotIn("https://cdn", text)


if __name__ == "__main__":
    unittest.main()
