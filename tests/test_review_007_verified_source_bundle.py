import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "build-review-007-verified-source-bundle.py"
spec = importlib.util.spec_from_file_location("review_007_verified_source_bundle", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class Review007VerifiedSourceBundleTests(unittest.TestCase):
    def test_build_targets_is_narrow_and_boundary_neutral(self):
        segment_map = {
            "targets": [
                {
                    "target_id": "BIN-DON-DYSON-SOURCE-VERSIONS",
                    "eo14040_candidate_positions": [
                        {
                            "parent_doc_id": "FBI-2022-eo14040-2-c-001",
                            "segments": [
                                {"candidate_id": "CAND-0005", "start_page": 58, "end_page": 63},
                                {"candidate_id": "CAND-0013", "start_page": 116, "end_page": 122},
                            ],
                        }
                    ],
                },
                {
                    "target_id": "BENOMRANE-INTERVIEWS-2002",
                    "eo14040_candidate_positions": [
                        {"parent_doc_id": "FBI-2021-eo14040-2-b-i-001", "text_page_index": 173, "segments": []},
                        {"parent_doc_id": "FBI-2021-eo14040-2-b-i-001", "text_page_index": 175, "segments": []},
                    ],
                },
            ]
        }
        targets = mod.build_targets(segment_map)
        by_id = {x["target_id"]: x for x in targets}
        self.assertEqual(set(by_id), {"CAND-0005", "CAND-0013", "BENOMRANE-GAP-WINDOW"})
        self.assertEqual((by_id["CAND-0005"]["start"], by_id["CAND-0005"]["end"]), (58, 63))
        self.assertEqual((by_id["CAND-0013"]["start"], by_id["CAND-0013"]["end"]), (116, 122))
        self.assertEqual((by_id["BENOMRANE-GAP-WINDOW"]["start"], by_id["BENOMRANE-GAP-WINDOW"]["end"]), (171, 177))
        self.assertFalse(any(x["boundary_claim"] for x in targets))

    def test_full_range_requires_every_page_exact_same_index(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            normalized = root / "normalized.txt"
            normalized.write_text("page one\fpage two\fpage three", encoding="utf-8")
            pages = {1: "page one", 2: "page two", 3: "page three"}
            with mock.patch.object(mod, "physical_page_text", side_effect=lambda _exe, _pdf, page: pages[page]):
                result = mod.verify_same_index_range("pdftotext", root / "fake.pdf", normalized, 1, 3)
            self.assertTrue(result["all_pages_verified"])
            self.assertEqual(result["verified_count"], 3)

            pages[2] = "different"
            with mock.patch.object(mod, "physical_page_text", side_effect=lambda _exe, _pdf, page: pages[page]):
                result = mod.verify_same_index_range("pdftotext", root / "fake.pdf", normalized, 1, 3)
            self.assertFalse(result["all_pages_verified"])
            self.assertEqual(result["verified_count"], 2)

    def test_wrapper_publishes_only_sanitized_report(self):
        wrapper = (Path(__file__).resolve().parents[1] / "tools" / "run-review-007-verified-source-bundle.sh").read_text(encoding="utf-8")
        self.assertIn("Source PDF bytes published to Git", wrapper)
        self.assertIn("git -C \"$ROOT\" add -- \"$REPORT\"", wrapper)
        self.assertNotIn("git -C \"$ROOT\" add -- \"$MANIFEST\"", wrapper)
        self.assertIn("No evidence-state mutation, boundary claim, or record promotion", wrapper)


if __name__ == "__main__":
    unittest.main()
