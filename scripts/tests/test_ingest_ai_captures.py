"""Fixtures are synthetic test data, never real AI visibility measurements."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ingest_ai_captures import capture_to_rows, ingest

FROZEN = {"D01": ("category_discovery", "An exact immutable sample question?")}


def capture():
    return {
        "run_id": "local-pilot-001", "observed_at_utc": "2026-10-11T12:00:00Z",
        "engine": "SyntheticTestEngine/mock", "prompt_id": "D01",
        "prompt": FROZEN["D01"][1],
        "answer_text": "Synthetic answer for testing only, not observed output.",
        "labels": {brand: {
            "mentioned": False, "cited": False, "recommended": False,
            "owned_source_cited": False, "third_party_source_cited": False,
            "position": None, "source_url": "", "evidence_note": "Synthetic review"
        } for brand in ("Notion", "Asana", "ClickUp", "monday.com")},
    }


class CaptureIngestTests(unittest.TestCase):
    def test_four_brand_rows_with_provenance_digest(self):
        rows = capture_to_rows(capture(), FROZEN)
        self.assertEqual(len(rows), 4)
        self.assertTrue(rows[0]["evidence_note"].startswith("observed_at_utc:2026-10-11T12:00:00Z; sha256:"))
        self.assertEqual(rows[0]["run_date"], "2026-10-11")
        self.assertEqual(rows[0]["mentioned"], "false")

    def test_frozen_prompt_drift_rejected(self):
        item = capture()
        item["prompt"] += " modified"
        with self.assertRaisesRegex(ValueError, "frozen"):
            capture_to_rows(item, FROZEN)

    def test_missing_brand_rejected(self):
        item = capture()
        del item["labels"]["Asana"]
        with self.assertRaisesRegex(ValueError, "every benchmark"):
            capture_to_rows(item, FROZEN)

    def test_unknown_cannot_be_guessed_false(self):
        item = capture()
        for flag in ("mentioned", "cited", "recommended"):
            item["labels"]["Notion"][flag] = None
        with self.assertRaisesRegex(ValueError, "no reviewed"):
            capture_to_rows(item, FROZEN)

    def test_citation_requires_valid_url(self):
        item = capture()
        item["labels"]["Notion"]["cited"] = True
        with self.assertRaisesRegex(ValueError, "requires URL"):
            capture_to_rows(item, FROZEN)
        item["labels"]["Notion"]["source_url"] = "not a URL"
        with self.assertRaisesRegex(ValueError, "http"):
            capture_to_rows(item, FROZEN)
        item["labels"]["Notion"]["source_url"] = "https://www.notion.com/help"
        self.assertEqual(len(capture_to_rows(item, FROZEN)), 4)

    def test_unjustified_position_and_owned_source_rejected(self):
        item = capture()
        item["labels"]["Asana"]["position"] = 1
        with self.assertRaisesRegex(ValueError, "position"):
            capture_to_rows(item, FROZEN)
        item = capture()
        item["labels"]["Asana"]["owned_source_cited"] = True
        with self.assertRaisesRegex(ValueError, "requires cited"):
            capture_to_rows(item, FROZEN)

    def test_bad_timestamp_or_demo_id_rejected(self):
        item = capture()
        item["observed_at_utc"] = "2026-10-11T12:00:00+02:00"
        with self.assertRaisesRegex(ValueError, "UTC"):
            capture_to_rows(item, FROZEN)
        item = capture()
        item["run_id"] = "EXAMPLE-pilot"
        with self.assertRaisesRegex(ValueError, "Demonstration"):
            capture_to_rows(item, FROZEN)

    def test_dry_run_and_atomic_duplicate_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source, output = folder / "capture.json", folder / "observations.csv"
            source.write_text(json.dumps(capture()), encoding="utf-8")
            with patch("ingest_ai_captures.load_prompt_texts", return_value=FROZEN):
                self.assertEqual(ingest([source], output, dry_run=True), (4, 4))
                self.assertFalse(output.exists())
                self.assertEqual(ingest([source], output), (4, 4))
                snapshot = output.read_bytes()
                with self.assertRaisesRegex(ValueError, "Duplicate"):
                    ingest([source], output)
                self.assertEqual(snapshot, output.read_bytes())


    def test_reserved_and_whitespace_padded_run_ids_rejected(self):
        for run_id in ("example-1", "DEMO-first", "Sample-1", "sYntheTic_01", " EXAMPLE-bypass"):
            item = capture()
            item["run_id"] = run_id
            with self.subTest(run_id=run_id), self.assertRaises(ValueError):
                capture_to_rows(item, FROZEN)

    def test_csv_formula_identifiers_rejected(self):
        for field, value in (("run_id", "=HYPERLINK('bad','click')"),
                             ("engine", "+DDE(...)"), ("engine", "@SUM(1,1)")):
            item = capture()
            item[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "Unsafe CSV"):
                capture_to_rows(item, FROZEN)

    def test_utc_provenance_retained_in_existing_schema(self):
        rows = capture_to_rows(capture(), FROZEN)
        from analyze_ai_visibility import REQUIRED
        self.assertEqual(list(rows[0]), list(REQUIRED))
        self.assertIn("observed_at_utc:2026-10-11T12:00:00Z", rows[0]["evidence_note"])


if __name__ == "__main__":
    unittest.main()
