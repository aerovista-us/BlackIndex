import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "blackindex.py"
spec = importlib.util.spec_from_file_location("blackindex", MODULE_PATH)
blackindex = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(blackindex)


def intake_args(**overrides):
    values = dict(
        root="",
        file="",
        source="CIA",
        collection="Test",
        year="1973",
        title="Sample",
        document_date=None,
        url=None,
        artifact_url=None,
        landing_url=None,
        native_id=None,
        record_group=None,
        series=None,
        call_id="CALL-TEST",
        tags="",
        classification_note=None,
        redaction_note=None,
    )
    values.update(overrides)
    return Namespace(**values)


class BlackIndexTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(blackindex.slugify("Family Jewels"), "family-jewels")
        self.assertEqual(blackindex.slugify("  JFK / Records  "), "jfk-records")

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "a.txt"
            path.write_text("blackindex", encoding="utf-8")
            self.assertEqual(
                blackindex.sha256_file(path),
                "c2958c5442b70061ac0fdf6f00ea043cbb09f4633b45f31336e01a36b4d155dd",
            )

    def test_intake_and_duplicate_detection(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            source = Path(td) / "sample.txt"
            source.write_text("primary source bytes", encoding="utf-8")

            args = intake_args(
                root=str(root),
                file=str(source),
                source="CIA",
                collection="Family Jewels",
                year="1973",
                title="Sample",
                document_date="1973-01-01",
                url="https://example.test/source",
                call_id="CALL-003",
                tags="oversight,governance",
            )

            self.assertEqual(blackindex.cmd_intake(args), 0)
            metadata_path = root / "metadata" / "CIA-1973-family-jewels-001.json"
            self.assertTrue(metadata_path.exists())
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(data["call_id"], "CALL-003")
            self.assertEqual(data["evidence_status"], "unreviewed")
            self.assertEqual(data["artifact_url"], "https://example.test/source")
            self.assertTrue(Path(data["local_raw_path"]).exists())
            self.assertEqual(blackindex.cmd_intake(args), 3)

    def test_verify_detects_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            source = Path(td) / "sample.txt"
            source.write_text("original", encoding="utf-8")
            args = intake_args(
                root=str(root), file=str(source), source="NARA", collection="Test",
                year="1970", title="Test", document_date=None,
            )
            self.assertEqual(blackindex.cmd_intake(args), 0)
            data = json.loads(next((root / "metadata").glob("*.json")).read_text(encoding="utf-8"))
            raw = Path(data["local_raw_path"])
            raw.chmod(0o644)
            raw.write_text("tampered", encoding="utf-8")
            verify_args = Namespace(root=str(root))
            self.assertEqual(blackindex.cmd_verify(verify_args), 1)


if __name__ == "__main__":
    unittest.main()
