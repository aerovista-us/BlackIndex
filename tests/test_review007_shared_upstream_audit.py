import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_review007_shared_upstream_audit_is_green():
    proc=subprocess.run([sys.executable,str(ROOT/'tools'/'audit-review-007-shared-upstream.py'),'--root',str(ROOT)],capture_output=True,text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data=json.loads(proc.stdout)
    assert data['ok'] is True
    assert data['source_dependencies_checked'] == 14
    assert data['classifications_checked'] == 4
    assert data['comparisons_checked'] == 2
    assert data['independent_high_risk_edges'] == 0
