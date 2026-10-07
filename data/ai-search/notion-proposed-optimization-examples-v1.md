# Notion proposed optimization examples — v1

Date: 2026-10-07
Status: independent redesign examples; not changes made by Notion
Companion: notion-public-baseline.md and notion-intervention-register-v1.md

## How to read these examples

"Before" describes the retrieval problem observed across the public information architecture; it is not presented as a verbatim copy of Notion's page text. "Proposed" is original portfolio copy showing how the same evidence could be made more self-contained, answerable and comparison-ready.

## Example 1 — Category definition

### Before: retrieval problem
The product can legitimately be described through several categories: connected workspace, docs/wiki, project management, enterprise search and AI. A category-discovery answer may therefore need to assemble the definition from multiple page contexts.

### Proposed optimized answer block
**What is Notion?**

Notion is a connected workspace for teams to manage knowledge and work in one place. It combines docs and wikis with project and task management, databases, AI capabilities and search across workspace content and supported connected apps.

### Why this is stronger
- Leads with a direct entity definition.
- Preserves the broader product without forcing a single narrow category.
- Names the major capability entities in one self-contained passage.
- Can support discovery and comparison without claiming that every capability is available on every plan.

### Measurement link
Primary prompts: D01, D02, C01, C02.

---

## Example 2 — Enterprise Search capability boundary

### Before: retrieval problem
"AI", "Agent", "Enterprise Search" and "connectors" are related but not interchangeable. If their boundaries are not explicit in the retrieved passage, an answer can overgeneralize what the product searches or what an agent can do.

### Proposed optimized answer block
**What does Enterprise Search search?**

Enterprise Search is designed to answer questions using information the user is permitted to access in Notion and supported connected sources. Connected-source coverage should be stated next to the feature and kept current as integrations change. Search access does not imply broader permissions than the user already has.

**How is that different from an AI agent?**

Search retrieves and synthesizes relevant information. An agent can use available context and tools to carry out a task. The product page should keep these functions distinct even when they work together.

### Why this is stronger
- Answers two likely follow-up questions directly.
- Separates retrieval from action.
- Makes the permission constraint explicit.
- Avoids hard-coding a connector list into reusable copy unless that list is maintained.

### Measurement link
Primary prompts: U01, U02, I01.

---

## Example 3 — Comparison-ready capability block

### Before: retrieval problem
A buyer comparing Notion with Asana, ClickUp or monday.com needs equivalent dimensions. Broad product claims are difficult to compare if evidence for project work, knowledge, search, integrations and AI is scattered.

### Proposed optimized structure
**Notion at a glance for a team evaluating a connected workspace**

| Buyer question | Evidence to expose directly |
| --- | --- |
| Can we manage projects and tasks? | Tasks, subtasks, assignees, due dates, status, dependencies, views and progress. |
| Can we maintain team knowledge? | Docs, wikis and structured databases within the workspace. |
| Can we search outside the workspace? | State supported connected sources, permission behaviour and any plan limitations. |
| What can AI do? | Separate search, meeting notes, agents and other AI capabilities by function. |
| Which plan includes what we need? | Link each volatile capability to a dated pricing/plan source rather than implying universal availability. |

### Why this is stronger
- Uses the questions a buyer actually needs answered.
- Gives retrieval systems stable comparison dimensions.
- Keeps capability evidence separate from product-superiority claims.
- Makes volatile plan evidence visibly conditional.

### Measurement link
Primary prompts: C01, C02, R01.

---

## Example 4 — Pricing/value answer block

### Before: retrieval problem
Pricing tables are machine-readable evidence, but "What should a 20-person team choose?" cannot be answered from seat price alone. AI packaging, required capabilities and billing assumptions matter.

### Proposed optimized answer block
**How should a team compare Notion plans?**

Start with the capabilities the team actually needs, then verify which current plan includes them. For AI-heavy use cases, check the current packaging for agents, enterprise search and meeting features rather than comparing only the per-member headline price. State whether the displayed rate assumes annual billing and date the answer because packaging can change.

### Why this is stronger
- Answers value intent without pretending there is one universally correct plan.
- Prevents a price-only recommendation.
- Makes freshness part of the answer.
- Can be updated without rewriting the core buyer guidance.

### Measurement link
Primary prompts: P01, P02, R01.

## Evaluation rule

These examples demonstrate optimization design, not performance. A future controlled run can test whether the same frozen prompts retrieve clearer evidence or produce more accurate/citable answers after an intervention. Until then, the portfolio labels them as proposed optimized versions.
