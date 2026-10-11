"""Convert reviewed AI answer captures to four-brand observations.

Does not fetch models, infer annotations, or manufacture measurements. Preserve
exact frozen prompts and raw answers in capture JSON; vet all data before making
anything public. Source captures stay local unless deliberately published.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from source_url_validation import valid_source_url

from analyze_ai_visibility import (
    BRANDS, PROMPTS, REQUIRED, read_csv, load_frozen_prompts,
    validate_observations,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data/ai-search/observations.csv"
FLAGS = ("mentioned", "cited", "recommended", "owned_source_cited", "third_party_source_cited")


def real_http_url(value: str) -> bool:
    return valid_source_url(value)


def load_prompt_texts(path: Path = PROMPTS) -> dict[str, tuple[str, str]]:
    families = load_frozen_prompts(path)
    _, rows = read_csv(path)
    return {r["prompt_id"]: (families[r["prompt_id"]], r["prompt"]) for r in rows}


def capture_to_rows(capture: dict, frozen: dict[str, tuple[str, str]]) -> list[dict[str, str]]:
    required = ("run_id", "observed_at_utc", "engine", "prompt_id", "prompt", "answer_text", "labels")
    if not isinstance(capture, dict) or any(key not in capture for key in required):
        raise ValueError("Capture missing mandatory fields")
    run_id, engine, prompt_id = (capture[key] for key in ("run_id", "engine", "prompt_id"))
    if any(not isinstance(v, str) or not v.strip() for v in (run_id, engine, prompt_id)):
        raise ValueError("run_id, engine, prompt_id must be nonempty strings")
    if run_id != run_id.strip() or engine != engine.strip():
        raise ValueError("run_id and engine must not contain surrounding whitespace")
    if run_id.casefold().startswith(("example", "demo", "test", "sample", "synthetic")):
        raise ValueError("Demonstration run IDs cannot enter real observations")
    if any(value.lstrip().startswith(("=", "+", "-", "@")) for value in (run_id, engine)):
        raise ValueError("Unsafe CSV formula prefix in run_id or engine")
    if prompt_id not in frozen or capture["prompt"] != frozen[prompt_id][1]:
        raise ValueError("Prompt absent or different from frozen v1 text")
    raw_answer = capture["answer_text"]
    if not isinstance(raw_answer, str) or len(raw_answer.strip()) < 10:
        raise ValueError("Preserve a meaningful verbatim answer before scoring")
    stamp = capture["observed_at_utc"]
    if not isinstance(stamp, str) or not stamp.endswith("Z"):
        raise ValueError("observed_at_utc must be ISO 8601 UTC ending Z")
    try:
        observed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid UTC timestamp") from exc
    if observed.tzinfo != timezone.utc:
        raise ValueError("Capture timestamp must use UTC")
    labels = capture["labels"]
    if not isinstance(labels, dict) or set(labels) != set(BRANDS):
        raise ValueError("A deliberate label group is required for every benchmark brand")
    answer_digest = hashlib.sha256(raw_answer.encode("utf-8")).hexdigest()
    result = []
    for brand in BRANDS:
        label = labels[brand]
        if not isinstance(label, dict) or any(k not in label for k in FLAGS):
            raise ValueError(f"Missing annotations for {brand}")
        if any(label[k] is not None and type(label[k]) is not bool for k in FLAGS):
            raise ValueError(f"Use true, false or null for {brand} flags")
        if all(label[k] is None for k in ("mentioned", "cited", "recommended")):
            raise ValueError(f"{brand} has no reviewed evidence classification")
        if label["cited"] is True and not label.get("source_url"):
            raise ValueError(f"{brand} cited=true requires URL")
        if label["cited"] is not True and (
            label["owned_source_cited"] is True or label["third_party_source_cited"] is True
        ):
            raise ValueError(f"{brand} source classification requires cited=true")
        urls = label.get("source_url") or ""
        if not isinstance(urls, str) or (urls and not all(real_http_url(x.strip()) for x in urls.split("|"))):
            raise ValueError(f"{brand} requires valid http(s) source URLs")
        if urls and label["cited"] is not True:
            raise ValueError(f"{brand} source URL requires cited=true")
        position = label.get("position")
        if position is not None and (
            type(position) is not int or position < 1 or label["recommended"] is not True
        ):
            raise ValueError(f"{brand} position only valid for an explicit ordered recommendation")
        note = label.get("evidence_note")
        if not isinstance(note, str) or not note.strip():
            raise ValueError(f"{brand} needs an evidence review note")
        result.append({
            "run_id": run_id, "run_date": observed.date().isoformat(),
            "engine": engine, "prompt_id": prompt_id,
            "prompt_family": frozen[prompt_id][0], "brand": brand,
            **{flag: "" if label[flag] is None else str(label[flag]).lower() for flag in FLAGS},
            "position": "" if position is None else str(position),
            "source_url": urls,
            "evidence_note": f"observed_at_utc:{stamp}; sha256:{answer_digest}; {note.strip()}",
        })
    return [{key: item[key] for key in REQUIRED} for item in result]


def ingest(paths: list[Path], output: Path, dry_run: bool = False) -> tuple[int, int]:
    frozen = load_prompt_texts()
    new_rows: list[dict[str, str]] = []
    for source in paths:
        with source.open(encoding="utf-8") as handle:
            new_rows.extend(capture_to_rows(json.load(handle), frozen))
    current_rows: list[dict[str, str]] = []
    families = {k: f for k, (f, _) in frozen.items()}
    if output.exists():
        headers, current_rows = read_csv(output)
        validate_observations(current_rows, families, headers)
    combined = current_rows + new_rows
    validate_observations(combined, families, list(REQUIRED))
    if dry_run:
        return len(new_rows), len(combined)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".observations-", suffix=".csv", dir=output.parent)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(REQUIRED))
            writer.writeheader()
            writer.writerows(combined)
        os.replace(tmp_name, output)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    return len(new_rows), len(combined)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("captures", type=Path, nargs="+", help="Reviewed real-answer JSON files")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--dry-run", action="store_true", help="Validate without changing observations.csv")
    options = parser.parse_args()
    try:
        added, total = ingest(options.captures, options.output, options.dry_run)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(
        f"Validated {added} brand observations; total {total}. "
        + ("No file changed." if options.dry_run else f"Saved {options.output}")
    )


if __name__ == "__main__":
    main()
