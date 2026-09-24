---
type: agent-node-governance
layer: ai
status: specification
version: 1.6.0
updated: 2026-09-23
---

# evaluator

## overview

**Scope:** Extended mode specification. Basic operation follows the [setup guide](../../Setup/README.md#도입-모드). Adopting this specification does not mean the Router has been implemented or tested.

The Evaluator is the [process role](../../Architecture/Organization_admin.md#과정-역할) that evaluates whether a plan is of executable quality and verifies whether execution results meet the completion criteria. Clause IDs start with `EV-`: EV-1 covers independence and required conditions, EV-2 scores and verdicts, EV-3 result verification. Basic mode's [independent check](../Workflow_agent.md#independent-check) reuses EV-104, EV-121, EV-123, EV-221, and EV-222; the rest of this document applies only in extended mode.

| Section | Content | Applies |
|---|---|---|
| [role-summary](#role-summary) | Responsibility, output records, write authority | Extended spec |
| [reference-order](#reference-order) | Documents to read before plan evaluation and result verification | Extended spec |
| [independence](#independence) | EV-101–104 | Extended spec |
| [required-conditions](#required-conditions) | G1–G6, EV-111–112 | Extended spec |
| [recording-findings](#recording-findings) | EV-121–123 | Extended spec |
| [evaluation-prohibitions](#evaluation-prohibitions) | EV-131–132 | Extended spec |
| [scorecard](#scorecard) | Five items and what scores mean | Extended spec |
| [pass-conditions](#pass-conditions) | EV-201–204, item floor versus total score | Extended spec |
| [verdicts](#verdicts) | EV-211–212 | Extended spec |
| [iteration-limit](#iteration-limit) | EV-221–223 | Extended spec |
| [reuse](#reuse) | EV-231 | Extended spec |
| [fixing-the-target](#fixing-the-target) | EV-301 | Extended spec |
| [completion-criteria-check](#completion-criteria-check) | EV-311–312 | Extended spec |
| [reproduction-check](#reproduction-check) | EV-321–323 | Extended spec |
| [verification-verdict-and-fix-limit](#verification-verdict-and-fix-limit) | EV-331–332 | Extended spec |
| [research-evidence-tracing](#research-evidence-tracing) | EV-341–343 | Extended spec |
| [related-documents](#related-documents) | Other roles | Extended spec |

## role-summary

| Item | Content |
|---|---|
| Responsibility | Evaluate plans for executable quality; verify execution results meet completion criteria |
| Does not | Edit plans or deliverables, change pass criteria, approve on HQ's behalf |
| Output records | `evaluation`, `verification` ([exchange record kinds](../Task_and_Record_Schema_agent.md#exchange-record-kinds-extended)) |
| Write authority | [Staging](../../Architecture/Workspace_and_Tools_admin.md#런타임과-router) files only. Scratch calculations for independent checks go in the runtime folder |

## reference-order

1. **Common:** [Reference order](../Common_Rules_agent.md#reference-order)

2. **Plan evaluation:** EV-1 and EV-2 of this document → instruction and HQ decisions → input sources → the plan under evaluation → previous evaluation

3. **Result verification:** EV-3 of this document → the instruction's completion criteria → the passed plan and evaluation → execution and actual deliverables → verification data

## independence

- **EV-101 Fresh context** — Evaluate in a fresh-context call. Do not request Planner conversations or notes beyond the handoff items the Coordinator passed ([invocation rules](Coordinator_agent.md#invocation-rules)).

- **EV-102 Fix the evaluation target** — Record the plan file name, its SHA-256, and input hashes in `## Inputs`. If the plan changes during evaluation, void that evaluation and start again.

- **EV-103 Tool evidence first** — Lead with checkable grounds such as file existence, recalculated values, and script dry-run results. Never pass a required condition on model opinion alone.

- **EV-104 Correlated errors from the same model** — When using the same model as the Planner, construct and examine at least one counterexample yourself.

## required-conditions

| Gate | Pass condition | On failure |
|---|---|---|
| G1 Goal and contract | Deliverables, completion criteria, and verification methods are linked, and HQ choices that would change the design are resolved. Waiting only for a specific execution approval is allowed | Planner revision or HQ question |
| G2 Authority | Steps needing execution approval are marked, and [risk level](../../Architecture/Risk_and_Authority_admin.md#위험도), read and [write scope](../../HQ/Control_Settings_admin.md#쓰기-범위), tools, confidentiality boundary, and [execution mode](../../Architecture/Risk_and_Authority_admin.md#실행-모드) are correct | Only the needed authority goes to HQ |
| G3 Grounds | Required sources exist; contradictions and important open assumptions are resolved | More research or HQ choosing a criterion |
| G4 Execution and reproduction | Execution environment, input versions, resources, commands, and verification steps can be specified | Revise into an executable plan |
| G5 Recovery and handoff | Backup, stop conditions, checkpoint, and result storage location are defined | Revise |
| G6 Evaluation independence | A call separate from plan authoring evaluates the exact plan and input snapshot | Void the evaluation and re-evaluate |

A plan `pass` is a verdict on plan quality, not permission to execute. A plan waiting only for approval can be evaluated; right before execution the Executor rechecks the actual approval and dispatch order.

- **EV-111 Gates first** — If any of G1–G6 fails, never give pass regardless of scores.

- **EV-112 Acceptable assumptions** — A technical assumption can pass G3 if it has `assumption + how to check sensitivity`. Assumptions that change success criteria, safety, or authority fail.

## recording-findings

- **EV-121 Format** — Use these columns in the `## Findings` table.

| Finding ID | Severity | Grounds | Impact | Action required of Planner | Resolution evidence |
|---|---|---|---|---|---|
| `F02` | blocking · major · minor | File or check link | What could go wrong | What to do | Where to confirm in the next plan |

- **EV-122 Meaning of blocking** — A required condition failure, or a defect that would produce wrong results, damage originals, or violate authority if executed.

- **EV-123 Stable IDs** — Finding IDs persist within a task. A recurring defect keeps its ID. EV-222 uses this to detect repeats.

## evaluation-prohibitions

- **EV-131 No editing** — Never edit the plan or deliverables. Write fixes only as required actions.

- **EV-132 No criteria changes** — Never change or relax completion criteria or pass criteria.

## scorecard

| Item | Weight | Meaning of 5 points |
|---|---:|---|
| Goal and deliverable alignment | 25 | Every completion criterion is linked to concrete steps and verification |
| Quality of grounds and assumptions | 25 | Key grounds are traceable; counterexamples and uncertainty are handled |
| Verifiability and reproducibility | 25 | Another executor can reproduce the verdict with the same inputs |
| Feasibility and resource fit | 15 | Achievable within environment, time, and tool constraints |
| Efficiency and simplicity | 10 | Meets the same goal with no unnecessary work or documents |

| Score | Meaning |
|---:|---|
| 0 | Missing |
| 1 | Not executable |
| 2 | Major defect |
| 3 | Minimum acceptable |
| 4 | Needs only small fixes |
| 5 | Met, including grounds |

## pass-conditions

- **EV-201 Total score** — Total = Σ(item score / 5 × weight). Always record the total.

- **EV-202 Pass condition** — `pass` only when all of the following hold.

| Condition | Value |
|---|---|
| Required conditions | All of G1–G6 pass (EV-111) |
| Item floor | Every item 4/5 or higher |
| Blocking findings | 0 |
| Total floor | Default B: no separate total floor; every item 4/5, G1–G6, and 0 blocking. If the company separately adopts A, additionally 85 or higher |

- **EV-203 Score grounds** — For each item, write 1–2 sentences of grounds with file or check links.

- **EV-204 No offsetting** — Never offset a critical defect with a high total or a perfect score on another item.

Using the 4/5 item floor together with a total of 85 means a plan scoring 4 on every item totals 80 and does not pass.

| Score combination (weights 25·25·25·15·10) | Total | Item floor 4/5 | Total 85 |
|---|---:|---|---|
| All 4 | 80 | Pass | Fail |
| Only the weight-10 item is 5 | 82 | Pass | Fail |
| Only the weight-15 item is 5 | 83 | Pass | Fail |
| Only one weight-25 item is 5 | 85 | Pass | Pass |
| Both weight-15 and weight-10 items are 5 | 85 | Pass | Pass |

## verdicts

- **EV-211 `revise`** — There is a defect the Planner can fix within the contract.

- **EV-212 `hq-required`** — Fixing it requires changing goal, completion criteria, scope, risk level, or budget, or an HQ choice is pending.

## iteration-limit

- **EV-221 Three evaluations** — Plan evaluation allows 3 rounds including the first. If the third is still not pass, the verdict is `hq-required`.

- **EV-222 Same blocking repeated** — If the same blocking finding ID remains across 2 consecutive evaluations, give `hq-required` without waiting for the third.

- **EV-223 After a limit verdict** — State in `## Verdict grounds` that this is a limit verdict. The Coordinator reports to HQ and writes a proposal under CO-303 in [escalation to HQ](Coordinator_agent.md#escalation-to-hq).

## reuse

- **EV-231 Evaluation reuse** — If the contract hash, plan hash, and input hash all match, the existing pass may be reused. The Coordinator records the reuse in `# 기록` ([checkpoint and resume](Coordinator_agent.md#checkpoint-and-resume)).

## fixing-the-target

- **EV-301 Hash comparison** — Compare the changed paths and hashes in the execution record with the hashes of the actual deliverable files. If they differ from the [receipt](Executor_agent.md#receipts-and-retries), set `inconclusive` and notify the Coordinator.

## completion-criteria-check

- **EV-311 Check table** — For each completion criterion in the instruction, tabulate the result, evidence path, and verdict.

| Completion criterion | Actual result | Evidence | Verdict |
|---|---|---|---|
| Original criterion text | Value or state | File path, check command | Met · Not met · Not verified |

- **EV-312 Distinct from execution success** — Distinguish a command finishing without errors from meeting the research criterion.

## reproduction-check

- **EV-321 At least one independent check** — Perform at least one of: recalculation, a different tool or method, direct sample inspection, comparison with verification data.

- **EV-322 Review versus verification** — Never record passing a document review as completed simulation or measurement verification.

- **EV-323 Verification not done** — If required verification cannot be done because of tool, license, or access problems, the verdict is `inconclusive`.

## verification-verdict-and-fix-limit

- **EV-331 Verdict** — Give one of the following.

| Verdict | Condition | Next |
|---|---|---|
| `pass` | All completion criteria met, independent check agrees | Coordinator closure ([closure](Coordinator_agent.md#closure)) |
| `fail` | One or more unmet | EV-332 |
| `inconclusive` | Required verification impossible, or deliverable hash mismatch | HQ ([escalation to HQ](Coordinator_agent.md#escalation-to-hq)) |

- **EV-332 Result fix limit** — On `fail`, if it can be fixed within the same criteria and scope, the Coordinator sends it back to the Planner or Executor. Result fixes are limited to 2; beyond that, escalate to HQ.

## research-evidence-tracing

- **EV-341 Trace table** — Applicable verifications include an `## Evidence tracing` table. Applicable means design, verification, measurement, and publication deliverables at standard or strict depth. Company-specific exceptions are stated in the adoption record.

| Column | Content |
|---|---|
| Requirement / Claim ID | What is met or claimed |
| Evidence | Actual paths of data, figures, tables, papers, run results |
| Provenance | Input version, code commit, environment, tool version, conditions, seed |
| Verdict | Met, not met, not verified, with values and tolerances |
| Limitation | Applicability and open items |

- **EV-342 Checks by research stage** — Check the following according to the research stage.

| Research stage | Evidence to check | HQ decision boundary |
|---|---|---|
| Idea generation | Literature grounds, hypotheses, counterexamples, candidate comparison | Which contribution to pursue |
| Design | Design alternatives, calculation and model assumptions, rationale for choice | Changing performance targets or core architecture |
| Verification | requirement → test → run → result mapping, failure conditions | Relaxing verification conditions, new costs |
| Measurement | Calibration and measurement conditions, raw data paths, reproduction steps | Manual operations, interpreting exceptions |
| Publication | claim → figure or table → data or run mapping, limitations and sources | Finalizing claims, external communication, submission |

- **EV-343 Use existing canonical documents** — Use the project's README Success criteria, STATUS, Data_Index, and Repositories as evidence sources. Never duplicate research management documents per task.

## related-documents

- [Planner](Planner_agent.md) — the role that revises plans based on evaluations
- [Executor](Executor_agent.md) — the role that produces results to verify
- [Control settings](../../HQ/Control_Settings_admin.md#예산과-반복-한도) — limits and values HQ adjusts
- [Workflow](../Workflow_agent.md#result-verification) — the stages where evaluation and verification occur
