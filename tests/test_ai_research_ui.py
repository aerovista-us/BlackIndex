import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools" / "inject-ai-research.py"


class AiResearchUiTests(unittest.TestCase):
    def test_ai_panel_injects_once(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "blackindex-dashboard.html"
            page.write_text(
                "<!doctype html><html><head></head><body>"
                "<section id='view'><div class='bi-record-tools'></div><pre></pre></section>"
                "<script>let current={metadata:{doc_id:'DOC-A'}};let tab='text';function renderView(){}</script>"
                "</body></html>",
                encoding="utf-8",
            )
            for _ in range(2):
                p = subprocess.run([sys.executable, str(INJECT), str(page)], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_AI_RESEARCH"), 1)
            for label in ("AI Research Assistant", "Quick Summary", "Deep Summary", "Timeline", "People &amp; Organizations", "Explain Simply", "Summarize Selection", "Ask this document", "Quick Compare", "Deep Compare"):
                self.assertIn(label, text)
            self.assertIn("/api/ai/status", text)
            self.assertIn("/api/ai/research", text)
            self.assertIn("never promoted to evidence", text)
            self.assertIn("jumpToCitation", text)
            self.assertIn("bi-source-line", text)
            self.assertIn("data-ai-mode", text)
            self.assertIn("jumpToCitation", text)
            self.assertIn("activeCitation", text)
            self.assertIn("lastAiResult", text)
            self.assertIn("bi-cite-hit", text)
            self.assertIn("data-cite-start", text)
            self.assertIn("data-cite-doc", text)
            self.assertIn("data-ai-compare-doc", text)
            self.assertIn("data-ai-compare-focus", text)
            self.assertIn("citation_docs", text)

    def test_server_exposes_local_ai_endpoints_without_evidence_writes(self):
        src = (ROOT / "tools" / "blackindex-ui-server.py").read_text(encoding="utf-8")
        self.assertIn('"/api/ai/status"', src)
        self.assertIn('"/api/ai/research"', src)
        self.assertIn("ai_research.handle", src)
        self.assertNotIn("objects/research_classifications", src)
        self.assertNotIn("publish-ingest", src)

    def test_dashboard_pipeline_injects_ai_layer(self):
        src = (ROOT / "tools" / "serve-dashboard.sh").read_text(encoding="utf-8")
        self.assertIn('inject-ai-research.py', src)


if __name__ == "__main__":
    unittest.main()
