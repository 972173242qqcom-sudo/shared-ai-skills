---
name: map-user-scenarios
description: Turn observations, interviews, diary notes, and usage logs into evidence-backed behavioral user definitions, scenario maps, task flows, and intervention opportunities. Use for scenario-based personas, journey reconstruction, attention or interruption analysis, and pre-concept user research synthesis. Do not use to invent demographic personas, fabricate research, or validate a market from unsupported examples.
---

# Map User Scenarios

Transform raw user evidence into scenarios that can guide product decisions without converting assumptions into fictional personas.

## Choose The Working Mode

Infer the narrowest useful mode unless the user selects one.

- `prepare`: define what to observe or ask, and create a record template for a real event.
- `map`: synthesize supplied observations, interviews, diary entries, or logs into user behaviors, scenario frames, task flows, and opportunity moments.
- `audit`: challenge an existing persona, journey, or scenario for invented facts, weak evidence, vague steps, and solution-first conclusions.

Use `prepare` when no real event record exists. Use `map` with limited evidence when necessary, but label the result provisional and state what cannot be generalized.

## Required Context

Use what is available and expose what is missing:

- the decision this research must support;
- source records with source ID, date, method, and sample when known;
- the user's main task, trigger, setting, tools, collaborators, and constraints;
- observable actions, state changes, workarounds, interruptions, errors, delays, and recovery;
- existing user definitions, scenarios, task flows, or product assumptions;
- the current project stage and expected output.

Do not turn an absent field into a plausible detail.

## Evidence Discipline

Use these labels when a statement affects a decision:

- `E — Evidence`: supported by a supplied observation, quotation, log, source, or completed test.
- `H — Hypothesis`: plausible but not yet supported well enough.
- `D — Decision`: a provisional project choice based on current evidence and constraints.
- `U — Unknown`: information that cannot yet be responsibly inferred.

Attach source IDs to consequential evidence. Preserve the difference between one person's event, a repeated pattern within a sample, and a claim about the broader population. Never invent quotations, timestamps, participants, frequency, emotional states, or causal explanations.

## Workflow

1. Restate the research decision and define the evidence boundary.
2. Build a source index. Separate direct observation, participant report, system log, researcher interpretation, and project assumption.
3. Extract observable events: trigger, context, main task, delegated or supporting task, state change, user response, consequence, and recovery.
4. Identify behavioral variables that can change the design, such as frequency, concurrency, duration, mobility, intervention frequency, switching cost, risk, and tolerance for feedback.
5. Define the primary user by behavior and context. Separate adjacent, edge, and non-priority users. Include demographics only when they materially affect access, safety, ergonomics, regulation, or behavior.
6. Build a six-frame scenario: background, main task, delegation or setup, state change, intervention decision, and recovery. Keep the problem observable and avoid prescribing the product form.
7. Map the task flow and mark breakdowns, workarounds, information gaps, decision points, and recovery costs.
8. When attention matters, build a `state × attention level` matrix. Distinguish system state from the urgency of interruption and include false-alert and missed-alert risks.
9. Compare candidate scenarios by frequency, consequence, product relevance, evidence strength, and implementation complexity. Keep reasons beside scores and lower confidence when evidence is weak.
10. End with design implications, excluded conclusions, critical unknowns, and the lowest-cost next observation or test.

For complete schemas and review criteria, read [references/scenario-schema.md](references/scenario-schema.md). When the user needs an editable research sheet, copy and adapt [assets/scenario-research-template.md](assets/scenario-research-template.md).

## Output Rules

For an ordinary response, return only the sections needed for the selected mode.

For a saved project package, use this structure unless the project already has a convention:

```text
01_source-index-and-boundary.md
02_behavioral-user-model.md
03_scenario-six-frames.md
04_task-flow-and-breakdowns.md
05_state-attention-matrix.md
06_scenario-priority-and-next-study.md
07_decision-and-change-log.md
```

Every complete package must make visible:

- which source supports each consequential claim;
- what belongs to E, H, D, and U;
- the behavior and context defining the primary user;
- the exact moment the problem occurs;
- the task flow before, during, and after the breakdown;
- the user's current workaround and its consequence;
- the proposed intervention moment without prematurely fixing the solution form;
- the next study that could confirm or overturn the current direction.

## Guardrails

- Do not use a stock photo, name, age, job title, income, or personality description as a substitute for evidence.
- Do not generalize a self-observation or one interview into a market-wide user truth.
- Do not infer emotion unless the participant stated it or behavior supports a carefully qualified interpretation.
- Do not convert every pain point into a feature. First identify the task, breakdown, consequence, and existing workaround.
- Do not assume an alert must interrupt immediately because a system state changed.
- Do not hide contradictory cases or average away important edge behavior.
- Do not claim that a scenario is validated when it is only a working hypothesis.

## Completion Standard

A scenario package is ready to guide concept work only when:

- the primary scenario contains a real or clearly provisional event chain;
- consequential statements carry evidence status and source IDs;
- the user definition relies on decision-relevant behavior and context;
- the task flow shows a specific breakdown, consequence, and recovery;
- intervention timing is separated from solution form;
- competing scenarios and non-priority users are visible;
- the next validation action and falsification signal are specific.
