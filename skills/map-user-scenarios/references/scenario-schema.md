# Scenario Research Schema

Use this reference for a complete saved package or a detailed audit.

## 1. Source Index And Evidence Boundary

For each source record:

| Field | Requirement |
|---|---|
| Source ID | Stable ID such as OBS-01 or INT-03 |
| Type | Observation, interview, diary, system log, document, or assumption |
| Date and sample | Preserve when known; mark unknown rather than inventing |
| Original record | Link, path, or concise verbatim excerpt |
| What it supports | The narrow claim this source can support |
| What it cannot support | Generalizations or causes not established by the source |

State the decision being supported and the sample boundary before synthesis.

## 2. Behavioral User Model

Define users with variables that could change the product decision:

- environment and mobility;
- task frequency and duration;
- concurrency or workload;
- intervention and confirmation frequency;
- tool, device, and collaboration context;
- switching and recovery cost;
- error or safety consequence;
- tolerance for visual, sound, haptic, or physical feedback.

Return primary, adjacent, edge, and non-priority users. Attach E/H/D/U labels and source IDs.

## 3. Six-Frame Scenario

1. `Background`: environment, tools, and conditions before the event.
2. `Main task`: what the user is trying to preserve or complete.
3. `Delegation or setup`: the supporting task placed in motion.
4. `State change`: the observable event that creates a need to decide.
5. `Intervention decision`: why the user acts now, later, or not at all.
6. `Recovery`: how the user returns to the main task and what context must be restored.

For each frame include evidence status, source IDs, unknowns, and design relevance. Avoid product features unless they are existing workarounds.

## 4. Task Flow And Breakdown Map

For every step record:

| Step | Trigger | User action | System or other actor | Information available | Breakdown or workaround | Consequence | Recovery |
|---|---|---|---|---|---|---|---|

Mark decision points, loops, handoffs, waiting, interruptions, errors, and abandoned actions.

## 5. State And Attention Matrix

Use attention levels only when interruption or ambient awareness matters:

- `L0 Silent`: no awareness needed now.
- `L1 Ambient`: awareness without a required response.
- `L2 Noticeable`: should be reviewed at a suitable stopping point.
- `L3 Interruptive`: prompt intervention because delay has meaningful consequence.

For each system state record default level, escalation and downgrade conditions, suitable feedback channels, available action, false-alert risk, and missed-alert risk. A state change alone does not determine urgency.

## 6. Scenario Priority

Score only when it helps compare alternatives. Suggested 1–5 dimensions:

```text
priority = frequency + consequence + product relevance + evidence strength - implementation complexity
```

Keep a reason and source beside every score. Treat the total as a discussion aid, not objective truth. Identify the largest uncertainty and lowest-cost falsification test.

## 7. Audit Classification

Classify findings as:

- `Critical`: invented evidence, unsupported generalization, or no observable problem event.
- `Major`: vague user definition, missing task chain, solution-first scenario, or missing recovery.
- `Minor`: inconsistent terminology, weak source linkage, or unclear prioritization reason.
- `Open question`: missing information that requires new observation or a project decision.

End with one judgment: ready for concept framing, provisionally usable with named limits, or not ready.
