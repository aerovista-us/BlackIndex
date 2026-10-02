import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools" / "inject-inline-definitions.py"

spec = importlib.util.spec_from_file_location("inline_defs", INJECT)
defs = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(defs)


class InlineDefinitionsUiTests(unittest.TestCase):
    def test_injects_idempotently(self):
        with tempfile.TemporaryDirectory() as td:
            page = Path(td) / "work-queue.html"
            page.write_text(
                "<!doctype html><html><head></head><body>"
                "<div id='bi-help-body'><div class='bi-help-note'>note</div></div>"
                "<div class='cards'><div class='card'>HOLD<strong>1</strong></div></div>"
                "</body></html>",
                encoding="utf-8",
            )
            for _ in range(2):
                p = subprocess.run(
                    [sys.executable, str(INJECT), str(page)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            text = page.read_text(encoding="utf-8")
            self.assertEqual(text.count("BLACKINDEX_INLINE_DEFINITIONS"), 1)
            self.assertIn("bi-meaning-popover", text)
            self.assertIn("Glossary / What does this mean?", text)

    def test_glossary_covers_requested_meaning_categories(self):
        script = defs.SCRIPT
        for value in (
            "Archive confidence",
            "Completeness",
            "Redaction concern",
            "Missing refs",
            "Unreviewed",
            "Reviewed",
            "PROMOTE",
            "HOLD",
            "MERGE",
            "REJECT-BOUNDARY",
            "Dependent",
            "Partially independent",
            "Sampled AI coverage",
            "Complete source coverage",
            "AI-derived research aid",
            "Canon",
            "Apocrypha",
            "Pseudepigrapha",
            "Deuterocanon",
            "Authenticity status",
            "Attribution status",
            "Provenance status",
            "Corroboration status",
            "Source independence",
            "Classification confidence",
        ):
            self.assertIn(value, script)

    def test_source_text_is_excluded_from_generic_annotation(self):
        script = defs.SCRIPT
        self.assertIn("el.closest('pre,#list,.bi-line-text')", script)

    def test_supports_hover_focus_and_tap(self):
        script = defs.SCRIPT
        for event in ("mouseenter", "mouseleave", "focus", "blur", "click"):
            self.assertIn(event, script)
        self.assertIn("aria-label", script)
        self.assertIn("pinned=true", script)

    def test_dynamic_content_is_rescanned(self):
        self.assertIn("MutationObserver", defs.SCRIPT)
        self.assertIn("requestAnimationFrame(scan)", defs.SCRIPT)

    def test_help_glossary_integration_exists(self):
        script = defs.SCRIPT
        self.assertIn("bi-help-glossary", script)
        self.assertIn("data-help-search", script)
        self.assertIn("bi-help-body", script)

    def test_serve_pipeline_runs_definitions_after_help(self):
        serve = (ROOT / "tools" / "serve-dashboard.sh").read_text(encoding="utf-8")
        help_pos = serve.index("inject-help-system.py")
        defs_pos = serve.index("inject-inline-definitions.py")
        self.assertLess(help_pos, defs_pos)
        for name in (
            "blackindex-dashboard.html",
            "work-queue.html",
            "named-source-recovery.html",
            "source-lineage.html",
            "entities.html",
        ):
            self.assertIn(name, serve)


if __name__ == "__main__":
    unittest.main()
