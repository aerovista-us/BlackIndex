from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/run-review-007c-cia-oig-exec-summary.sh"


def test_exec_summary_checkpoint_is_official_and_bounded():
    src = SCRIPT.read_text(encoding="utf-8")
    assert "https://purl.fdlp.gov/GPO/LPS93679" in src
    assert '--source "CIA"' in src
    assert '--native-id "GPO-LPS93679"' in src
    assert "CALL-911-CIA-OIG-EXEC-SUMMARY" in src
    assert "--publish" in src
    assert "Third-party source substitution" in src
    assert "OCR performed by this checkpoint" in src
    assert "No OCR, evidence-state mutation, or historical conclusion" in src


def test_exec_summary_failure_is_recorded_as_acquisition_gap():
    src = SCRIPT.read_text(encoding="utf-8")
    assert 'ACQ_STATUS="ACQUISITION_GAP"' in src
    assert "no third-party substitution will be attempted" in src
    assert "Acquisition failure is an acquisition gap" in src
    assert "exit 0" in src


def test_checkpoint_reconciles_single_living_ledger():
    src = SCRIPT.read_text(encoding="utf-8")
    assert "reconcile-review-007-ledger.py" in src
    assert "BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md" in src
    assert "git -C \"$ROOT\" add -- \"$REPORT\" \"$ROOT/docs/BLACKINDEX_MASTER_STATUS_AND_BACKLOG.md\"" in src
