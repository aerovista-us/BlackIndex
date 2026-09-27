import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "objects/research_classifications/RC-LOOKING-GLASS-afgsci13-5302v2-directive.json"
ME = ROOT / "objects/missing_evidence/ME-LOOKING-GLASS-2017-alcs-authority-source-family.json"
META = ROOT / "metadata/USAF-2017-air-force-global-strike-command-instructions-001.json"


class LookingGlassAfgsciObjectTests(unittest.TestCase):
    def test_directive_is_document_canon_not_imported_authority(self):
        rc = json.loads(RC.read_text(encoding="utf-8"))
        self.assertEqual(rc["subject_type"], "document")
        self.assertEqual(rc["canonical_status"], "canon")
        self.assertTrue(rc["review_required"])
        self.assertIn("does not import", rc["reason"])

    def test_authority_source_family_remains_unresolved(self):
        me = json.loads(ME.read_text(encoding="utf-8"))
        self.assertEqual(me["status"], "unresolved")
        self.assertIn("AFGSCI 13-5302V4", "\n".join(me["named_records"]))
        self.assertIn("STRATCOM Directive 501-1", "\n".join(me["named_records"]))
