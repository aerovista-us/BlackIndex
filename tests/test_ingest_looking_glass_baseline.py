import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-looking-glass-baseline.sh"


class LookingGlassBaselineTests(unittest.TestCase):
    def test_baseline_is_exactly_two_official_usaf_histories(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("SAC%20Alert%20Operations%20Lo-Res.pdf", text)
        self.assertIn("https://media.defense.gov/", text)
        self.assertEqual(text.count('run_one "'), 2)
        self.assertEqual(text.count('--source "USAF"'), 2)
        self.assertEqual(text.count('--publish'), 2)
        self.assertIn("CALL-LOOKING-GLASS-OFFICIAL-BASELINE", text)

    def test_baseline_preserves_source_class_limits(self):
        text = SCRIPT.read_text(encoding="utf-8").lower()
        self.assertIn("not an operational order or nuclear-use authority", text)
        self.assertIn("must not be counted as independent corroboration", text)
        self.assertIn("no claim is made", text)
        self.assertNotIn("tesseract", text)
        self.assertNotIn("ocrmypdf", text)
        self.assertNotIn("promote-candidate", text)
        self.assertNotIn("--apply", text)

    def test_baseline_fails_closed_on_acquisition_or_verify_failure(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('if [[ "$VERIFY_RC" -ne 0 ]]', text)
        self.assertIn("if (( SUCCEEDED != 2 ))", text)
        self.assertIn("exit 5", text)


if __name__ == "__main__":
    unittest.main()
