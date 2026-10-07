# Notion optimization intervention register — v1

Date: 2026-10-07
Status: proposed interventions, not published changes
Scope: independent portfolio research using Notion's public-site baseline. Not commissioned by or affiliated with Notion.

## Purpose

This register converts baseline observations into testable SEO/AEO/GEO interventions. It deliberately separates diagnosis from recommendation and recommendation from measured outcome.

## Prioritization model

Priority considers:
- buyer-intent relevance;
- retrieval ambiguity;
- evidence already available to support the answer;
- implementation effort;
- whether the intervention can be measured with the frozen prompt set.

No intervention is labelled successful before a controlled post-intervention observation exists.

## Intervention candidates

### N-I01 — Make category boundaries explicit
**Intent families:** discovery, alternatives, comparison
**Diagnosis:** Notion spans workspace, docs, knowledge, project management, enterprise search and AI. Breadth is commercially useful but can make category-level retrieval ambiguous.
**Proposed intervention:** add concise, self-contained category definitions that state what Notion is, which jobs it combines, and where each major capability sits in the product.
**Evidence required:** existing first-party product positioning and capability pages.
**Expected measurable signal:** clearer matching across discovery prompts; this is a hypothesis, not a predicted ranking gain.
**Priority:** high.

### N-I02 — Build comparison-ready capability blocks
**Intent families:** comparison, recommendation
**Diagnosis:** buyers often compare products on dimensions rather than slogans: project execution, knowledge, connected search, integrations, automation and AI.
**Proposed intervention:** expose compact capability blocks using consistent labels, scope and limitations so equivalent dimensions can be retrieved without inference.
**Evidence required:** product, project-management, enterprise-search and connector documentation.
**Expected measurable signal:** more accurate comparison answers and fewer unsupported capability assumptions.
**Priority:** high.

### N-I03 — Tighten AI capability boundaries
**Intent families:** capability, implementation, pricing/value
**Diagnosis:** terms such as Agent, Enterprise Search, AI Meeting Notes and connectors can be retrieved together even though they represent different functions and packaging.
**Proposed intervention:** define each AI capability in one direct answer block: what it does, what sources it can use, relevant permission behaviour, plan/beta status where applicable, and what it does not imply.
**Evidence required:** current first-party AI, enterprise-search, connector and pricing pages.
**Expected measurable signal:** better answer precision and source attribution for AI-specific prompts.
**Priority:** high.

### N-I04 — Connect pricing to buyer questions
**Intent families:** pricing/value, recommendation
**Diagnosis:** a plan table is structured evidence, but buyers ask outcome-oriented questions such as what a 20-person team needs for AI search or whether a capability is included.
**Proposed intervention:** add dated, concise plan-answer sections that connect major capabilities to plan boundaries without hiding billing assumptions.
**Evidence required:** current pricing and product packaging.
**Expected measurable signal:** higher answerability for value prompts and fewer inferred plan claims.
**Priority:** high, but volatile; requires frequent verification.

### N-I05 — Strengthen implementation paths
**Intent families:** implementation, capability
**Diagnosis:** retrieval systems need explicit evidence for migration and adoption questions, not only feature existence.
**Proposed intervention:** create or strengthen task-oriented paths such as moving from a separate wiki/project tracker to a connected workspace, connecting external sources, and preserving permissions.
**Evidence required:** setup, import, connector and permission documentation.
**Expected measurable signal:** stronger evidence coverage for implementation prompts.
**Priority:** medium.

### N-I06 — Add evidence freshness signals
**Intent families:** pricing/value, capability
**Diagnosis:** AI packaging, beta status, connectors and pricing are volatile. Undated content can remain retrievable after it stops being accurate.
**Proposed intervention:** surface meaningful updated dates or version context on volatile commercial/AI documentation and maintain clear canonical pages.
**Evidence required:** change history and current first-party pages.
**Expected measurable signal:** not a direct visibility claim; improves auditability and reduces stale-answer risk.
**Priority:** medium-high.

## Measurement plan

For each intervention, preserve the pre-intervention prompt IDs. A post-intervention run should record the same prompt wording, engine, date, mention/citation/recommendation fields, source URL and evidence note. New exploratory prompts may be added separately but must not replace the frozen baseline.

## Guardrails

- Proposed changes are not represented as changes made by Notion.
- Expected signals are hypotheses, not outcomes.
- No traffic, ranking, citation, recommendation or conversion lift is invented.
- Missing public evidence remains missing.
- Pricing and AI packaging must be reverified before publication.
