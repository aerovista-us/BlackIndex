from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "ingest-phase2-nc3-program-genealogy.sh"

class NC3ProgramGenealogyIngestTests(unittest.TestCase):
    def test_runner_is_bounded_to_two_public_program_records(self):
        text = RUNNER.read_text()
        self.assertEqual(text.count("CALL-NC3-PROGRAM-GENEALOGY-001"), 2)
        self.assertIn("FY2026_r1.pdf", text)
        self.assertIn("RDTEN_BA1-3_Book.pdf", text)

    def test_scope_stays_program_level(self):
        text = RUNNER.read_text()
        self.assertIn("program/funding lineage", text)
        self.assertNotIn("ocr", text.lower())
        self.assertNotIn("promote", text.lower())

if __name__ == "__main__":
    unittest.main()
