import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "run-review-007-local.sh"


class Review007LocalCheckpointTests(unittest.TestCase):
    def test_checkpoint_does_not_mutate_evidence_or_promote_records(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("recover-911-named-sources.py", text)
        self.assertIn("dependency-audit.py", text)
        self.assertIn("review-state-audit.py", text)
        self.assertIn("named-source-recovery-ui.py", text)
        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn('"evidence_state_mutated": False', text)
        self.assertNotIn("evidence_map.py", text)
        self.assertNotIn("promote-911", text)

    def test_checkpoint_preserves_physical_page_warning(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"physical_page_claim": False', text)
        self.assertIn("does not promote records", text)
        self.assertIn("not proof that the record is absent", text)
        self.assertIn("Physical page: `UNVERIFIED`", text)

    def test_sanitized_report_is_the_only_git_target(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("durable_report_contains_previews", text)
        self.assertIn("git -C \"$ROOT\" add -- \"$REPORT\"", text)
        self.assertIn("git -C \"$ROOT\" commit", text)
        self.assertIn("git -C \"$ROOT\" push", text)
        self.assertIn("PRESTAGED", text)
        self.assertNotIn("git -C \"$ROOT\" add -A", text)
        self.assertNotIn("git -C \"$ROOT\" add .", text)

    def test_report_distinguishes_citation_from_underlying_container_candidates(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("EO14040_CONTAINER_CANDIDATE", text)
        self.assertIn("CITATION_OR_SYNTHESIS", text)
        self.assertIn("targets_with_eo14040_container_candidates", text)
        self.assertIn("targets_citation_or_synthesis_only", text)
        self.assertIn("A citation inside a synthesis document is not an underlying-record recovery", text)


if __name__ == "__main__":
    unittest.main()
