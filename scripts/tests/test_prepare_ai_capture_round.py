"""Synthetic fixture tests only, never genuine AI observations."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prepare_ai_capture_round import BRANDS, prepare_round, read_frozen_prompts


class PrepareRoundTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.site = self.root / "public-site"
        self.site.mkdir()
        self.prompts = self.root / "frozen.csv"
        with self.prompts.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(("prompt_id", "prompt_family", "prompt", "primary_measure"))
            for i, family in enumerate(("category_discovery", "alternatives", "comparison",
                                        "capability", "pricing_value", "implementation",
                                        "recommendation")):
                for j in range(5):
                    writer.writerow((f"{i:02d}-{j}", family, f"Frozen question {i}-{j}?", "mention"))
        self.out = self.root / "private-evidence"

    def generate(self, **kwargs):
        params = dict(output_dir=self.out, run_id="oct-2026-pilot01",
                      engine="ChatGPT / model observed / search on",
                      prompt_ids=("00-0", "06-0"), repo_root=self.site,
                      prompts_file=self.prompts)
        params.update(kwargs)
        return prepare_round(**params)

    def test_private_templates_are_unobserved_and_preserve_exact_prompts(self):
        paths = self.generate()
        self.assertEqual(len(paths), 2)
        first = json.loads(paths[0].read_text(encoding="utf-8"))
        self.assertEqual(first["prompt"], "Frozen question 0-0?")
        self.assertEqual(first["capture_status"], "UNOBSERVED_TEMPLATE")
        self.assertEqual(first["answer_text"], "")
        self.assertEqual(first["observed_at_utc"], "")
        self.assertEqual(set(first["labels"]), set(BRANDS))
        self.assertTrue(all(v["mentioned"] is None and v["evidence_note"] == ""
                            for v in first["labels"].values()))

    def test_refuse_writes_inside_public_site(self):
        with self.assertRaisesRegex(ValueError, "OUTSIDE"):
            self.generate(output_dir=self.site / "data/ai-search/raw-captures")
        self.assertFalse((self.site / "data").exists())

    def test_refuse_overwrite_and_preserve_original_bytes(self):
        paths = self.generate()
        before = paths[0].read_bytes()
        with self.assertRaises(FileExistsError):
            self.generate()
        self.assertEqual(paths[0].read_bytes(), before)

    def test_reject_unknown_or_duplicate_ids_without_creating_directory(self):
        for ids in (("00-0", "missing"), ("00-0", "00-0"), ()):
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                self.generate(prompt_ids=ids)
        self.assertFalse(self.out.exists())

    def test_reject_demonstration_or_formula_runs(self):
        for run in ("example-data", "demo-abc", "test_01", "=DANGEROUS", "bad name"):
            with self.subTest(run=run), self.assertRaises(ValueError):
                self.generate(run_id=run)

    def test_mid_batch_write_failure_rolls_back_all_new_files(self):
        real_dump = json.dump
        calls = 0

        def fail_on_second(data, stream, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated write failure")
            return real_dump(data, stream, **kwargs)

        with patch("prepare_ai_capture_round.json.dump", side_effect=fail_on_second):
            with self.assertRaisesRegex(OSError, "simulated write failure"):
                self.generate()
        self.assertTrue(self.out.is_dir())
        self.assertEqual(list(self.out.iterdir()), [])

    def test_first_write_failure_leaves_no_partial_json(self):
        with patch("prepare_ai_capture_round.json.dump", side_effect=ValueError("bad serialization")):
            with self.assertRaisesRegex(ValueError, "bad serialization"):
                self.generate()
        self.assertEqual(list(self.out.iterdir()), [])

    def test_reject_uneven_intent_families(self):
        lines = self.prompts.read_text(encoding="utf-8").splitlines()
        lines[1] = lines[1].replace("category_discovery", "alternatives", 1)
        self.prompts.write_text("\n".join(lines) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "five prompts per intent"):
            self.generate()

    def test_reject_duplicate_question_and_unsafe_prompt_id(self):
        with self.prompts.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.reader(stream))
        rows[2][2] = rows[1][2]
        with self.prompts.open("w", newline="", encoding="utf-8") as stream:
            csv.writer(stream).writerows(rows)
        with self.assertRaisesRegex(ValueError, "distinct question"):
            self.generate()
        rows[2][2] = "Restored unique question?"
        rows[2][0] = "../bad"
        with self.prompts.open("w", newline="", encoding="utf-8") as stream:
            csv.writer(stream).writerows(rows)
        with self.assertRaisesRegex(ValueError, "Unsafe frozen prompt"):
            self.generate()
        self.assertFalse(self.out.exists())

    def test_reject_wrong_prompt_schema_and_count(self):
        self.prompts.write_text("prompt_id,prompt_family,prompt,primary_measure\nA,a,hi,x\n")
        with self.assertRaisesRegex(ValueError, "Expected 35"):
            read_frozen_prompts(self.prompts)


if __name__ == "__main__":
    unittest.main()
