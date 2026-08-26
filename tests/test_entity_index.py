import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTITY_INDEX = ROOT / "tools/entity-index.py"
ENTITY_UI = ROOT / "tools/entity-ui.py"


class EntityIndexTests(unittest.TestCase):
    def test_explicit_mentions_and_genealogy_do_not_become_culpability_edges(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "metadata").mkdir()
            (root / "entities/example").mkdir(parents=True)
            doc = {
                "schema_version": 1,
                "doc_id": "TEST-2026-entity-record-001",
                "title": "Entity test record",
                "source": "TEST",
                "collection": "Entity Test",
                "sha256": "0" * 64,
                "people": ["Alex Example"],
                "organizations": ["Example Office"],
            }
            (root / "metadata/TEST-2026-entity-record-001.json").write_text(json.dumps(doc), encoding="utf-8")
            genealogy = {
                "schema_version": 1,
                "object_type": "genealogy_baseline",
                "founder": {"person_id": "example-alex-1900", "canonical_name": "Alex Example", "birth_year": 1900},
                "five_branches": [
                    {"person_id": "example-sam-1930", "canonical_name": "Sam Example", "parent_id": "example-alex-1900"}
                ],
                "rules": {"no_inherited_guilt": True, "no_surname_only_identity_linkage": True},
            }
            (root / "entities/example/genealogy-baseline.json").write_text(json.dumps(genealogy), encoding="utf-8")

            p = subprocess.run([sys.executable, str(ENTITY_INDEX), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            data = json.loads((root / "local/index/entity-index.json").read_text(encoding="utf-8"))
            self.assertFalse(data["rules"]["association_implies_culpability"])
            self.assertFalse(data["rules"]["surname_only_matching"])
            edge_types = {e["edge_type"] for e in data["edges"]}
            self.assertEqual(edge_types, {"document_mentions_entity", "genealogy_parent_child"})
            self.assertFalse(any("culp" in e["edge_type"].lower() or "alleg" in e["edge_type"].lower() for e in data["edges"]))

            # Metadata mention and curated genealogy identity remain separate IDs unless explicitly resolved later.
            ids = {e["entity_id"] for e in data["entities"]}
            self.assertIn("person:alex-example", ids)
            self.assertIn("person:example-alex-1900", ids)

            q = subprocess.run([sys.executable, str(ENTITY_UI), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(q.returncode, 0, q.stdout + q.stderr)
            page = (root / "local/dashboard/entities.html").read_text(encoding="utf-8")
            self.assertIn("Association is not culpability", page)
            self.assertIn("Alex Example", page)
            self.assertIn("genealogy_parent_child", page)


if __name__ == "__main__":
    unittest.main()
