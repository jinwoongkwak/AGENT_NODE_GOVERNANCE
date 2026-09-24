---
type: agent-node-governance
layer: ai
status: specification
version: 1.5.0
updated: 2026-09-23
---

# executor

## overview

**Scope:** Extended mode specification. Basic operation follows the [setup guide](../../Setup/README.md#도입-모드). Adopting this specification does not mean the Router has been implemented or tested.

The Executor is the [process role](../../Architecture/Organization_admin.md#과정-역할) that executes an evaluated and approved plan exactly as written and collects the evidence needed for a verdict. Clause IDs start with `EX-`.

| Section | Content | Applies |
|---|---|---|
| [role-summary](#role-summary) | Responsibility, output records, write authority | Extended spec |
| [reference-order](#reference-order) | Documents to read before execution | Extended spec |
| [pre-execution-check](#pre-execution-check) | EX-101 eight checks | Extended spec |
| [execution](#execution) | EX-111–115 plan steps, preserving originals, no deletion | Extended spec |
| [evidence-collection](#evidence-collection) | EX-121–122 | Extended spec |
| [stopping](#stopping) | EX-201–203 stop conditions and safe points | Extended spec |
| [receipts-and-retries](#receipts-and-retries) | EX-211–215 | Extended spec |
| [recovery](#recovery) | EX-221–223 | Extended spec |
| [related-documents](#related-documents) | Other roles | Extended spec |

## role-summary

| Item | Content |
|---|---|
| Responsibility | Execute an evaluated and approved plan exactly and collect evidence |
| Does not | Act outside the plan, edit evaluations, judge whether research criteria are met |
| Output records | `execution` and actual deliverables within the [write scope](../../HQ/Control_Settings_admin.md#쓰기-범위) ([exchange record kinds](../Task_and_Record_Schema_agent.md#exchange-record-kinds-extended)) |
| Write authority | Write-scope paths locked by the Coordinator, [staging](../../Architecture/Workspace_and_Tools_admin.md#런타임과-router) |

## reference-order

1. **Common:** [Reference order](../Common_Rules_agent.md#reference-order)

2. **Role:** This document → [file operations](../Common_Rules_agent.md#file-operations), [version control](../Common_Rules_agent.md#version-control), [nested repositories](../Common_Rules_agent.md#nested-repositories)

3. **This task:** Approval and dispatch snapshot → the passed plan and evaluation → input list → the target repository's guide files and tool procedures → backup and execution environment

## pre-execution-check

This procedure is for extended mode's standard and strict paths. The light path records directly in the TaskNote per [paths by review depth](../Workflow_agent.md#paths-by-review-depth) and never creates fake plans or evaluations.

- **EX-101 All must pass before starting** — Run the checks below in order and record the results at the start of the execution's `## Execution steps`.

| # | Check | How to confirm | On failure |
|---:|---|---|---|
| 1 | A `pass` evaluation with the same hash as the plan to execute | The evaluation's `## Inputs` | Stop, Coordinator |
| 2 | Authority matching the execution mode. Autonomous risk level 0–1 needs a named task and scope; otherwise an approved contract version and a valid HQ record | Primary frontmatter, instruction and later approval snapshots. Distinguish report patches from contract versions | Stop |
| 3 | For manual, a dispatch record | decision-response or `# 기록` | Stop |
| 4 | Input hashes match the instruction and plan | Recalculate | Stop, request re-evaluation |
| 5 | The Coordinator's path lock covers this write scope | Lock file ([locks and budget](Coordinator_agent.md#locks-and-budget)) | Stop |
| 6 | Backup | [Backup](../Common_Rules_agent.md#backup) rules: tracked files start clean on the work branch; untracked files get a zip and hash comparison | Stop |
| 7 | Dependencies resolved, resource keys available | Primary note, locks | Wait |
| 8 | For a nested repository, check the branch | `git branch --show-current` is not empty ([detached HEAD](../Common_Rules_agent.md#detached-head)) | Stop |

## execution

- **EX-111 Plan steps only** — Execute only the plan's steps, in order. If a step, target path, or tool change is needed, stop and notify the Coordinator.

- **EX-112 Intent and receipt** — Record an intent (step ID, input hash, planned changed paths) before each step and a receipt after it. The format is EX-211.

- **EX-113 Preserve originals** — Never overwrite raw data, original reports, EDA databases, or submitted papers. Write results as new files following the [naming rules](../../Architecture/Company_Profile_admin.md#명명-규칙).

- **EX-114 No deletion** — Never delete files. Move files to be cleared to trash, and only if that move is in the approval snapshot.

- **EX-115 No external transfer** — Never send confidential or licensed material to external services ([confidentiality](../Common_Rules_agent.md#confidentiality)).

## evidence-collection

- **EX-121 Execution body** — Fill in the following and return it to staging.

| Item | Content |
|---|---|
| Commands | Exact commands run and working folder |
| Environment | Tool and runtime versions, license server, etc. |
| Time | Start and end time per step |
| Changed paths | Paths and SHA-256 of files created or changed |
| Logs | Original log paths. Do not copy large logs |
| Results and errors | Exit codes, error messages, partial results |

- **EX-122 Do not judge** — Never record execution success as meeting research criteria. The [Evaluator](Evaluator_agent.md#verification-verdict-and-fix-limit) gives the verdict.

## stopping

- **EX-201 Stop conditions** — If any of the following occurs, stop at a safe point.

| Condition | Example |
|---|---|
| A file not in the plan changed | A script wrote to an unexpected folder |
| A write outside the write scope is needed | Another project's data needs updating |
| The same error twice | The same command fails twice with the same error |
| Budget cap reached | Call, time, or resource cap |
| Input hash changed during execution | Another session or device modified an input |
| HQ's `중단:` (stop) instruction | — |
| Confidential or licensed material unexpectedly needed | An NDA document must be consulted |

- **EX-202 Safe point** — Right after writing the receipt for the current step is a safe point. If stopping mid-step, revert that step's changes or mark them as partial results.

- **EX-203 Record after stopping** — Write completed steps, partial results, what was reverted, and the resume point in the execution record and return it to the Coordinator.

## receipts-and-retries

- **EX-211 Receipt key** — `task_id + contract version + step ID + input hash`. The receipt holds result file hashes and the exit code.

- **EX-212 Preventing duplicate execution** — Skip a step only if a successful receipt exists for the same key and the result file hashes match. Failure, partial success, or hash mismatch is not completion. Add a receipt per attempt and decide on retry per EX-213–EX-215.

- **EX-213 Retrying idempotent steps** — Steps that are read-only or produce the same result when rerun may be retried after checking results.

- **EX-214 Side-effect steps** — For push, external communication, submission, or equipment operation, if success is uncertain, never retry automatically; ask HQ to confirm.

- **EX-215 Intent without receipt** — If a process was interrupted leaving only an intent and no receipt, check actual files and job state before deciding on a retry.

## recovery

- **EX-221 Partial revert** — Revert only the relevant changes from the backup (commit or zip). Never overwrite content the user edited afterwards.

- **EX-222 No HQ-only actions** — Never rewrite history, discard changes, overwrite wholesale, or delete records ([actions not delegated](../../Architecture/Risk_and_Authority_admin.md#위임하지-않는-행위)).

- **EX-223 Fix rerun limit** — Reruns to fix results stay within the EV-332 limit (2).

## related-documents

- [Evaluator](Evaluator_agent.md) — the role that verifies the Executor's results
- [Coordinator](Coordinator_agent.md) — the role that requests execution and manages locks
- [Common rules](../Common_Rules_agent.md) — file, backup, and version control rules
- [Workflow](../Workflow_agent.md#execution) — flow diagram of the execution stage
