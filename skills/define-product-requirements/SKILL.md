---
name: define-product-requirements
description: Turn a vague product or industrial-design request into a traceable, testable Product Brief. Use for requirement clarification, problem definition, scope boundaries, evidence/hypothesis separation, brief generation, or pre-concept audits. Do not use to invent user research, generate styling concepts, or claim engineering feasibility.
---

# Define Product Requirements

Convert incomplete project input into a Product Brief that can guide research and concept work without disguising assumptions as facts.

## Choose The Working Mode

Infer the narrowest useful mode from the request. If the user explicitly selects one, follow it.

- `clarify`: clean the input, separate evidence from assumptions, expose conflicts, and produce prioritized questions.
- `build`: create or revise a complete Product Brief and minimum validation plan.
- `audit`: challenge an existing brief before research or concept generation.

Use `clarify` before `build` when the input is too vague to support responsible decisions. Do not block all progress when information is incomplete; create a provisional brief, mark unknowns, and identify the decisions they prevent.

## Required Context

Use what the user has and distinguish missing information explicitly:

- original request and project background;
- target user, buyer, operator, or other affected roles;
- trigger, setting, task, current workaround, and failure point;
- business objective and reason for doing the project;
- product, cost, schedule, channel, technical, legal, brand, and delivery constraints;
- available evidence with source, date, sample, and confidence when known;
- expected project stage and final deliverable.

Never convert an absent field into a plausible-sounding fact.

## Evidence Discipline

Use these labels whenever the distinction affects a decision:

- `E — Evidence`: directly supported by supplied material, observation, source, or completed test.
- `H — Hypothesis`: plausible but unverified.
- `D — Decision`: a current project choice made from available evidence and constraints.
- `U — Unknown`: information that is missing and cannot yet be responsibly inferred.

Preserve source wording when a claim is consequential. Record contradictions instead of silently choosing the most convenient version. Do not upgrade self-observation, a single interview, AI inference, or a marketing statement into general user evidence.

## Workflow

1. Restate the project in one neutral sentence without adding a solution.
2. Build an E/H/D/U register. Separate user needs, client requests, business objectives, and implementation constraints.
3. Identify conflicts and decision-critical gaps. Rank questions by how much the answer could change the project direction.
4. Define the target user by relevant behavior and context rather than decorative demographics. Separate user, buyer, installer, maintainer, and approver when relevant.
5. Describe the trigger, current task chain, workaround, obstacle, consequence, and desired outcome.
6. Write a problem statement, Job Statement, How Might We question, and value hypothesis. Keep them solution-neutral unless the product form is an explicit constraint.
7. Establish `Must / Should / Won't` boundaries and identify conflicting goals.
8. Convert goals into observable success criteria. Separate what can be checked now, what needs a prototype or study, and what is outside the current stage.
9. Produce the minimum validation plan: question, evidence needed, lowest-cost method, success signal, falsification signal, owner when known, and next decision.
10. End with a readiness judgment and the specific conditions required before moving to research or concept generation.

For a complete brief or a scored audit, read [references/brief-schema.md](references/brief-schema.md). When the user asks for an editable blank document, copy and adapt [assets/product-brief-template.md](assets/product-brief-template.md).

## Output Rules

For an ordinary chat response, return the smallest useful set of sections for the selected mode.

For a saved project package, use this structure unless the user already has a preferred format:

```text
01_input-and-source-index.md
02_EHD-U-register.md
03_product-brief.md
04_minimum-validation-plan.md
05_decision-and-change-log.md
```

Every complete package must make the following visible:

- confirmed input and source limits;
- assumptions and unknowns that could change direction;
- target user and scenario;
- user task, obstacle, and consequence;
- problem statement and value hypothesis;
- project scope and anti-goals;
- observable success criteria;
- next validation actions;
- readiness status.

## Guardrails

- Do not generate product form, CMF, feature lists, or marketing copy unless the user explicitly moves beyond requirement definition.
- Do not make hardware the answer merely because the original request asks for a device. Test whether software, service, process, or existing products may solve the task.
- Do not treat “premium,” “young,” “smart,” “minimal,” or “easy to use” as requirements until translated into observable implications.
- Do not invent market size, interviews, quotations, prices, regulations, tests, or technical feasibility.
- Do not force every unknown to be researched. Prioritize only unknowns that could change the decision.
- State when an output is a provisional working brief rather than a validated conclusion.

## Completion Standard

A brief is ready for the next stage only when:

- it names one primary user and scenario;
- it defines an observable task and obstacle;
- consequential statements carry E/H/D/U status;
- the scope states what will and will not be solved;
- success criteria can be checked;
- important contradictions are visible;
- the next validation action is specific;
- the user can explain what evidence would cause the current direction to change.
