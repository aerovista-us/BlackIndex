from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "ingest-phase2-nc3-governance-currency-supplement.sh"

class NC3GovernanceCurrencySupplementTests(unittest.TestCase):
    def test_single_public_placeholder_only(self):
        text = RUNNER.read_text()
        self.assertEqual(text.count("CALL-NC3-GOVERNANCE-CURRENCY-001"), 1)
        self.assertIn("S-510092_placeholder.pdf", text)
        self.assertIn("public placeholder only", text)
        self.assertNotIn("ocr", text.lower())
        self.assertNotIn("promote", text.lower())

if __name__ == "__main__":
    unittest.main()
