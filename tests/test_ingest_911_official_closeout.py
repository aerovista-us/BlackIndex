import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-911-official-closeout.sh"


class Official911CloseoutSprintTests(unittest.TestCase):
    def test_sprint_is_bounded_and_uses_preserved_official_sources(self):
        text = SCRIPT.read_text(encoding="utf-8")

        # Four acquisition targets only: Commission final report, two staff
        # monographs, and the CIA OIG accountability review.
        self.assertEqual(text.count('run_one "'), 4)

        self.assertIn("GPO-911REPORT.pdf", text)
        self.assertIn("GOVPUB-Y3-PURL-LPS53198.pdf", text)
        self.assertIn("GOVPUB-Y3-PURL-LPS53197.pdf", text)
        self.assertIn("DOC_0006184107.pdf", text)

        # Do not regress to the fragile archived Commission artifact URLs.
        self.assertNotIn("www.9-11commission.gov/report/911Report_Ch7.pdf", text)
        self.assertNotIn("www.9-11commission.gov/staff_statements/911_TerrFin_Monograph.pdf", text)
        self.assertNotIn("www.9-11commission.gov/staff_statements/911_TerrTrav_Monograph.pdf", text)

        # Sprint must end with corpus verification and a source-dependency gate.
        self.assertIn('blackindex.py" --root "$ROOT" verify', text)
        self.assertIn("STOP GATE", text)
        self.assertIn("not evidence gaps", text)

        # The operator should not have to copy verifier output back manually.
        # A durable status-only run report is generated and pushed after each
        # document's normal metadata/extraction publication.
        self.assertIn("docs/run-reports/2026-08-27-911-official-closeout.md", text)
        self.assertIn("BLACKINDEX_SPRINT_VERIFY_JSON", text)
        self.assertIn("Verifier checked", text)
        self.assertIn("CALL-911-OFFICIAL-CLOSEOUT", text)
        self.assertIn("record 9/11 official closeout sprint result", text)
        self.assertIn("pre-existing staged changes detected", text)

        # Keep UI generation on the same current path, including embedded favicon.
        self.assertIn("inject-record-context.py", text)
        self.assertIn("inject-research-session.py", text)
        self.assertIn("inject-research-export.py", text)
        self.assertIn("inject-favicon.py", text)


if __name__ == "__main__":
    unittest.main()
