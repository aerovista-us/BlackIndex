import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-looking-glass-afpd13-5-afi13-520.sh"


class LookingGlassAuthorityFamilyIngestTests(unittest.TestCase):
    def test_runner_is_bounded_and_first_party(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertEqual(text.count("run_ingest \\\n"), 2)
        self.assertIn("static.e-publishing.af.mil", text)
        self.assertIn("AFPD13-5", text)
        self.assertIn("AFI13-520", text)
        self.assertNotIn("AFI13-530.pdf", text)

    def test_runner_preserves_supersession_limit(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("AFI13-530 remains a superseded historical source target", text)
        self.assertIn("do not treat AFI13-520 as a byte/content substitute", text)
        self.assertIn('python3 "$ROOT/tools/blackindex.py" --root "$ROOT" verify', text)


if __name__ == "__main__":
    unittest.main()
