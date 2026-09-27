import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "objects" / "research_classifications"
SD = ROOT / "objects" / "source_dependencies"
ME = ROOT / "objects" / "missing_evidence"


class NC3GovernanceObjectTests(unittest.TestCase):
    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_public_and_placeholder_documents_are_canon_with_bounded_scope(self):
        names = [
            "RC-NC3-dodi3741-public-governance.json",
            "RC-NC3-dodd3700-public-governance.json",
            "RC-NC3-cjcsi5119-public-charter.json",
            "RC-NC3-s373001-placeholder.json",
            "RC-NC3-s371001-placeholder.json",
            "RC-NC3-s521081-placeholder.json",
        ]
        docs = [self.load(RC / name) for name in names]
        self.assertTrue(all(d["canonical_status"] == "canon" for d in docs))
        self.assertTrue(all(d["provenance_status"] == "mapped" for d in docs))
    def test_placeholder_scope_does_not_import_controlled_contents(self):
        for name in [
            "RC-NC3-s373001-placeholder.json",
            "RC-NC3-s371001-placeholder.json",
            "RC-NC3-s521081-placeholder.json",
        ]:
            d = self.load(RC / name)
            self.assertIn("placeholder", d["reason"].lower())
            self.assertIn("controlled", d["reason"].lower())
            self.assertIn("access-boundary", d["corroboration_status"])

    def test_public_layers_are_dependent_on_controlled_parents(self):
        a = self.load(SD / "SD-NC3-dodi3741-to-dodd-s371001.json")
        b = self.load(SD / "SD-NC3-dodd3700-to-controlled-governance-parents.json")
        self.assertEqual(a["independence"], "dependent")
        self.assertEqual(b["independence"], "dependent")
        self.assertIn("S-3710.01", a["depends_on"])
        self.assertIn("S-5210.81", b["depends_on"])

    def test_missing_evidence_keeps_access_state_explicit(self):
        d = self.load(ME / "ME-NC3-controlled-governance-family.json")
        self.assertEqual(d["status"], "unresolved")
        self.assertIn("access/provenance", d["stated_reason_missing"])
        self.assertTrue(any(x.startswith("DoDD S-3730.02") for x in d["named_records"]))
        self.assertTrue(any(x.startswith("AFGSCMD 63-101") for x in d["named_records"]))


if __name__ == "__main__":
    unittest.main()
