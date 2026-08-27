import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "run-review-007-local.sh"


class Review007LocalCheckpointTests(unittest.TestCase):
    def test_checkpoint_is_read_only_with_respect_to_evidence_and_git(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("recover-911-named-sources.py", text)
        self.assertIn("dependency-audit.py", text)
        self.assertIn("review-state-audit.py", text)
        self.assertIn("named-source-recovery-ui.py", text)
        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn('"evidence_state_mutated": False', text)
        self.assertIn('"git_mutation_performed": False', text)
        self.assertNotIn("git -C", text)
        self.assertNotIn("evidence_map.py", text)
        self.assertNotIn("promote", text.lower().split("python3 -", 1)[0])

    def test_checkpoint_preserves_physical_page_warning(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"physical_page_claim": False', text)
        self.assertIn("does not promote records", text)
        self.assertIn("not proof that the record is absent", text)


if __name__ == "__main__":
    unittest.main()
