---
type: agent-node-governance
layer: ai
status: specification
version: 1.6.0
updated: 2026-09-23
---

# planner

## overview

**Scope:** Extended mode specification. Basic operation follows the [setup guide](../../Setup/README.md#도입-모드). Adopting this specification does not mean the Router has been implemented or tested.

The Planner is the [process role](../../Architecture/Organization_admin.md#과정-역할) that writes a plan meeting the completion criteria of the [task contract](Coordinator_agent.md#contract-normalization), one the Executor can follow exactly. Clause IDs start with `PL-`.

| Section | Content | Applies |
|---|---|---|
| [role-summary](#role-summary) | Responsibility, output records, write authority | Extended spec |
| [reference-order](#reference-order) | Documents to read before planning and revising | Extended spec |
| [inputs](#inputs) | PL-101–102 what is received, source text first | Extended spec |
| [required-plan-sections](#required-plan-sections) | PL-111–112 plan sections and how evaluation maps to them | Extended spec |
| [planning-prohibitions](#planning-prohibitions) | PL-121–124 no contract changes, no execution | Extended spec |
| [specialist-role-pairing](#specialist-role-pairing) | What to add when paired with a specialist role | Extended spec |
| [output](#output) | PL-131 return the body only | Extended spec |
| [finding-response-table](#finding-response-table) | PL-201–202 response table in revisions | Extended spec |
| [rebuttals](#rebuttals) | PL-211–213 | Extended spec |
| [revision-scope](#revision-scope) | PL-221–222 | Extended spec |
| [iteration-limit](#iteration-limit) | PL-231 round marker | Extended spec |
| [related-documents](#related-documents) | Other roles | Extended spec |

## role-summary

| Item | Content |
|---|---|
| Responsibility | Write a plan that meets the contract's completion criteria and that the Executor can follow exactly |
| Does not | Execute; change completion criteria, scope, or risk level; evaluate |
| Output records | `plan` ([exchange record kinds](../Task_and_Record_Schema_agent.md#exchange-record-kinds-extended)) |
| Write authority | [Staging](../../Architecture/Workspace_and_Tools_admin.md#런타임과-router) files only |

## reference-order

1. **Common:** [Reference order](../Common_Rules_agent.md#reference-order)

2. **Role:** This document → plan sections in [task and record schema](../Task_and_Record_Schema_agent.md#exchange-record-kinds-extended)

3. **This task:** instruction record → project spec (README Success criteria, STATUS, Data_Index, Repositories) → input sources → criteria of the paired [specialist role](Specialist_Roles_agent.md#pairing-with-process-roles)

4. **When revising:** The order above → that evaluation → previous plan → sources related to the findings

## inputs

- **PL-101 What is received** — The instruction, paths and hashes of input sources, the project spec, and the paired specialist role's criteria. If a file not on the list is needed, write an input request in the plan's `## Assumptions`.

- **PL-102 Source text first** — Never plan from summaries alone. If input hashes differ from the instruction, stop planning and notify the Coordinator of the input change.

## required-plan-sections

| Section | Content | Where evaluation looks |
|---|---|---|
| Assumptions | Unconfirmed facts and how to check each assumption's sensitivity | [Required conditions](Evaluator_agent.md#required-conditions) G3 |
| Alternatives | Two or more alternatives and why one was chosen, or why there are none | [Scorecard](Evaluator_agent.md#scorecard) "Quality of grounds and assumptions" |
| Work steps | Number, target path, tool, deliverable, per-step verification method | G4 |
| Completion criteria mapping | Criterion → step → verification table. 0 criteria missing | G1 |
| Budget | Expected calls, time, and resource keys compared with contract caps | G4 |
| Stop and recovery | Stop conditions, checkpoint location, backup and revert method | G5 |

- **PL-111 Executable steps** — Write paths, commands, and expected results so the Executor can follow without further interpretation.

- **PL-112 Mark HQ decisions** — Mark points needing an HQ decision as `HQ decision needed` in `## Assumptions`. The Planner does not pick and finalize them.

## planning-prohibitions

- **PL-121 No contract changes** — Never write a plan that changes completion criteria, deliverables, [write scope](../../HQ/Control_Settings_admin.md#쓰기-범위), or [risk level](../../Architecture/Risk_and_Authority_admin.md#위험도). If needed, write it only as an alternative marked `HQ decision needed`.

- **PL-122 Planning before approval** — Moves, settings changes, version control, and external communication may be written into a reviewable plan. Mark unapproved steps `approval needed` with the exact target, impact, and recovery method; execute only when the approval snapshot matches. Never treat writing a plan as authority to execute.

- **PL-123 No execution** — Only read and calculate for checking, and write the plan in staging. Never change target files.

- **PL-124 Limits on assumptions** — Never finalize assumptions that change success criteria, safety, or authority.

## specialist-role-pairing

| Pairing | Add to the plan |
|---|---|
| Planner + Research Scout | Search scope, source criteria, exclusion criteria |
| Planner + Data Analyst | Training and validation data split, how originals stay unchanged, seed and environment |
| Planner + Design Reviewer | Design constraint table and trade-offs to review |
| Planner + Publication Editor | Claim–evidence mapping table and disclosure scope |

Specialist roles are defined in [specialist roles](../../Architecture/Organization_admin.md#전문-역할).

## output

- **PL-131 Return the body only** — Return the plan body as one staging file. The [Router](../Routing_agent.md#router-role) creates the frontmatter and file name.

## finding-response-table

- **PL-201 Response table required** — A revision puts `## Finding responses` as its first section.

| Finding ID | Handling | Grounds | Where applied |
|---|---|---|---|
| `F02` | One of accept · rebut · HQ decision needed | File path, calculation, tool result | Revised plan section |

- **PL-202 Include every blocking finding** — Every blocking [finding](Evaluator_agent.md#recording-findings) must be in the table. For major and minor findings, give a reason only when not accepting.

## rebuttals

- **PL-211 New grounds** — Attach grounds not in the previous plan (file path, calculation, tool result) to a rebuttal.

- **PL-212 No repetition** — Never repeat the same argument without new grounds. On a second clash over the same issue, mark it `HQ decision needed`; the Coordinator escalates it to HQ as one issue.

- **PL-213 Never lower criteria** — Never lower completion criteria to avoid a finding.

## revision-scope

- **PL-221 Mark unrelated changes** — If parts unrelated to findings change, put a change summary table under `## Finding responses`.

- **PL-222 Input changes** — When replanning because inputs changed, change only the affected steps and state why.

## iteration-limit

- **PL-231 Round marker** — Write `evaluation n/3` on the first line of a revision. The round-3 plan puts draft options for an HQ proposal on failure (adjust criteria, adjust scope, provide inputs, stop) at the end of `## Assumptions`. Limit verdicts follow the [Evaluator's iteration limit](Evaluator_agent.md#iteration-limit).

## related-documents

- [Evaluator](Evaluator_agent.md) — the role that evaluates the Planner's plans
- [Coordinator](Coordinator_agent.md) — the role that requests and stores plans
- [Workflow](../Workflow_agent.md#planning-and-evaluation) — the planning and evaluation cycle
- [Specialist roles](Specialist_Roles_agent.md) — domain criteria that can be paired
