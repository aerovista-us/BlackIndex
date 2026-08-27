import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "tools/fix-dashboard-html.py"
CONTEXT = ROOT / "tools/inject-record-context.py"


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
            for label in ("Work Queue", "Named Sources", "Lineage", "Entities", "Unreviewed", "Missing refs", "Export record", "Resume FBI Review"):
                self.assertIn(label, text)
            self.assertIn('/named-source-recovery.html', text)
            self.assertIn("data-bi-mode", text)
            self.assertIn("history.replaceState", text)
            self.assertIn("navigator.clipboard", text)
            self.assertNotIn("<script src=", text)
            self.assertNotIn("<link rel=\"stylesheet\" href=\"http", text)

    def test_record_context_is_embedded_from_encoded_indexes_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            dashboard = root / "local/dashboard"
            index = root / "local/index"
            dashboard.mkdir(parents=True)
            index.mkdir(parents=True)
            page = dashboard / "blackindex-dashboard.html"
            page.write_text(
                "<!doctype html><html><head><style>:root{--line:#222}</style></head><body>"
                "<section id='view'></section><script>let current=null;</script></body></html>",
                encoding="utf-8",
            )
            (index / "entity-index.json").write_text(json.dumps({
                "entities": [{"entity_id": "person:test-person", "canonical_name": "Test Person"}],
                "edges": [{"edge_type": "document_mentions_entity", "from": "DOC-A", "to": "person:test-person", "entity_type": "person"}],
            }), encoding="utf-8")
            (index / "source-lineage.json").write_text(json.dumps({
                "edges": [{"source_id": "DOC-A", "depends_on": "DOC-B", "dependency_type": "summary-derived-from", "independence": "dependent"}],
            }), encoding="utf-8")
            (index / "research-reference-audit.json").write_text(json.dumps({
                "pairs": [{"doc_a": "DOC-A", "doc_b": "DOC-C", "status": "REVIEW_REQUIRED", "cooccurrence_files": 2}],
            }), encoding="utf-8")
            (index / "review-state-audit.json").write_text(json.dumps({
                "mismatches": [{"doc_id": "DOC-A", "extraction_state": "substantive", "finding": "metadata status lag"}],
            }), encoding="utf-8")

            for _ in range(2):
                p = subprocess.run([sys.executable, str(CONTEXT), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_RECORD_CONTEXT"), 1)
            for value in ("Test Person", "DOC-B", "DOC-C", "metadata status lag", "Record context"):
                self.assertIn(value, text)
            self.assertIn("Entity mention does not imply conduct", text)
            self.assertNotIn("<script src=", text)
            self.assertNotIn("https://cdn", text)


if __name__ == "__main__":
    unittest.main()
