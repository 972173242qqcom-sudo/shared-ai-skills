---
name: competitive-product-analysis
description: Analyze collected competitor evidence across physical products, software, services, platforms, and B2B solutions, turning it into comparison models, opportunity hypotheses, and decision-ready reports. Use for competitive analysis, positioning, design opportunity discovery, scoring, or strategy synthesis. Do not use when the main task is searching, downloading, deduplicating, or licensing source assets.
---

# Competitive Product Analysis

# Version

V1.0 — initial reusable release for cross-category competitor analysis, evidence auditing, opportunity discovery, and decision-ready reporting.

Turn an existing evidence package into a decision, not a screenshot collection. Keep research collection and analysis separate: this skill consumes traceable evidence; a collection skill produces and maintains that evidence.

## Start From The Decision

Before choosing dimensions or competitors, state:

- the decision this analysis must support;
- the target user, scenario, product stage, and geography;
- the primary comparison question;
- the freshness date and known evidence limits.

If the requested decision is unclear, infer a narrow working question from the deliverable and label it as an assumption. Do not create a universal scorecard without a decision context.

## Select The Analysis Mode

Classify the offering before selecting dimensions: physical product, software or SaaS, service, platform or marketplace, B2B solution, consumer goods or retail, or a hybrid. Choose one primary lens and at most two supporting lenses from product experience, market and positioning, business model, technology and operations, channel and brand, or trust and compliance.

Read [references/dimension-packs.md](references/dimension-packs.md) and select only the dimensions that can change the target decision. Do not force hardware interaction dimensions onto non-hardware categories or combine every available dimension into one oversized matrix.

## Audit The Input Package

When competitor and asset manifests are available, run `scripts/audit_package.py` before analysis. Treat missing images, sources, status, price, or stable identifiers as visible gaps. Do not silently remove competitors because their evidence is incomplete.

For image-led HTML, slides, or documents where visual evidence materially supports the decision:

- every listed competitor needs a basic comparison row;
- every deep-dive competitor needs at least one traceable hero image;
- use one clear product image before adding detail images;
- label third-party, retailer, historical, or reference-only images;
- if coverage is incomplete, show a missing-evidence list or return to the collection workflow.

Read [references/handoff-contract.md](references/handoff-contract.md) when preparing or validating the collection-to-analysis handoff.

## Build The Analysis

1. Separate competitors into three rings: direct task competitors, adjacent solutions, and analogous experiences. Explain why each ring matters.
2. Label reasoning as evidence, hypothesis, or decision. Do not present inference as a sourced fact.
3. Choose comparison dimensions from the decision and offering type. Start with the universal core, then add the relevant domain pack. For interaction-heavy products, task object, state model, attention mechanism, feedback channel, intervention mode, cross-device ability, and safety/reversibility remain useful defaults.
4. Weight dimensions by the research question. A score is a compressed argument, not an objective truth. Preserve the underlying evidence and rationale.
5. Compare patterns, trade-offs, contradictions, and failure cases. Identify what the market systematically overbuilds, under-serves, or makes unnecessarily risky.
6. Convert findings into opportunity hypotheses. Each hypothesis must include target user and scenario, unmet task, supporting evidence, proposed mechanism, non-negotiable principles, lowest-cost test, main risk, and falsification condition.
7. End with a recommended direction, explicit anti-goals, evidence gaps, and a validation plan.

Read [references/analysis-framework.md](references/analysis-framework.md) when selecting dimensions, scoring, or writing opportunity hypotheses.

## Evidence Rules

- Prefer official product pages, support documents, pricing pages, manuals, release notes, and credible primary reporting.
- Record source URL, source type, retrieval date, market/region, and whether the product is current, announced, unavailable, or discontinued.
- Distinguish current facts from historical facts. Prices and availability require dates and regions.
- Use `E` for evidence, `H` for hypothesis, and `D` for decision when the distinction is not obvious in prose.
- Cite negative cases as carefully as successful products; shutdowns, recalls, dependence on cloud services, and channel failures often reveal design constraints.
- Do not claim image reuse rights from product availability. Keep usage notes and attribution with the asset.

## Deliverables

Choose the smallest format that supports the decision. A complete report normally contains:

- executive decision summary;
- scope, research question, method, and evidence limits;
- competitor pool and market structure;
- comparison matrix with decision-specific rationale;
- representative deep dives and failure cases;
- opportunity map and three to five testable hypotheses;
- recommendation, anti-goals, risks, and validation plan;
- appendix with the full competitor list, image/source coverage, and citations.

For HTML, DOCX, slides, or a review dashboard, read [references/deliverable-templates.md](references/deliverable-templates.md). Preserve the same evidence model across formats.

## Boundary With Collection Skills

Use a collection skill for discovery, downloading, quality screening, deduplication, licensing, manifests, and contact sheets. Use this skill for framing, comparison, interpretation, opportunity discovery, and decisions.

When analysis exposes a gap, issue a narrow collection request containing the missing competitor IDs, required evidence fields, desired image role, source preference, and freshness requirement. Do not restart broad research unless the user asks for it.

## Success Criteria

- The report answers a named decision rather than merely describing products.
- Every material claim is traceable or explicitly labeled as hypothesis.
- Competitor and image coverage are visible and auditable.
- Comparison dimensions reflect the decision and preserve trade-offs.
- The framework fits the offering type instead of importing irrelevant dimensions from another category.
- Opportunities are testable and include falsification conditions.
- Recommendations state both what to do and what not to do.
