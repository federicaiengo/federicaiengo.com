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
| AI Connectors | https://www.notion.com/help/notion-ai-connectors | Connector eligibility and explicit personal-Gmail exception |
| Personal Gmail AI Connector | https://www.notion.com/help/notion-mail-ai-connector | Individual Gmail inbox on any Notion plan; account-email requirement |
| Organizational Gmail AI Connector | https://www.notion.com/help/notion-ai-connector-for-gmail | Workspace/admin requirements and Business/Enterprise eligibility |
| Notion Agent | https://www.notion.com/help/notion-agent | Agent operates with the user's existing permissions |
| Custom Agent permissions | https://www.notion.com/help/custom-agents-sharing-and-permissions | Separate access grants and distinct agent permission model |

These pages were consulted on the date above. Website copy, plan names, prices, availability and betas are volatile: these links are **not** perpetual proof of feature availability or identical localized prices.

## 2. Confirmed distinctions relevant to answer quality

**Core features versus autonomous workflows.** Notion's own AI documentation describes core Notion AI features on Business and Enterprise, including Notion Agent and Enterprise Search. Custom Agents are described separately with a Notion-credit charging model. A buyer-facing answer that says merely “AI is included” can omit a meaningful cost boundary. This supports the existing `N-I03` and `N-I04` proposed interventions.

**Search versus action.** Enterprise Search documentation describes retrieving content from the workspace and connected applications, with source citations, and lets users select search scope. The Notion Agent help page describes editing pages/databases within the acting user's permissions. Custom Agents are documented as having separately granted resource permissions rather than simply inheriting the requester's access. These are materially different behaviors; a comparison that treats “search,” “agent,” and “connected tool” as synonyms risks unsupported claims.

**Connector permissions and exceptions.** Notion's AI Connectors overview specifies Business/Enterprise for most third-party connectors **but explicitly exempts the Personal Gmail AI Connector, which is available on all Notion plans**. The personal connector is for an individual Gmail inbox and requires the Gmail address to match the Notion account email. The distinct **organization-wide Gmail AI Connector** requires Business/Enterprise, Google Workspace organizational access and administrative permissions. These two Gmail integrations must not be conflated; see the overview and both connector-specific help pages below. Plan and connector capabilities must be checked **per integration and use case** rather than summarized as “all AI connectors require Business”. “Basic connections” in a plan table should not automatically be equated with AI-enabled indexed search.

**Correction recorded 2026-10-11:** A prior revision incorrectly claimed that Gmail was always restricted to Business/Enterprise and confused Notion Mail with the Personal Gmail AI Connector. That claim has been withdrawn on verification of the first-party documentation.

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
