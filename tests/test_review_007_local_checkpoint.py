import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "run-review-007-local.sh"


class Review007LocalCheckpointTests(unittest.TestCase):
    def test_checkpoint_preserves_evidence_state_and_only_self_reports(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("recover-911-named-sources.py", text)
        self.assertIn("dependency-audit.py", text)
        self.assertIn("review-state-audit.py", text)
        self.assertIn("named-source-recovery-ui.py", text)
        self.assertIn("blackindex.py\" --root \"$ROOT\" verify", text)
        self.assertIn('"evidence_state_mutated": False', text)
        self.assertIn('"git_report_publication_requested": True', text)
        self.assertNotIn("evidence_map.py", text)

        # Git mutation is deliberately limited to the sanitized run report.
        self.assertIn("2026-08-27-review-007-named-source-recovery.md", text)
        self.assertIn('git -C "$ROOT" add -- "$REPORT"', text)
        self.assertIn('git -C "$ROOT" commit -m "BlackIndex: record Review 007 named-source recovery" -- "$REPORT"', text)
        self.assertNotIn("objects/record_integrity", text)
        self.assertNotIn("metadata/", text)
        self.assertNotIn("extractions/", text)

    def test_durable_report_is_sanitized(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("durable_report_contains_previews", text)
        self.assertIn("normalized-text previews", text)
        self.assertIn("Parent document", text)
        self.assertIn("Text-page index", text)
        self.assertIn("Parent SHA-256", text)

        # Full local recovery JSON may contain previews, but the durable report
        # generator must not serialize candidate preview text into Git.
        report_generator = text.split("# Durable report is intentionally sanitized.", 1)[1]
        report_generator = report_generator.split("PY\n", 1)[0]
        self.assertNotIn("cand.get('preview')", report_generator)

    def test_checkpoint_preserves_physical_page_warning(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('"physical_page_claim": False', text)
        self.assertIn("does not promote records", text)
        self.assertIn("not proof that the record is absent", text)
        self.assertIn("Physical page: `UNVERIFIED`", text)

    def test_pre_staged_changes_fail_safe(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('PRESTAGED="$(git -C "$ROOT" diff --cached --name-only)"', text)
        self.assertIn("pre-existing staged changes detected", text)
        self.assertIn("leaving Review 007 run report uncommitted", text)


if __name__ == "__main__":
    unittest.main()
