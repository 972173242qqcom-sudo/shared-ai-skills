---
name: generate-industrial-design-sketches
description: Turn product briefs, user scenarios, competitor conclusions, opportunity hypotheses, constraints, and reference images into controlled batches of industrial-design sketches and evidence-aware shortlists. Use for early form exploration, silhouette and proportion studies, physical interaction sketches, state-expression studies, structural combinations, sketch review, and concept-direction selection. Do not use to claim engineering feasibility, copy a competitor's distinctive design, or replace research with attractive renderings.
---

# Generate Industrial Design Sketches

Convert design evidence into deliberately varied sketches, then reduce them to a small set of directions worth validating.

## Choose The Working Mode

Use the narrowest useful mode unless the user specifies one.

- `plan`: turn research and constraints into a sketch plan without generating images.
- `explore`: create controlled sketch batches around defined variables.
- `shortlist`: compare supplied sketches and retain two to four materially different directions.
- `iterate`: revise one retained direction while preserving its product logic.

If the available environment cannot generate images, produce complete sketch briefs and prompts that can be transferred to an image tool. Do not imply that images were generated when they were not.

## Required Context

Use what is available and expose what is missing:

- the decision the sketches must support;
- the primary user scenario and task breakdown;
- competitor findings, opportunity hypotheses, and source IDs when available;
- required functions, physical constraints, prohibited features, and validation budget;
- reference images and the specific qualities to learn from each reference;
- the variables to explore in this round;
- the expected number, format, and destination of sketch boards.

Do not invent research, dimensions, mechanisms, manufacturing claims, or user preferences. Mark consequential statements as `E — Evidence`, `H — Hypothesis`, `D — Decision`, or `U — Unknown` when evidence quality matters.

## Separate Design Logic From Visual Treatment

Before drawing, write a one-sentence direction statement containing:

1. the user value;
2. the mechanism that creates that value;
3. the physical relationship being explored;
4. the major trade-off or deliberate omission.

Treat reference images as sources of transferable attributes such as proportion, control hierarchy, seam strategy, light diffusion, grip geometry, or surface transition. Never reproduce a reference product's distinctive silhouette, branding, graphic layout, or ornamental identity.

## Workflow

1. Restate the decision, evidence boundary, non-negotiable constraints, and anti-goals.
2. Build a sketch-variable table. Typical variables include footprint, center of gravity, posture, primary control, status expression, component arrangement, and user reach.
3. Choose one major variable for the first round. Hold the others sufficiently stable so the sketches remain comparable.
4. Create a batch plan with materially different candidates rather than cosmetic variants.
5. For early exploration, default to black fineliner, graphite construction lines, light gray marker, white paper, minimal labels, and no final CMF or advertising scene.
6. Generate each distinct sketch board separately when using an image tool. Keep prompts explicit about the product category, view, sketch medium, variables, and forbidden content.
7. Inspect the results for duplicates, accidental competitor copying, impossible perspective, inconsistent controls, decorative detail, unreadable state logic, and premature rendering polish.
8. Record every candidate in a review matrix. Evaluate scenario fit, mechanism clarity, state readability, differentiation, validation cost, and anti-goal violations.
9. Retain two to four directions with different product logic. For each, state why it remains, what it intentionally gives up, the largest unknown, and the cheapest next test.
10. Save the sketch boards, plan, review matrix, and decision log in the project package when the task is project-bound.

Use [assets/sketch-brief-template.md](assets/sketch-brief-template.md) to plan a batch and [assets/sketch-review-matrix.md](assets/sketch-review-matrix.md) to make the shortlist traceable.

## Controlled Exploration Rounds

Use these rounds when the project needs broad exploration. Skip rounds that do not support the decision.

### Round 1 — Silhouette And Massing

Compare footprint, posture, proportion, center of gravity, and relationship to the desk, body, or environment. Avoid detailed interfaces.

### Round 2 — Interaction And State

Explore primary controls, hand approach, motion, status lights, direction changes, tactile feedback, and how a user understands system state. Keep the chosen massing families visible.

### Round 3 — Structure And Combination

Combine the strongest massing, interaction, and state-expression ideas. Show seams, assemblies, support, access, and component relationships only as hypotheses—not proof of engineering feasibility.

### Round 4 — Direction Iteration

Select one direction and vary a single unresolved relationship, such as knob position, tilt angle, light aperture, or module spacing. Do not reopen every variable at once.

## Image-Generation Rules

- Use one generation call per distinct board or deliverable when the tool supports it.
- Request several clearly different candidates within the board, not repeated angles of one design.
- Keep sketch annotations short and legible; add precise labels outside the generated image if text accuracy matters.
- Do not add logos or pretend the concept belongs to an existing brand.
- Do not use polished photorealistic rendering during early exploration unless the user explicitly moves to CMF or visualization.
- Preserve local output files in the project asset directory and use stable relative paths in documents.
- If a generated image is missing, corrupted, or visually inconsistent, regenerate or replace it before claiming completion.

## Shortlist Criteria

Score with written reasons rather than numbers alone:

- scenario fit: does the concept address the observed task and breakdown;
- mechanism clarity: can the user understand how value is created;
- state readability: can important states be distinguished quickly;
- differentiation: is the difference meaningful rather than stylistic;
- validation cost: can the riskiest assumption be tested cheaply;
- feasibility uncertainty: what is still unknown and must not be presented as solved;
- anti-goal compliance: does the concept avoid prohibited directions.

Reject attractive sketches when they fail the scenario, depend on an unexplained mechanism, copy a reference, or conceal the critical unknown.

## Output Rules

For a complete saved package, use this structure unless the project already has a convention:

```text
01_sketch-input-and-boundary.md
02_sketch-batch-plan.md
03_sketch-boards/
04_sketch-review-matrix.md
05_shortlisted-directions.md
06_decision-and-change-log.md
```

Each shortlisted direction must include:

- one-sentence product logic;
- source sketch IDs;
- user value and working mechanism;
- retained physical relationships;
- deliberate omissions;
- largest risk or unknown;
- lowest-cost next validation;
- evidence status for consequential claims.

## Completion Standard

The sketch phase is complete only when:

- the batch answers a named design decision;
- candidates differ in product logic or a controlled major variable;
- references are translated into attributes rather than copied;
- all images are accessible and traceable to prompts or briefs;
- duplicates and anti-goal violations have been removed;
- the shortlist includes explicit keep and reject reasons;
- no sketch is presented as engineering or market validation;
- the next test can confirm or overturn each retained direction.
