# Product Brief Schema And Audit

Read this reference when building a complete Product Brief or auditing whether a project can enter research or concept development.

## Complete Brief

### 1. Project Frame

- Project name and version
- Date and owner
- Current stage
- Original request
- Business objective
- Expected deliverable
- Explicit project boundary

### 2. Evidence Status

Record each consequential item with:

| ID | Statement | Status | Source or reason | Confidence | Decision affected |
|---|---|---|---|---|---|
|  |  | E / H / D / U |  | high / medium / low |  |

### 3. People And Roles

- Primary user
- Secondary user
- Buyer or budget owner
- Installer, maintainer, approver, or affected party when relevant
- People explicitly not prioritized in this version

Use behavior, task frequency, environment, capability, and consequence. Include age, occupation, or income only when it changes the design.

### 4. Scenario And Task Chain

- Trigger
- Time and place
- Main task already in progress
- Current workaround
- Step where friction occurs
- Observable consequence
- Desired outcome
- Before and after context

### 5. Definition Statements

Problem statement:

> For [primary user], when [trigger and scenario] and they try to [task], [obstacle] causes [observable consequence]. We need to explore [opportunity], while avoiding [important boundary].

Job Statement:

> When [situation], I want to [motivation or task], so I can [desired progress].

How Might We:

> How might we help [user] achieve [progress] in [scenario], without causing [new burden or risk]?

Value hypothesis:

> If [mechanism] helps [user] reduce [cost or consequence] during [scenario], it may be more valuable than [current workaround] because [reason to test].

### 6. Scope

- `Must`: the project fails without it.
- `Should`: valuable if evidence and resources support it.
- `Won't`: explicitly excluded from this version.
- Anti-goals: attractive directions that would undermine the core task.
- Conflicts: pairs of goals that cannot both be maximized.

### 7. Success Criteria

For every criterion, record:

- observable behavior or comparison;
- validation stage: now / research / concept prototype / engineering / later;
- method;
- pass signal;
- falsification signal;
- current evidence state.

### 8. Validation Plan

| Priority | Question | Evidence needed | Lowest-cost method | Success signal | Falsification signal | Next decision |
|---:|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Prioritize questions that can change the target user, product form, value mechanism, scope, or willingness to continue.

## Readiness Score

Score each item from 0 to 2. This is a conversation aid, not an objective scientific scale.

| Item | 0 | 1 | 2 |
|---|---|---|---|
| Primary user | everyone | broad label | behavior and scenario defined |
| Scenario | abstract | time or place only | trigger, context, and main task |
| Core task | feature request | broad goal | observable user progress |
| Obstacle | absent | generic pain | specific failing step and consequence |
| Evidence status | all treated as fact | partly marked | E/H/D/U consistently visible |
| Value hypothesis | feature bundle | benefit named | mechanism, user, and consequence linked |
| Scope | absent | partial limitations | Must/Should/Won't and anti-goals |
| Differentiation | style words | concept slogan | mechanism differs from workaround |
| Success criteria | preference language | partly observable | checkable with stage and method |
| Validation | none | generic research | prioritized test and falsification signal |

Interpretation:

- `0–9`: do not enter concept generation; clarify the project first.
- `10–13`: provisional brief; conduct the highest-risk validation before broad exploration.
- `14–17`: ready for targeted research and controlled concept work.
- `18–20`: unusually clear early brief; remain open to revision when new evidence arrives.

Do not use the score to hide a critical zero. If target user, core task, or evidence status is zero, state the blocking risk even when the total score is high.

## Audit Output

When auditing, classify findings as:

- `keep`: clear and adequately supported;
- `downgrade`: rewrite an apparent fact as a hypothesis;
- `clarify`: wording or ownership is ambiguous;
- `test`: evidence is required before the next decision;
- `remove`: irrelevant, contradictory, or outside scope;
- `decide`: enough information exists, but the team has not made the choice.

End with:

1. the three highest-risk issues;
2. the smallest next validation action;
3. the decision that action will unlock;
4. the explicit readiness status.
