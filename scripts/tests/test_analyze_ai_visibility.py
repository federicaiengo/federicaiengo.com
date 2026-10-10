"""Tests use invented observations only; no real AI-platform results implied."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze_ai_visibility import (
    BRANDS, REQUIRED, load_frozen_prompts,
    validate_observations, score,
)

PROMPTS = {"D01": "category_discovery", "R01": "recommendation"}


def record(brand="Notion", prompt="D01", run="round1", **overrides):
    row = {
        "run_id": run, "run_date": "2026-10-09", "engine": "TestEngine",
        "prompt_id": prompt, "prompt_family": PROMPTS[prompt],
        "brand": brand, "mentioned": "false", "cited": "false",
        "recommended": "false", "position": "", "owned_source_cited": "",
        "third_party_source_cited": "", "source_url": "",
        "evidence_note": "Simulated unit test row",
    }
    row.update(overrides)
    return row


class CompetitiveVisibilityTests(unittest.TestCase):
    def validate(self, rows):
        validate_observations(rows, PROMPTS, list(REQUIRED))

    def test_balanced_four_brand_comparison(self):
        rows = [record(brand=b, mentioned="true" if b=="Notion" else "false")
                for b in BRANDS]
        self.validate(rows)
        result = score(rows)
        self.assertEqual(result["complete_four_brand_rounds"], 1)
        self.assertEqual(result["incomplete_rounds_excluded"], 0)
        self.assertEqual(result["by_brand"]["Notion"]["mention"]["percent"], 100.0)
        self.assertEqual(result["by_brand"]["Asana"]["mention"]["percent"], 0.0)
        self.assertIsNone(result["by_brand"]["Notion"]["recommendation"]["percent"])

    def test_incomplete_round_does_not_create_false_absences(self):
        result = score([record("Notion"), record("Asana")])
        self.assertEqual(result["complete_four_brand_rounds"], 0)
        self.assertEqual(result["incomplete_rounds_excluded"], 1)
        for b in BRANDS:
            self.assertIsNone(result["by_brand"][b]["mention"]["percent"])

    def test_missing_boolean_is_not_a_negative_answer(self):
        rows = [record(brand=b, mentioned="" if b=="Notion" else "false")
                for b in BRANDS]
        self.validate(rows)
        result = score(rows)
        self.assertEqual(result["by_brand"]["Notion"]["mention"]["eligible"], 0)
        self.assertIsNone(result["by_brand"]["Notion"]["mention"]["percent"])

    def test_recommendation_uses_recommendation_intent_only(self):
        rows = [record(b, prompt="R01", recommended="true" if b=="Asana" else "false",
                       position="1" if b=="Asana" else "") for b in BRANDS]
        self.validate(rows)
        r = score(rows)
        self.assertEqual(r["by_brand"]["Asana"]["recommendation"]["percent"], 100.0)
        self.assertEqual(r["by_brand"]["Asana"]["ordered_mean_position"], 1.0)

    def test_invalid_boolean_is_not_silently_scored_false(self):
        with self.assertRaises(ValueError):
            self.validate([record(mentioned="maybe")])

    def test_cited_answer_requires_actual_source_url(self):
        with self.assertRaises(ValueError):
            self.validate([record(cited="true")])

    def test_invalid_or_mismatched_prompt_rejected(self):
        with self.assertRaises(ValueError):
            self.validate([record(prompt_family="comparison")])

    def test_missing_date_or_bad_date_rejected(self):
        for invalid in ("", "9 October", "2026-13-09"):
            with self.assertRaises(ValueError):
                self.validate([record(run_date=invalid)])

    def test_example_cannot_be_used_as_real_measurement(self):
        with self.assertRaises(ValueError):
            self.validate([record(run="EXAMPLE_NOT_MEASURED")])

    def test_duplicate_round_cell_rejected(self):
        with self.assertRaises(ValueError):
            self.validate([record(), record()])

    def test_position_requires_qualified_recommendation(self):
        with self.assertRaises(ValueError):
            self.validate([record(position="1")])

    def test_wrong_header_rejected(self):
        with self.assertRaises(ValueError):
            validate_observations([record()], PROMPTS, ["run_id", "prompt_id"])

    def test_separate_dates_cannot_make_one_comparable_round(self):
        first = [record("Notion"), record("Asana")]
        second = [record("ClickUp", run_date="2026-10-10"),
                  record("monday.com", run_date="2026-10-10")]
        rows = first + second
        self.validate(rows)
        result = score(rows)
        self.assertEqual(result["complete_four_brand_rounds"], 0)
        self.assertEqual(result["incomplete_rounds_excluded"], 2)

    def test_boolean_whitespace_normalized_not_miscounted(self):
        rows = [record(brand=b, mentioned=" TRUE " if b=="Notion" else "false")
                for b in BRANDS]
        self.validate(rows)
        self.assertEqual(score(rows)["by_brand"]["Notion"]["mention"]["positive"], 1)

    def test_frozen_protocol_requires_exact_35_and_seven_families(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prompts.csv"
            families = [
                "category_discovery", "alternatives", "comparison",
                "capability", "pricing_value", "implementation",
                "recommendation",
            ]
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(("prompt_id","prompt_family","prompt","primary_measure"))
                for i, family in enumerate(families):
                    for j in range(5):
                        writer.writerow((f"{i:02d}-{j:02d}",family,
                                         f"Invented prompt {i}-{j}","mention"))
            self.assertEqual(len(load_frozen_prompts(path)), 35)


if __name__ == "__main__":
    unittest.main()
