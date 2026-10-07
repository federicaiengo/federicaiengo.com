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

## Portfolio interpretation
Observed evidence, analysis/inference and proposed optimization are separate layers. The project is independent research and is not client work for any benchmarked company.
