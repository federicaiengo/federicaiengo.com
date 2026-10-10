# Competitive Intelligence Protocol v1

## Objective
Compare Notion, Asana, ClickUp and monday.com across identical buyer-intent prompts without treating one generated answer as a stable ranking.

## Frozen prompt set
35 prompts across seven intent families: category discovery, alternatives, comparison, capability, pricing/value, implementation and recommendation. Prompt text is versioned before scoring.

## Observation unit
One brand × one prompt × one engine/run. Record mention, citation, recommendation inclusion, ordinal position when meaningful, owned/third-party citation type, source URL and evidence note.

## Core metrics
- Mention Coverage = prompts mentioning brand / eligible prompts.
- Citation Coverage = prompts with a citation supporting brand / eligible prompts.
- Recommendation Coverage = recommendation prompts including brand / eligible recommendation prompts.
- Mean Position is reported only where the response presents an ordered shortlist; it is never treated as a universal search rank.
- Intent Consistency = dispersion of coverage across prompt families; family-level results remain visible even when a summary is shown.

## Guardrails
No fabricated observations. Missing evidence remains missing. Pricing and capabilities are time-sensitive and must carry collection dates. Correlation does not establish a ranking factor. Repeated runs should retain raw observations rather than overwrite them.

## Implemented validation and fair comparison (2026-10-09)

The original frozen prompts remain untouched: **35 unique prompts in seven intent families**, five per family. The separate 12-prompt Notion case study is unchanged.

The revised `scripts/analyze_ai_visibility.py` implements source-level validation before any comparison. Real observations belong in `data/ai-search/observations.csv` (not yet collected); a schema-only example in `observations.example.csv` is deliberately labelled **EXAMPLE_NOT_MEASURED** and must not be scored. The example now matches the 14-field schema.

- Every brand row requires an ISO run date, engine/run identifier, valid frozen prompt ID and matching family; booleans are `true`, `false`, or blank. Invalid values do not silently become negatives.
- A brand `cited=true` must include an actual source URL. If a metric is blank, its denominator excludes the unknown observation instead of treating it as `false`.
- **Comparable run:** the same run ID, date, engine and prompt must contain all four benchmark brands. Incomplete sets are counted and reported but **excluded** from four-brand comparative percentages; this controls false absence from data-collection gaps but cannot remove every selection bias.
- Mention/citation coverage includes explicit numerator and eligible denominator. Recommendation coverage uses recommendation-intent prompts only. Ordered mean position uses explicitly recorded shortlist positions and is **not** a universal AI Search rank.
- Store the exact unedited answer or a privacy-safe reproducible transcript reference in `evidence_note` / controlled evidence storage before interpreting source claims. Do not silently alter archived observations.
- Any apparent performance change requires repeated comparable observations, date context and a discussion of model changes, geography, personalization, indexing and missingness. No causality is assumed.

**Execution gate:** current 15 unit tests for validation/scoring passed in an isolated local Python 3.13.5 session against scripts verified byte-for-byte by Git blob SHA; these are **synthetic test fixtures, not measured responses**. The CLI currently reports that no real `observations.csv` exists.

Run from the site repository root (locally, without deploying):

```bash
python -m unittest discover scripts/tests -v
python scripts/analyze_ai_visibility.py
```

## Portfolio interpretation
Observed evidence, analysis/inference and proposed optimization are separate layers. The project is independent research and is not client work for any benchmarked company.
