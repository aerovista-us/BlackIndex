import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "ingest-phase2-911-official-closeout-resume.sh"


class Official911CloseoutResumeTests(unittest.TestCase):
    def test_resume_is_two_document_collision_safe_recovery(self):
        text = SCRIPT.read_text(encoding="utf-8")

        self.assertEqual(text.count('run_one "'), 2)
        self.assertIn("GOVPUB-Y3-PURL-LPS53198.pdf", text)
        self.assertIn("GOVPUB-Y3-PURL-LPS53197.pdf", text)

        # The failed run used one shared collection namespace for both sources.
        # Recovery must keep separate canonical namespaces so immutable raw
        # artifacts can never collide on the same generated document ID.
        self.assertIn('9/11 Commission Terrorist Financing Staff Monograph', text)
        self.assertIn('9/11 Commission Terrorist Travel Staff Monograph', text)
        self.assertNotIn('--collection "9/11 Commission Staff Monographs"', text)

        # Never "solve" the collision by deleting or overwriting raw evidence.
        self.assertNotIn("rm -f", text)
        self.assertNotIn("chmod +w", text)
        self.assertNotIn("source-vault/raw", text.split("run_one", 1)[0])

        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn("official-closeout-resume.md", text)
        self.assertIn("Recovery note", text)
        self.assertIn("STOP GATE", text)
        self.assertIn("Do not open a new corpus cluster yet", text)

        # Metadata/extractions publish per document; the recovery run report is
        # separately durable. Record-integrity state is not blindly staged.
        self.assertIn("--publish", text)
        self.assertIn('git -C "$ROOT" add -- "$REPORT"', text)
        self.assertNotIn('git -C "$ROOT" add -- objects/record_integrity', text)


if __name__ == "__main__":
    unittest.main()
