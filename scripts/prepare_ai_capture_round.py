"""Create unobserved, local-only templates for the frozen AI Search pilot.

No AI queries are made and no experimental results are fabricated. Outputs must
be outside the public website repository; fill them from actual model answers.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "data/ai-search/competitive-prompts-v1.csv"
DEFAULT_IDS = ("D01", "U01", "P01", "R01")
BRANDS = ("Notion", "Asana", "ClickUp", "monday.com")
RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")


def read_frozen_prompts(source: Path) -> dict[str, str]:
    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["prompt_id", "prompt_family", "prompt", "primary_measure"]:
            raise ValueError("Unexpected frozen prompt schema")
        rows = list(reader)
    prompts = {row["prompt_id"]: row["prompt"] for row in rows}
    if len(rows) != 35 or len(prompts) != 35 or len({row["prompt_family"] for row in rows}) != 7:
        raise ValueError("Expected 35 unique prompts in seven intent families")
    if any(not p.strip() for p in prompts.values()):
        raise ValueError("Missing frozen prompt text")
    return prompts


def prepare_round(output_dir: Path, run_id: str, engine: str,
                  prompt_ids: tuple[str, ...] = DEFAULT_IDS,
                  *, repo_root: Path = ROOT, prompts_file: Path = PROMPTS) -> list[Path]:
    """Write one non-scoreable template per selected prompt, never overwrite."""
    if not RUN_ID.fullmatch(run_id) or run_id.lower().startswith(
        ("example", "demo", "test", "sample", "synthetic")
    ):
        raise ValueError("Use a unique, non-demonstration ASCII run ID")
    if not engine.strip() or engine != engine.strip() or engine.startswith(("=", "+", "-", "@")):
        raise ValueError("Provide the exact nonempty engine/model configuration")
    output = output_dir.expanduser().resolve()
    repository = repo_root.resolve()
    if output == repository or output.is_relative_to(repository):
        raise ValueError("Keep raw AI captures OUTSIDE the public repository")
    frozen = read_frozen_prompts(prompts_file)
    if not prompt_ids or len(prompt_ids) != len(set(prompt_ids)):
        raise ValueError("Select distinct frozen prompt IDs")
    if any(pid not in frozen for pid in prompt_ids):
        raise ValueError("Unknown frozen prompt ID")
    paths = [output / f"{run_id}__{pid}.json" for pid in prompt_ids]
    if any(path.exists() for path in paths):
        raise FileExistsError("Capture template exists; do not overwrite evidence")
    output.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    try:
        for pid, path in zip(prompt_ids, paths):
            data = {
                "capture_status": "UNOBSERVED_TEMPLATE",
                "run_id": run_id, "observed_at_utc": "", "engine": engine,
                "prompt_id": pid, "prompt": frozen[pid], "answer_text": "",
                "collection_context": {
                    "country": "", "language": "", "search_mode": "",
                    "personalization": "", "model_version": ""
                },
                "labels": {brand: {
                    "mentioned": None, "cited": None, "recommended": None,
                    "owned_source_cited": None, "third_party_source_cited": None,
                    "position": None, "source_url": "", "evidence_note": ""
                } for brand in BRANDS}
            }
            with path.open("x", encoding="utf-8") as stream:
                json.dump(data, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            created.append(path)
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--prompt-ids", nargs="+", default=list(DEFAULT_IDS))
    args = parser.parse_args()
    try:
        paths = prepare_round(args.output_dir, args.run_id, args.engine,
                              tuple(args.prompt_ids))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    for path in paths:
        print("UNOBSERVED (private):", path)
    print("No model queried, no observations collected, no public files changed.")


if __name__ == "__main__":
    main()
