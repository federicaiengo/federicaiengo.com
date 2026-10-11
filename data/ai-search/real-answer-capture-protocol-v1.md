# AI Search benchmark — real-answer capture protocol v1

**Research artifact, not a result report.** The 35 frozen prompts in `competitive-prompts-v1.csv` and the four benchmark entities (Notion, Asana, ClickUp, monday.com) remain unchanged. This protocol prepares the first *real* observation round without importing synthetic sample data as measurements.

## Why an additional capture layer exists

A four-brand observation table is a *scoring output*, not a complete original model response. Reviewers need to retain the exact prompt and answer, capture time, model/engine and cited URLs before deciding whether each brand is **mentioned**, **cited** or **recommended**. Those are distinct classifications. Absence must not be guessed from incomplete collection.

`scripts/ingest_ai_captures.py` converts individually reviewed JSON captures to the **existing, unchanged** 14-column `observations.csv` schema. It does not query AI systems, assign brand labels, scrape accounts or claim visibility changes.

## Suggested first round — small but comparable

Use frozen prompt IDs **D01, U01, P01, R01** (category discovery, capability, pricing, recommendation), collecting *one unaltered answer per prompt per chosen engine*. Record an actual UTC timestamp and exact engine/model configuration for each answer. Use a fresh, documented session; note geography, language, tool/search mode, account/personalization context and notable experimental limitations in the evidence notes. At least two independent rounds are needed to assess repeatability; a single round cannot establish a trend.

Each answer yields four separately reviewed brand rows. A complete four-brand *annotation* is required for a given answer; it does **not** mean all four brands appeared. An explicit `false` means the reviewer inspected the full answer and determined absence; use `null` when a specific classification cannot be resolved. A brand must have at least one deliberately classified main flag, otherwise the capture is incomplete and not ingested.

## JSON capture format (structure only; example is not a measurement)

Use a **local** JSON file for each real, directly observed AI answer:

```json
{
  "run_id": "pilot-2026-10-11-a",
  "observed_at_utc": "2026-10-11T12:00:00Z",
  "engine": "Engine / exact model / search mode",
  "prompt_id": "D01",
  "prompt": "<EXACT text of D01 from competitive-prompts-v1.csv>",
  "answer_text": "<UNEDITED observed model answer>",
  "labels": {
    "Notion": {
      "mentioned": null,
      "cited": null,
      "recommended": null,
      "position": null,
      "owned_source_cited": null,
      "third_party_source_cited": null,
      "source_url": "",
      "evidence_note": "<reviewer rationale and collection environment>"
    },
    "Asana": { "<same keys>": "<reviewed values>" },
    "ClickUp": { "<same keys>": "<reviewed values>" },
    "monday.com": { "<same keys>": "<reviewed values>" }
  }
}
```

The compact brand placeholders above explain the structure; they are not ready-to-ingest data. Replace **all** labels with full reviewed entries. Use JSON booleans (`true`/`false`) or `null`, not quoted boolean strings. For a citation, include the specific cited http(s) URL (multiple URLs joined by `|`) and classify first-party / third-party source if actually known. Include `position` only for explicitly ordered recommendations. Every brand needs a nonempty review note. The importer rejects missing groups, bad timestamps, frozen-prompt drift, fake/example run IDs, duplicate cells and unsupported URL/position combinations. It computes an SHA-256 digest of the captured unedited answer and stores it in each row's evidence note, allowing an independently retained original capture to be compared later.

**Data minimization:** Avoid uploading account-specific conversations, credentials, personal data or confidential workplace content into a public repository. Preserve raw responses separately in an authorized location, redact before intentional publication, and never mistake a hash for publicly accessible evidence. A digest establishes integrity against a retained source; it does not establish the source was genuinely produced by a named AI model.

## Execute

From the website repository root, with Python 3.10+:

```bash
python -m unittest discover scripts/tests -v
python scripts/ingest_ai_captures.py --dry-run /path/to/reviewed-D01.json
python scripts/ingest_ai_captures.py /path/to/reviewed-D01.json
python scripts/analyze_ai_visibility.py
```

The second command performs **no write**. The third appends validated rows to local `data/ai-search/observations.csv` atomically; it rejects duplicate run/date/engine/prompt/brand combinations instead of overwriting observations. Public release of measurement data requires an explicit review of provenance, source permissions, personal information, and consistency. No background jobs, paid APIs or automated AI queries are required.

## What remains unmeasured

As of initial protocol publication, **no verified real cross-engine/model benchmark observations are being claimed here**. Public-source evidence is not an AI response. Unit tests and synthetic fixtures measure code correctness, not Notion/Asana/ClickUp/monday.com visibility. After a real set is collected: validate the entire CSV, report eligible denominators and incomplete rounds, then discuss context and sampling limits before drawing comparisons.
