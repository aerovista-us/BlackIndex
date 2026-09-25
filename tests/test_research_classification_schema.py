import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_schema_includes_research_classification_states():
    schema = json.loads((ROOT / "objects" / "schema-v1.json").read_text())
    assert "research_classification" in schema["properties"]["object_type"]["enum"]
    block = next(x for x in schema["allOf"] if x.get("if", {}).get("properties", {}).get("object_type", {}).get("const") == "research_classification")
    states = set(block["then"]["properties"]["canonical_status"]["enum"])
    assert states == {"canon", "field_note", "apocrypha", "pseudepigrapha", "deuterocanon", "fragment", "rejected", "superseded"}


def test_classification_keeps_authenticity_and_attribution_separate():
    schema = json.loads((ROOT / "objects" / "schema-v1.json").read_text())
    block = next(x for x in schema["allOf"] if x.get("if", {}).get("properties", {}).get("object_type", {}).get("const") == "research_classification")
    props = block["then"]["properties"]
    assert "authenticity_status" in props
    assert "attribution_status" in props
    assert "promotion_history" in props
