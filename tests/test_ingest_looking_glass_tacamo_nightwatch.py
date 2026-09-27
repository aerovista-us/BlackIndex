import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-looking-glass-tacamo-nightwatch-baseline.sh"


class LookingGlassTacamoNightwatchIngestTests(unittest.TestCase):
    def test_runner_is_three_first_party_documents(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertEqual(text.count("run_ingest \\\n"), 3)
        self.assertIn("www.stratcom.mil", text)
        self.assertIn("media.defense.gov", text)
        self.assertIn("static.e-publishing.af.mil", text)
        self.assertIn("2024-USSTRATCOM-SASC-POSTURE", text)
        self.assertIn("NPG17", text)
        self.assertIn("AFMAN11-2E-4BV3", text)

    def test_runner_keeps_analysis_scope_bounded(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("mission/command-source records only", text)
        self.assertIn('python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify', text)


if __name__ == "__main__":
    unittest.main()
