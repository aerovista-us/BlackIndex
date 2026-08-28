import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "map-911-recovery-to-segments.py"
spec = importlib.util.spec_from_file_location("map_911_recovery_to_segments", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class RecoveryToSegmentsTests(unittest.TestCase):
    def test_maps_eo14040_position_to_segment_and_p0_packet(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "local/index/segmentation").mkdir(parents=True)
            (root / "local/index/triage").mkdir(parents=True)
            (root / "local/review/911-fbi-p0").mkdir(parents=True)

            recovery = {
                "targets": [{
                    "target_id": "BENOMRANE",
                    "label": "Benomrane interviews",
                    "candidates": [
                        {"doc_id": "COMMISSION-2004-9-11-commission-001", "text_page_index": 533},
                        {"doc_id": "FBI-2021-eo14040-2-b-i-001", "container_sha256": "abc", "text_page_index": 173},
                    ],
                }]
            }
            (root / "local/index/911-named-source-recovery.json").write_text(json.dumps(recovery), encoding="utf-8")

            segmentation = {
                "candidates": [{
                    "candidate_id": "CAND-0020",
                    "start_page": 170,
                    "end_page": 176,
                    "record_type_guess": "fd_302",
                    "entity_hits": ["Fahad al-Thumairy"],
                    "date_hits": ["03/07/2002"],
                    "serial_or_case_hits": ["123-ABC"],
                }]
            }
            (root / "local/index/segmentation/FBI-2021-eo14040-2-b-i-001.json").write_text(json.dumps(segmentation), encoding="utf-8")

            triage = {"all_candidates": [{
                "container_doc_id": "FBI-2021-eo14040-2-b-i-001",
                "candidate_id": "CAND-0020",
                "review_priority_band": "P0",
                "review_priority_score": 9,
            }]}
            (root / "local/index/triage/911-fbi-segmentation-priority.json").write_text(json.dumps(triage), encoding="utf-8")

            manifest = {"packets": [{
                "container_doc_id": "FBI-2021-eo14040-2-b-i-001",
                "candidate_id": "CAND-0020",
                "packet": "/tmp/packet.md",
                "promotion_state": "review_required",
            }]}
            (root / "local/review/911-fbi-p0/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            report = mod.map_recovery(root)
            self.assertEqual(report["target_family_count"], 1)
            self.assertEqual(report["candidate_position_count"], 1)
            self.assertEqual(report["positions_with_segment_match"], 1)
            pos = report["targets"][0]["eo14040_candidate_positions"][0]
            self.assertEqual(pos["parent_doc_id"], "FBI-2021-eo14040-2-b-i-001")
            self.assertEqual(pos["segment_match_count"], 1)
            seg = pos["segments"][0]
            self.assertEqual(seg["candidate_id"], "CAND-0020")
            self.assertEqual(seg["priority_band"], "P0")
            self.assertEqual(seg["p0_packet"], "/tmp/packet.md")
            self.assertFalse(seg["boundary_verified"])
            self.assertFalse(seg["physical_page_verified"])
            self.assertFalse(report["physical_page_claim"])
            self.assertFalse(report["boundary_claim"])

    def test_commission_only_hits_are_not_mapped_as_underlying_container_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "local/index").mkdir(parents=True)
            recovery = {
                "targets": [{
                    "target_id": "ABDULLAH",
                    "label": "Abdullah",
                    "candidates": [{"doc_id": "COMMISSION-2004-9-11-commission-001", "text_page_index": 533}],
                }]
            }
            (root / "local/index/911-named-source-recovery.json").write_text(json.dumps(recovery), encoding="utf-8")
            report = mod.map_recovery(root)
            self.assertEqual(report["target_family_count"], 0)
            self.assertEqual(report["candidate_position_count"], 0)


if __name__ == "__main__":
    unittest.main()
