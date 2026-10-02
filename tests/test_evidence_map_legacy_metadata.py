import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evidence_map_legacy_test", ROOT / "tools" / "evidence_map.py"
)
evidence_map = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(evidence_map)


class EvidenceMapLegacyMetadataTests(unittest.TestCase):
    def test_legacy_space_bearing_metadata_is_included(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            md = root / "metadata"
            md.mkdir()
            legacy = md / "US CONGRESS-2002-9-11-joint-inquiry-001.json"
            legacy.write_text(
                json.dumps({
                    "doc_id": "US CONGRESS-2002-9-11-joint-inquiry-001",
                    "title": "Joint Inquiry",
                }),
                encoding="utf-8",
            )
            (md / "schema-v1.json").write_text(
                json.dumps({"schema_version": 1}),
                encoding="utf-8",
            )
            files = evidence_map.metadata_files(root)
            self.assertEqual([p.name for p in files], [legacy.name])


if __name__ == "__main__":
    unittest.main()
