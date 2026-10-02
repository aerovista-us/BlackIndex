import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INJECT = ROOT / "tools" / "inject-help-system.py"

spec = importlib.util.spec_from_file_location("context_help_inject", INJECT)
help_inject = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(help_inject)


class ContextHelpUiTests(unittest.TestCase):
    def _page(self, directory: Path, name: str, with_head: bool = True) -> Path:
        page = directory / name
        if with_head:
            html = (
                "<!doctype html><html><head><meta charset='utf-8'><title>Test</title>"
                "<style>body{background:#111}</style></head><body>"
                "<header><h1>Test</h1></header><main><h2>Section</h2></main></body></html>"
            )
        else:
            html = (
                "<!doctype html><meta charset='utf-8'><title>Test</title>"
                "<style>body{background:#111}</style><body>"
                "<header><h1>Test</h1></header><main><h2>Section</h2></main></body>"
            )
        page.write_text(html, encoding="utf-8")
        return page

    def test_injects_idempotent_help_layer_on_all_ui_names(self):
        names = [
            "blackindex-dashboard.html",
            "work-queue.html",
            "named-source-recovery.html",
            "source-lineage.html",
            "entities.html",
        ]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            pages = [self._page(root, name, with_head=(i % 2 == 0)) for i, name in enumerate(names)]
            for _ in range(2):
                p = subprocess.run(
                    [sys.executable, str(INJECT), *[str(x) for x in pages]],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

            for page in pages:
                text = page.read_text(encoding="utf-8")
                self.assertEqual(text.count("BLACKINDEX_CONTEXT_HELP"), 1)
                self.assertIn("helpBtn.id='bi-help-open'", text)
                self.assertIn("tipBtn.id='bi-tip-open'", text)
                self.assertIn("Show me around", text)
                self.assertIn("Tips & tricks", text)
                self.assertIn("blackindex-help-hint-v1", text)
                self.assertIn("MutationObserver", text)
                self.assertLess(text.index("<!doctype"), text.index("BLACKINDEX_CONTEXT_HELP"))

    def test_help_content_covers_primary_blackindex_sections(self):
        script = help_inject.SCRIPT
        for value in (
            "Evidence Map",
            "Work Queue",
            "Named Source Recovery",
            "Source Lineage",
            "Entities",
            "AI Research Assistant",
            "Clickable citations",
            "Missing evidence",
            "Shared upstream family",
            "Document mention",
        ):
            self.assertIn(value, script)

    def test_multiple_help_patterns_exist(self):
        script = help_inject.SCRIPT
        for marker in (
            "openHelp",
            "showTip",
            "startTour",
            "applyContextualHelp",
            "bi-inline-help",
            "bi-help-search",
            "bi-help-hint",
        ):
            self.assertIn(marker, script)

    def test_main_dashboard_help_controls_avoid_existing_bottom_controls(self):
        style = help_inject.STYLE
        self.assertIn("bi-help-page-evidence #bi-help-open{bottom:112px}", style)
        self.assertIn("bi-help-page-evidence #bi-tip-open{bottom:154px}", style)

    def test_serve_pipeline_injects_help_into_all_pages(self):
        serve = (ROOT / "tools" / "serve-dashboard.sh").read_text(encoding="utf-8")
        self.assertIn("inject-help-system.py", serve)
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
