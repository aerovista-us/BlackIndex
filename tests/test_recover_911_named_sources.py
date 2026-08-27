import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "recover-911-named-sources.py"
spec = importlib.util.spec_from_file_location("recover_911_named_sources", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class NamedSourceRecoveryTests(unittest.TestCase):
    def test_finds_candidate_but_never_claims_physical_page(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "metadata").mkdir()
            (root / "normalized" / "text").mkdir(parents=True)

            text_path = root / "normalized" / "text" / "FBI-TEST-001.txt"
            text_path.write_text(
                "cover page\f"
                "FEDERAL BUREAU OF INVESTIGATION\n"
                "ELECTRONIC COMMUNICATION\n"
                "SUBJECT: Fahad Al-Thumairy\n"
                "DATE: November 20, 2002\n"
                "telephone analysis follows\n",
                encoding="utf-8",
            )
            metadata = {
                "schema_version": 1,
                "doc_id": "FBI-TEST-001",
                "source": "FBI",
                "sha256": "abc123",
                "normalized_text_path": str(text_path),
            }
            (root / "metadata" / "legacy name.json").write_text(json.dumps(metadata), encoding="utf-8")

            report = mod.scan_root(root)
            target = next(x for x in report["targets"] if x["target_id"] == "THUMAIRY-EC-2002-11-20")
            self.assertEqual(target["candidate_count"], 1)
            candidate = target["candidates"][0]
            self.assertEqual(candidate["doc_id"], "FBI-TEST-001")
            self.assertEqual(candidate["text_page_index"], 2)
            self.assertIsNone(candidate["physical_page_index"])
            self.assertFalse(candidate["physical_page_verified"])
            self.assertFalse(report["physical_page_claim"])

            rendered = mod.render_markdown(report)
            self.assertIn("physical page **unverified**", rendered)
            self.assertIn("not** a verified physical PDF page", rendered)

    def test_requires_all_signature_components(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "metadata").mkdir()
            (root / "normalized" / "text").mkdir(parents=True)
            text_path = root / "normalized" / "text" / "FBI-TEST-002.txt"
            text_path.write_text("Fahad Al-Thumairy appears here, but no target date.", encoding="utf-8")
            (root / "metadata" / "record.json").write_text(json.dumps({
                "schema_version": 1,
                "doc_id": "FBI-TEST-002",
                "source": "FBI",
                "sha256": "def456",
                "normalized_text_path": str(text_path),
            }), encoding="utf-8")

            report = mod.scan_root(root)
            target = next(x for x in report["targets"] if x["target_id"] == "THUMAIRY-EC-2002-11-20")
            self.assertEqual(target["candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
