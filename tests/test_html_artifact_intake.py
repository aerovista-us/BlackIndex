import importlib.util
import json
import stat
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("blackindex_html_test", ROOT / "tools" / "blackindex.py")
blackindex = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(blackindex)


class HtmlArtifactIntakeTests(unittest.TestCase):
    def test_html_raw_is_preserved_and_visible_text_is_normalized(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            source = Path(td) / "source.html"
            original = """<!doctype html><html><head><title>Program Page</title>
<style>.secret{display:none}</style><script>DO_NOT_INDEX</script></head>
<body><h1>Visible &amp; Verified</h1><p>Line <b>two</b>.</p>
<noscript>HIDDEN_FALLBACK</noscript></body></html>"""
            source.write_text(original, encoding="utf-8")
            args = Namespace(
                root=str(root), file=str(source), source="NAVAIR",
                collection="Program Pages", year="2026", title="Program Page",
                document_date=None, url=None, artifact_url="https://example.test/program",
                landing_url=None, native_id="program-page", record_group=None,
                series=None, call_id="CALL-HTML-TEST", tags="nc3,tacamo",
                classification_note=None, redaction_note=None,
            )
            self.assertEqual(blackindex.cmd_intake(args), 0)
            meta_path = root / "metadata" / "NAVAIR-2026-program-pages-001.json"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            raw = Path(meta["local_raw_path"])
            normalized = Path(meta["normalized_text_path"])

            self.assertEqual(raw.read_text(encoding="utf-8"), original)
            self.assertEqual(stat.S_IMODE(raw.stat().st_mode), 0o444)
            self.assertEqual(meta["normalization_status"], "html-visible-text")
            text = normalized.read_text(encoding="utf-8")
            self.assertIn("Program Page", text)
            self.assertIn("Visible & Verified", text)
            self.assertIn("Line two.", text)
            self.assertNotIn("DO_NOT_INDEX", text)
            self.assertNotIn("HIDDEN_FALLBACK", text)
            self.assertNotIn(".secret", text)


if __name__ == "__main__":
    unittest.main()
