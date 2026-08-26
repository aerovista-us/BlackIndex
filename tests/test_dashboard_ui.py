import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "tools/fix-dashboard-html.py"


class DashboardUtilityTests(unittest.TestCase):
    def test_standalone_utility_layer_is_injected_once(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "blackindex-dashboard.html"
            page.write_text(
                "<!doctype html><html><head><style>:root{--line:#222}</style></head>"
                "<body><header><div class='controls'></div></header><main></main>"
                "<script>const DATA={documents:[],evidence_map:{objects:{}}};"
                "const docs=[];let filtered=[];let current=null;let tab='extraction';"
                "const esc=s=>String(s);function searchable(d){return ''}"
                "function renderList(){} function renderView(){}</script></body></html>",
                encoding="utf-8",
            )
            for _ in range(2):
                p = subprocess.run([sys.executable, str(POST), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_UI_UTILITY"), 1)
            for label in ("Work Queue", "Lineage", "Entities", "Unreviewed", "Missing refs", "Export record", "Resume FBI Review"):
                self.assertIn(label, text)
            self.assertIn("data-bi-mode", text)
            self.assertIn("history.replaceState", text)
            self.assertIn("navigator.clipboard", text)
            self.assertNotIn("<script src=", text)
            self.assertNotIn("<link rel=\"stylesheet\" href=\"http", text)


if __name__ == "__main__":
    unittest.main()
