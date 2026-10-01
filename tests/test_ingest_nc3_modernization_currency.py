from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "ingest-phase2-nc3-modernization-currency.sh"

class NC3ModernizationCurrencyIngestTests(unittest.TestCase):
    def test_runner_is_bounded_to_three_public_records(self):
        text = RUNNER.read_text()
        self.assertEqual(text.count("CALL-NC3-MODERNIZATION-CURRENCY-001"), 3)
        self.assertIn("2022-NUCLEAR-POSTURE-REVIEW.PDF", text)
        self.assertIn("2025%20USSTRATCOM%20Congressional%20Posture%20Statement.pdf", text)
        self.assertIn("2026%20USSTRATCOM%20Congressional%20Posture%20Statement.pdf", text)

    def test_runner_preserves_scope_guardrails(self):
        text = RUNNER.read_text()
        self.assertIn("institutional version layers", text)
        self.assertNotIn("ocr", text.lower())
        self.assertNotIn("promote", text.lower())

if __name__ == "__main__":
    unittest.main()
