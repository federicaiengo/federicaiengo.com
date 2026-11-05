# Professional website — SEO, AEO and GEO measurement protocol (v1)

## Purpose and attribution boundary
This is the **existing** independent professional-site case study, not a new project. The site is the canonical hub and GitHub is technical evidence. Measure qualified discoverability and professional contacts, not vanity rankings. Distinguish actual platform/source observations from hypotheses and from source commits.

## Measurement strata
1. **Technical / SEO:** public domain response; robots/sitemap; page crawl/index status from a verifiable source; page-level canonical/title/meta/structured-data validation; actual search impressions, queries, clicks and pages from Search Console when the owner supplies authorized data.
2. **AEO:** answerable passages, clear referents, cited definitions and evidence, page question/intent mapping; technical presence is not proof that an answer engine used the page.
3. **GEO / AI Search:** prespecified branded and unbranded prompts (see `site-query-set-v1.csv`). Archive exact timestamp, engine/model, language, geography, prompt, unedited answer, URLs actually cited, and independent classification of mention/citation/recommendation. A model naming the owner when directly prompted by name is **brand recall**, not proof of unbranded discovery.
4. **Career value:** human-verified qualified profile visits, work samples opened, contacts, recruiter replies and relevant interviews when data is available. Do not upload personal correspondence or recruiter identity publicly.

## Controls and sequence
- Freeze query text and evaluation rules **before** running a round. Preserve prompt version even when improving later versions.
- Record a genuine pre-change baseline **when available**. Historical source commits without past measurements must not be retroactively represented as a measured baseline.
- Run comparable prompts at specified date/time, browser/account state, geography and language; repeat the SAME prompt/model to estimate variance, separating different model versions.
- Record link/quote evidence and response snapshots under private storage if necessary; publicly share only nonconfidential permitted excerpts. Distinguish own-domain citations, third-party citations and unsupported mentions.
- For changes, log intervention and Git commit, then determine if deployed. **Never** use a GitHub source commit date as a live-site publication date.
- With no comparable pre-change measurement, report **post-change observation only**, never percent uplift.
- For sparse samples, present raw numerators/denominators and uncertainty. AI output volatility, model updates, query selection, personalization, search indexing and external posts are confounders.
- Never attribute traffic or AI visibility changes causally to one edit without a design that supports the inference.

## Current source/retrieval evidence — 2026-10-09
- Astro site config uses `site: https://federicaiengo.com` and the sitemap integration. `public/robots.txt` allows crawling and points to `https://federicaiengo.com/sitemap-index.xml`. **This verifies repository configuration, not live indexing.**
- Latest successful GitHub Pages workflow in available history: run `37931193234`, source SHA `e88b09207cf7b43e5bc017c28ab3feceb3bb6099`; latest main source is ahead. No permission to infer recent work is live.
- Attempted public retrieval via available external text tool for `https://federicaiengo.com/`; tool reported inaccessible. A site-restricted discovery query returned no hits. Neither observation establishes a site outage or lack of indexing; both are **inconclusive**.
- Search Console, web analytics and actual AI model responses: **not provided or measured here**. No synthetic visibility gains should be recorded.

## Status update — 2026-11-05 (observations vs source checks)
- **Owner-reported Search Console observation (2026-10-27):** the URL-prefix property for `https://federicaiengo.com/` was verified and `sitemap-index.xml` was submitted. Search Console reported **11 discovered URLs**. This is a sitemap discovery count, **not** evidence of 11 indexed pages; the indexing report was still processing at the time. No subsequent index totals, query impressions, clicks, CTR or average positions are verified in this repository.
- **Last independently verified live release:** 2026-11-03, source commit `f954995`, Pages run [41689513930](https://github.com/federicaiengo/federicaiengo.com/actions/runs/41689513930) and HTTP smoke [41689683757](https://github.com/federicaiengo/federicaiengo.com/actions/runs/41689683757). This verifies a release and an HTTP check, not browser rendering or search visibility.
- **Later unpublished site source:** the synthetic DuckDB 15-model E-Commerce evidence alignment passed source-only preflight [41927133381](https://github.com/federicaiengo/federicaiengo.com/actions/runs/41927133381). The subsequent dependency-lock milestone passed clean `npm ci`, 83 Python tests and Astro build in [PR #2 preflight 41928173058](https://github.com/federicaiengo/federicaiengo.com/actions/runs/41928173058). Neither is a Pages deployment. The current HEAD after final documentation/workflow changes has not been separately confirmed with a complete build in the cited evidence.
- **AI-search observations:** no controlled, completed comparable query round or verified third-party citation baseline is documented here. Owner-observed variations in identity-disambiguation answers are anecdotal, not a controlled measurement.
- **Next measurement gate:** after a separately authorized release and verified live smoke, obtain dated Search Console coverage/performance exports (or owner-confirmed snapshots), then run frozen branded/unbranded prompt rounds with exact engine, version, timestamp and cited URLs. Report numerators and missing data; do not infer ranking or citation uplift without a comparable baseline.

## Data files
- `change-ledger-v1.csv`: source-side interventions, evidence status and follow-up tests.
- `site-query-set-v1.csv`: versioned prompts **not yet executed**.
- `site-observations-v1.csv`: schema only; **zero** measured rows until actual observations are available.

## Decision rule
Do not add public case-study claims about improved rankings, AI citations or qualified demand without a dated and reproducible evidence record. Iterations must improve the work itself and the credibility of the claims.
