import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-nc3-governance-baseline.sh"


class NC3GovernanceBaselineTests(unittest.TestCase):
    def test_runner_is_bounded_to_four_first_party_records(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertEqual(text.count("--call-id CALL-NC3-GOVERNANCE-001"), 4)
        self.assertIn("374101p.pdf", text)
        self.assertIn("370001p.pdf", text)
        self.assertIn("5119_01.pdf", text)
        self.assertIn("S-373001_placeholder.pdf", text)

    def test_controlled_instruction_is_not_misrepresented(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Public Placeholder", text)
        self.assertIn("access-boundary", text)
        self.assertIn("not the controlled instruction contents", text)

    def test_runner_verifies_corpus(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('blackindex.py\" --root \"$ROOT\" verify', text)


if __name__ == "__main__":
    unittest.main()
