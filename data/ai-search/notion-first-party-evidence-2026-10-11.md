# Notion SEO/AEO/GEO study — dated first-party evidence review

**Observation date:** 2026-10-11  
**Research subject:** Notion's public product, help, and pricing documentation  
**Independence:** This study is not commissioned by or affiliated with Notion.  
**Evidence type:** Public-source content review; **not** a test of Google rankings or AI answer visibility.

## 1. Source inventory

| Source | First-party URL | Evidence relevant to the study |
|---|---|---|
| Pricing | https://www.notion.com/it/pricing | Plan boundaries, billing assumptions, Notion AI packaging, agent credits |
| Notion AI | https://www.notion.com/product/ai | Included AI features vs separately metered Custom Agents |
| Enterprise Search | https://www.notion.com/help/enterprise-search | Availability on Business/Enterprise, source citations, scope and model selection |
| AI Connectors | https://www.notion.com/help/notion-ai-connectors | Connector eligibility, connected systems, exceptions |
| Notion Agent | https://www.notion.com/help/notion-agent | Agent operates with the user's existing permissions |
| Custom Agent permissions | https://www.notion.com/help/custom-agents-sharing-and-permissions | Separate access grants and distinct agent permission model |

These pages were consulted on the date above. Website copy, plan names, prices, availability and betas are volatile: these links are **not** perpetual proof of feature availability or identical localized prices.

## 2. Confirmed distinctions relevant to answer quality

**Core features versus autonomous workflows.** Notion's own AI documentation describes core Notion AI features on Business and Enterprise, including Notion Agent and Enterprise Search. Custom Agents are described separately with a Notion-credit charging model. A buyer-facing answer that says merely “AI is included” can omit a meaningful cost boundary. This supports the existing `N-I03` and `N-I04` proposed interventions.

**Search versus action.** Enterprise Search documentation describes retrieving content from the workspace and connected applications, with source citations, and lets users select search scope. The Notion Agent help page describes editing pages/databases within the acting user's permissions. Custom Agents are documented as having separately granted resource permissions rather than simply inheriting the requester's access. These are materially different behaviors; a comparison that treats “search,” “agent,” and “connected tool” as synonyms risks unsupported claims.

**Connector permissions and exceptions.** The general AI Connectors documentation lists Business/Enterprise as the requirement for connecting third-party apps, while explicitly identifying **Notion Mail** and **Notion Calendar** as available on all plans. **Do not confuse Notion Mail with the separate Gmail AI Connector**, which falls under the documented Business/Enterprise rule. Plan and connector details should therefore be checked **per connector and per use case**, not reduced to a universal “all integrations require Business” statement. “Basic connections” in a plan table should not automatically be treated as equivalent to AI-enabled indexed search.

**Localized prices and usage assumptions.** The Italian-language pricing page observed in USD displays Free, Plus, Business and Enterprise tiers and lists Plus at USD 10/member/month, Business at USD 20/member/month, with Enterprise quote-based. The pricing page also has monthly/annual and currency selectors; another locale/currency can differ. For a hypothetical 20-person team, a published seat price is not a complete total-cost estimate without billing period, geography, plan, number of billable members, AI feature eligibility and any extra usage credits.

## 3. Proposed refinements to the intervention register

| Existing ID | Additional testable design refinement | Verification requirement |
|---|---|---|
| N-I03 | Use separate direct-answer sections for Enterprise Search, Notion Agent and Custom Agents; explicitly distinguish retrieval, actions and resource permissions. | Link each scope/permission assertion to the relevant current Help documentation. |
| N-I04 | Build a dated buyer-answer matrix: monthly vs annual, selected currency, 20 billable members, core AI vs separately metered custom-agent usage. | Recheck first-party pricing and applicable credit rules at observation time; avoid invented totals for unknown consumption. |
| N-I06 | Add verification timestamps and source links near fast-changing feature/plan claims; distinguish beta status by plan. | Revisit official documentation before the next observational round. |

These are **research proposals for a third party's public information architecture**, not changes made to Notion. The baseline's original 12 prompts and competitive benchmark's separate 35 prompts remain frozen. Do not backfill a historical Notion result using this later snapshot.

## 4. What can and cannot be concluded

This review shows that first-party evidence exists for several high-intent capability, pricing and implementation questions. It cannot establish whether any given AI engine retrieves that evidence, accurately cites it, recommends Notion, or changes behavior after an optimization. Those claims require separately captured model responses, repeatable sampling and clearly defined denominators.

**Measurement next step:** compare frozen capability (U01/U02) and pricing (P01/P02) prompts against actual recorded model answers, checking feature-boundary accuracy as a qualitative dimension alongside mentions, citations and recommendations. Missing AI observations remain **unmeasured**, not zero.
