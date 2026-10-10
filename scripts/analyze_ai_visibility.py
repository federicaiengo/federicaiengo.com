"""Validate and score real AI Search competitive observations, never synthetic rows.

Scope: the *existing* 35-prompt, 4-brand competitive benchmark.
Incomplete model/engine/prompt rounds are preserved but excluded from
cross-brand comparisons; they are NOT silently treated as brand absence.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/ai-search/observations.csv"
SCHEMA = ROOT / "data/ai-search/observations-schema.csv"
PROMPTS = ROOT / "data/ai-search/competitive-prompts-v1.csv"
BRANDS = ("Notion", "Asana", "ClickUp", "monday.com")
BOOLEAN = {"true", "false", ""}
REQUIRED = (
    "run_id", "run_date", "engine", "prompt_id", "prompt_family", "brand",
    "mentioned", "cited", "recommended", "position",
    "owned_source_cited", "third_party_source_cited", "source_url",
    "evidence_note",
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = list(reader)
    return headers, rows


def load_frozen_prompts(path: Path = PROMPTS) -> dict[str, str]:
    headers, rows = read_csv(path)
    if headers != ["prompt_id", "prompt_family", "prompt", "primary_measure"]:
        raise ValueError("Frozen prompt header drift; preserve versioned protocol")
    prompts: dict[str, str] = {}
    for row in rows:
        identifier = row["prompt_id"]
        if not identifier or identifier in prompts or not row["prompt"]:
            raise ValueError("Invalid or duplicate frozen prompt")
        prompts[identifier] = row["prompt_family"]
    families = set(prompts.values())
    if len(prompts) != 35 or len(families) != 7:
        raise ValueError("Expected 35 frozen prompts across seven intent families")
    return prompts


def validate_observations(rows: list[dict[str, str]], prompts: dict[str, str],
                          headers: list[str]) -> None:
    if headers != list(REQUIRED):
        raise ValueError("Observation file must match observations-schema.csv columns")
    seen: set[tuple[str, str, str, str, str]] = set()
    for idx, row in enumerate(rows, 2):
        if None in row:
            raise ValueError(f"Extra CSV fields on line {idx}")
        for field in ("run_id", "run_date", "engine", "prompt_id", "brand"):
            if not (row.get(field) or "").strip():
                raise ValueError(f"Missing {field} on line {idx}")
        if row["run_id"].startswith("EXAMPLE"):
            raise ValueError("Illustrative example must not be scored as a real run")
        try:
            date.fromisoformat(row["run_date"])
        except ValueError:
            raise ValueError(f"run_date must be ISO YYYY-MM-DD on line {idx}") from None
        if row["prompt_id"] not in prompts or row["prompt_family"] != prompts[row["prompt_id"]]:
            raise ValueError(f"Unknown prompt or mismatched family on line {idx}")
        if row["brand"] not in BRANDS:
            raise ValueError(f"Unexpected comparison brand on line {idx}")
        for flag in ("mentioned", "cited", "recommended",
                     "owned_source_cited", "third_party_source_cited"):
            if row.get(flag, "").strip().lower() not in BOOLEAN:
                raise ValueError(f"Invalid {flag} value on line {idx}; use true/false/blank")
        if row["cited"].strip().lower() == "true" and not row["source_url"].strip():
            raise ValueError(f"Cited answer without source URL on line {idx}")
        if row["position"]:
            if not row["position"].isdigit() or int(row["position"]) < 1:
                raise ValueError(f"Invalid ordered-shortlist position on line {idx}")
            if row["recommended"].strip().lower() != "true":
                raise ValueError(f"Ordered position without recommendation on line {idx}")
        key = (row["run_id"], row["run_date"], row["engine"], row["prompt_id"], row["brand"])
        if key in seen:
            raise ValueError(f"Duplicate brand/prompt/engine/run cell on line {idx}")
        seen.add(key)


def measure(items: list[dict[str, str]], field: str) -> dict[str, float | int | None]:
    eligible = [r for r in items if r[field].strip().lower() in ("true", "false")]
    positive = sum(r[field].strip().lower() == "true" for r in eligible)
    total = len(eligible)
    return {"positive": positive, "eligible": total,
            "percent": round(100 * positive / total, 1) if total else None}


def score(rows: list[dict[str, str]]) -> dict:
    by_round: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_round[(row["run_id"], row["run_date"], row["engine"], row["prompt_id"])].append(row)
    complete = [group for group in by_round.values()
                if set(r["brand"] for r in group) == set(BRANDS)]
    comparable = [r for group in complete for r in group]
    summary = {}
    for brand in BRANDS:
        items = [r for r in comparable if r["brand"] == brand]
        recommendations = [r for r in items if r["prompt_family"] == "recommendation"]
        positions = [int(r["position"]) for r in recommendations if r["position"].strip()]
        summary[brand] = {
            "mention": measure(items, "mentioned"),
            "citation": measure(items, "cited"),
            "recommendation": measure(recommendations, "recommended"),
            "ordered_mean_position": round(sum(positions)/len(positions), 2) if positions else None,
            "comparable_rows": len(items),
        }
    return {
        "raw_observation_rows": len(rows),
        "complete_four_brand_rounds": len(complete),
        "incomplete_rounds_excluded": len(by_round) - len(complete),
        "by_brand": summary,
        "by_intent": {
            f"{brand} / {family}": {
                "mention": measure([r for r in comparable if r["brand"] == brand
                                    and r["prompt_family"] == family], "mentioned"),
                "citation": measure([r for r in comparable if r["brand"] == brand
                                     and r["prompt_family"] == family], "cited"),
            }
            for brand in BRANDS
            for family in sorted({r["prompt_family"] for r in comparable})
        },
    }


def show_rate(value: dict) -> str:
    pct = f'{value["percent"]}%' if value["percent"] is not None else "not measured"
    return f'{value["positive"]}/{value["eligible"]} ({pct})'


def main() -> None:
    if not INPUT.exists():
        print("No real observations.csv yet; no AI visibility results to report.")
        return
    expected_headers, _ = read_csv(SCHEMA)
    if expected_headers != list(REQUIRED):
        raise SystemExit("Observation schema changed unexpectedly; review before running")
    headers, rows = read_csv(INPUT)
    if not rows:
        print("Observation file has zero rows; no results to report.")
        return
    prompts = load_frozen_prompts()
    validate_observations(rows, prompts, headers)
    result = score(rows)
    print(f'Collected rows: {result["raw_observation_rows"]}')
    print(f'Comparable complete four-brand rounds: {result["complete_four_brand_rounds"]}')
    print(f'Incomplete rounds excluded: {result["incomplete_rounds_excluded"]}')
    if not result["complete_four_brand_rounds"]:
        print("No balanced brand comparison can yet be calculated.")
        return
    for brand, row in result["by_brand"].items():
        print(f'{brand}: mention={show_rate(row["mention"])}; '
              f'citation={show_rate(row["citation"])}; '
              f'recommendation={show_rate(row["recommendation"])}; '
              f'ordered_mean_position={row["ordered_mean_position"]}')
    print("BY INTENT (includes denominators)")
    for key, value in sorted(result["by_intent"].items()):
        print(f'{key}: mention={show_rate(value["mention"])}; '
              f'citation={show_rate(value["citation"])}')


if __name__ == "__main__":
    main()
