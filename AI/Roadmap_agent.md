---
type: agent-node-governance
layer: ai
status: active
version: 1.6.0
updated: 2026-09-23
---

# roadmap

## overview

How an agent writes, checks, and submits project and portfolio roadmaps. A roadmap states where a project is going and its next three steps; STATUS keeps only the current state. Every roadmap passes the [independent check](Workflow_agent.md#independent-check) before HQ approval.

| Section | Content | Applies |
|---|---|---|
| [inputs](#inputs) | Evidence a roadmap may use | Operating manual |
| [project-roadmap](#project-roadmap) | Content of `ROADMAP.md` for one project | Operating manual |
| [portfolio-roadmap](#portfolio-roadmap) | Content of the portfolio roadmap and trend research | Operating manual |
| [roadmap-check](#roadmap-check) | Scorecard and loop for the independent check | Operating manual |
| [hq-approval](#hq-approval) | Proposal, approval, and what changes afterwards | Operating manual |
| [revisit](#revisit) | When a roadmap is updated | Operating manual |
| [related-documents](#related-documents) | Workflow, templates, review | Operating manual |

## inputs

| Source | Use |
|---|---|
| Project README Success criteria, STATUS, `10_NOTES/Decisions.md` | Goals, current state, fixed decisions |
| `10_NOTES/`, repositories and data indexes named by CONTEXT | Completed work and evidence |
| Archived tasks of the project (for example `90_ARCHIVE/Tasks/Research/`) | What has been done and when |
| Open TaskNotes that name the project | Work already in flight |
| Advisor and meeting notes named by the project | External expectations |

- **Confidential areas:** Never open or pass [confidential areas](../Architecture/Company_Profile_admin.md#기밀-영역) unless the task names the path ([confidentiality](Common_Rules_agent.md#confidentiality)).

- **No invention:** A goal, date, or owner without a source goes to `HQ 검토 필요`, never into the roadmap body.

## project-roadmap

A project roadmap lives at `<projects-folder>/<id>/ROADMAP.md` and follows the [project roadmap template](../Setup/Templates_agent.md#project-roadmap). It is written in Korean because HQ reads it.

| Part | Required content |
|---|---|
| 목표 | Research objective and success criteria, quoted from the README with links |
| 완료한 것 | Completed work with dates and evidence links |
| 현재 위치 | Current state and blockers, consistent with STATUS |
| 다음 단계 | **Exactly three** steps in order. Each has an owner, first action, completion condition, evidence link, and target date or `추정` |
| 일정 | Mermaid Gantt when dates exist; estimated dates are labeled `추정` |
| HQ 검토 필요 | Every ambiguity, missing input, or roadblock, each with a question and options |
| 근거 | List of files the roadmap relies on |

- **Scope:** Next steps stay inside the project's scope and write authority. A step that needs a risk-level-2 action is marked `승인 필요`.

- **STATUS:** Changes to STATUS frontmatter that the roadmap implies are proposed in the decision table only ([canonical promotion check](../HQ/Review_and_Closure_admin.md#정본-승격-확인)).

## portfolio-roadmap

The portfolio roadmap lives at `00_HQ/Portfolio_Roadmap.md` and follows the [portfolio roadmap template](../Setup/Templates_agent.md#portfolio-roadmap). It is written only after the project roadmaps it aggregates are approved.

| Part | Required content |
|---|---|
| Project summary | One row per active project: goal, phase, next step, date, link to its roadmap |
| Connections | Technical and strategic links, synergies, and overlaps between projects, as a Mermaid flowchart and a table |
| Trends | Research trends of the last five years by topic, as a Mermaid timeline and a table with venue, year, and source |
| Next research direction | One proposed direction with rationale, marked as an AI recommendation |
| Bridge | How past, current, and planned projects lead to that direction, as a Mermaid flowchart |
| Schedule | Mermaid Gantt across projects; estimated dates labeled `추정` |
| HQ decisions | Short list of items HQ must decide, at the end |

- **Trend research window:** Five years back from the writing date, unless HQ sets another window.

- **Search queries:** Use public topic keywords only. Never put confidential, NDA, PDK, or unpublished project content into a query.

- **Sources:** Cite venue, year, and link for each trend claim. Separate facts from estimates ([fact, estimate, recommendation](Reporting_Style_agent.md#fact-estimate-recommendation)).

## roadmap-check

Roadmaps use the [independent check](Workflow_agent.md#independent-check) loop with this scorecard. The checker records findings in the EV-121 format.

| Item | Weight | Meaning of 5 points |
|---|---:|---|
| Objective alignment | 25 | Every step and milestone traces to README success criteria, STATUS, or Decisions; nothing invented |
| Evidence traceability | 25 | Every fact links a source; facts and estimates are labeled |
| Feasibility and dependencies | 20 | Blockers, external dependencies, and capacity are handled; dates are sourced or marked `추정` |
| Next-step actionability | 20 | Exactly three steps, each with owner, first action, and completion condition |
| HQ-review completeness | 10 | Every ambiguity or roadblock appears under `HQ 검토 필요` with a question and options |

- **Pass:** Every item 4/5 or higher and 0 blocking findings.

- **Blocking:** An invented fact, goal, or date; a step outside the project's scope or needing unflagged risk-level-2 action; confidential content; a missing HQ-review item that blocks a step.

- **Limit:** At most three check rounds. The same blocking finding in two consecutive rounds ends the loop early ([iteration limit](Roles/Evaluator_agent.md#iteration-limit)).

- **Exit:** On pass or at the limit, submit to HQ with the last verdict and any unresolved findings.

## hq-approval

| Step | Rule |
|---|---|
| Proposal | One TaskNote per roadmap, `to-do / {hq-owner} / decide`, with the draft, check summary, and a decision table of 10 or fewer HQ items |
| Approval | HQ approves a version or orders a revision. Only then does the agent write `ROADMAP.md` or `Portfolio_Roadmap.md` and set `approved_version` |
| Revision | A revision request starts a new version and a new check loop |
| Records | Check summaries go to the TaskNote `# 기록` in Korean; full checker output in English goes where the task names |

## revisit

Roadmaps are canonical documents updated on events, not periodic planning notes. Update a roadmap when one of these occurs:

- HQ asks for it.
- The project's `phase` or success criteria change.
- A decision in the project's Decisions changes a next step.
- All three next steps are done or blocked.

## related-documents

- [Workflow](Workflow_agent.md#independent-check) — the independent check loop
- [Initial templates](../Setup/Templates_agent.md#project-roadmap) — roadmap templates
- [Review and closure](../HQ/Review_and_Closure_admin.md) — how HQ reviews results
- [AI guide](README.md) — list of AI documents
