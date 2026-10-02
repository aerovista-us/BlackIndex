import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ai_research_test", ROOT / "tools" / "ai_research.py")
ai = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ai
assert spec.loader is not None
spec.loader.exec_module(ai)


class AiResearchTests(unittest.TestCase):
    def test_split_chunks_preserves_line_ranges(self):
        text = "\n".join(f"line {i}" for i in range(1, 21))
        chunks = ai.split_chunks(text, max_chars=35)
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0].start, 1)
        self.assertEqual(chunks[-1].end, 20)
        self.assertIn("[L1]", chunks[0].prompt_text())

    def test_rank_chunks_prefers_question_terms(self):
        chunks = [
            ai.Chunk(1, 2, "apples and oranges"),
            ai.Chunk(3, 4, "survivable airborne operations center contract award"),
            ai.Chunk(5, 6, "unrelated history"),
        ]
        ranked = ai.rank_chunks(chunks, "What does the SAOC contract award establish?", limit=1)
        self.assertEqual(ranked[0].start, 3)

    def test_locate_selection_maps_source_lines(self):
        text = "alpha\nbeta\ngamma\ndelta\n"
        c = ai.locate_selection(text, "beta\ngamma")
        self.assertEqual((c.start, c.end), (2, 3))
        self.assertEqual(c.text, "beta\ngamma")

    def test_citation_validator_rejects_out_of_range(self):
        allowed = [ai.Chunk(10, 20, "x")]
        good = ai._validate_citations("supported [L12-L14]", allowed)
        bad = ai._validate_citations("bad [L21-L22]", allowed)
        self.assertTrue(good["citation_ok"])
        self.assertFalse(bad["citation_ok"])
        self.assertEqual(bad["invalid_citations"], ["L21-L22"])


    def test_default_models_and_quick_retrieval_guardrails(self):
        self.assertEqual(ai.FAST_MODEL, "qwen2.5:1.5b")
        self.assertEqual(ai.DEEP_MODEL, "gemma4:e4b")
        text = "alpha\nSAOC contract award Sierra Nevada\nunrelated Global Hawk contract\nomega\n"
        windows = ai.retrieve_windows(text, "SAOC contract award", limit=1, radius=0)
        self.assertEqual(len(windows), 1)
        self.assertEqual((windows[0].start, windows[0].end), (2, 2))
        self.assertNotIn("Global Hawk", windows[0].text)


if __name__ == "__main__":
    unittest.main()
