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

    def test_source_token_is_path_safe(self):
        self.assertEqual(blackindex.source_token("CIA"), "CIA")
        self.assertEqual(blackindex.source_token("US Congress"), "US_CONGRESS")
        self.assertEqual(blackindex.source_token("9/11 Commission"), "9_11_COMMISSION")
        self.assertNotIn("/", blackindex.source_token("9/11 Commission"))

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

    def test_path_bearing_source_label_cannot_escape_generated_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            source = Path(td) / "sample.txt"
            source.write_text("staff monograph bytes", encoding="utf-8")
            args = intake_args(
                root=str(root), file=str(source), source="9/11 Commission",
                collection="Staff Monographs", year="2004", title="Sample",
            )
            self.assertEqual(blackindex.cmd_intake(args), 0)
            metadata = next((root / "metadata").glob("*.json"))
            self.assertEqual(metadata.name, "9_11_COMMISSION-2004-staff-monographs-001.json")
            data = json.loads(metadata.read_text(encoding="utf-8"))
            raw = Path(data["local_raw_path"])
            self.assertEqual(raw.parent.name, "staff-monographs")
            self.assertEqual(raw.parent.parent.name, "9-11-commission")
            self.assertEqual(raw.name, "9_11_COMMISSION-2004-staff-monographs-001.txt")

    def test_legacy_space_bearing_metadata_stays_enumerable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            blackindex.ensure_layout(root)
            legacy = root / "metadata" / "US CONGRESS-2002-9-11-joint-inquiry-001.json"
            legacy.write_text(json.dumps({
                "doc_id": "US CONGRESS-2002-9-11-joint-inquiry-001",
                "sha256": "abc",
            }), encoding="utf-8")
            support = root / "metadata" / "schema-v1.json"
            support.write_text(json.dumps({"schema_version": 1}), encoding="utf-8")
            self.assertEqual([p.name for p in blackindex.metadata_files(root)], [legacy.name])

    def test_orphan_raw_sequence_is_reserved(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            blackindex.ensure_layout(root)
            raw_dir = blackindex.raw_collection_dir(root, "COMMISSION", "Staff Monographs")
            raw_dir.mkdir(parents=True, exist_ok=True)
            orphan = raw_dir / "COMMISSION-2004-staff-monographs-001.pdf"
            orphan.write_bytes(b"%PDF-orphan")
            self.assertEqual(
                blackindex.make_doc_id(root, "COMMISSION", "2004", "Staff Monographs"),
                "COMMISSION-2004-staff-monographs-002",
            )

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
