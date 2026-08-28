from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_server_has_blackindex_health_marker():
    src = (ROOT / "tools/blackindex-ui-server.py").read_text(encoding="utf-8")
    assert '"/__blackindex_health"' in src
    assert '"service": "blackindex-dashboard"' in src
    assert '"ok": True' in src
    assert 'Cache-Control", "no-store"' in src


def test_serve_dashboard_reuses_existing_blackindex_server():
    src = (ROOT / "tools/serve-dashboard.sh").read_text(encoding="utf-8")
    assert "blackindex_health()" in src
    assert "/__blackindex_health" in src
    assert 'payload.get("service") == "blackindex-dashboard"' in src
    assert "legacy_blackindex_process()" in src
    assert "blackindex-ui-server.py" in src
    assert "Existing BlackIndex dashboard detected on port $START_PORT; reusing it." in src
    assert "exit 0" in src
    assert "find_free_port()" in src
    assert "occupied by a non-BlackIndex service" in src


def test_dashboard_is_regenerated_before_reuse_probe():
    src = (ROOT / "tools/serve-dashboard.sh").read_text(encoding="utf-8")
    generate = src.index('python3 "$ROOT/tools/evidence_map.py" --root "$ROOT" dashboard')
    probe = src.index('if ! port_is_free "$BIND" "$START_PORT"; then')
    assert generate < probe
