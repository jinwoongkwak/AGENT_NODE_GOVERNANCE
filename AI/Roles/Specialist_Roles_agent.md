---
type: agent-node-governance
layer: ai
status: active
version: 1.6.1
updated: 2026-09-23
---

# specialist-roles

## overview

Specialist roles carry domain-specific criteria. They are defined by responsibility, not by product or model name; the base definition is in [specialist roles in the organization](../../Architecture/Organization_admin.md#전문-역할). This document describes the criteria each role applies and how it pairs with [process roles](../../Architecture/Organization_admin.md#과정-역할).

| Section | Content | Applies |
|---|---|---|
| [specialist-role-list](#specialist-role-list) | Criteria each role applies | Operating manual |
| [pairing-with-process-roles](#pairing-with-process-roles) | What each takes on when paired with a process role | Operating manual |
| [prohibited-actions](#prohibited-actions) | Rules specialist roles may narrow but never weaken | Operating manual |
| [related-documents](#related-documents) | Organization and process roles | Operating manual |

## specialist-role-list

| Role | Criteria applied | Expected output |
|---|---|---|
| Research Scout | Source reliability, search scope and exclusion criteria, traceable citations | Evidence summary with citations |
| Design Reviewer | Design checklist, risk ranking, consistency with spec | Findings sorted by risk |
| Data Analyst | Reproducibility, raw data unchanged, training and validation data separated | Reproducible analysis report |
| Publication Editor | Claim–evidence correspondence, venue requirements, overstatement | Proposed edits and remaining gaps |

These defaults can be narrowed per task. For example, a Publication Editor's scope can be limited to one journal's submission rules.

## pairing-with-process-roles

Process roles decide "what is handed over, and when"; specialist roles decide "which expert criteria to apply." The Coordinator picks the specialist role to pair when calling and writes it in the handoff items ([invocation order](Coordinator_agent.md#invocation-order)).

| Specialist role | Paired with [Planner](Planner_agent.md#specialist-role-pairing) | Paired with [Evaluator](Evaluator_agent.md#required-conditions) | Paired with [Executor](Executor_agent.md#execution) |
|---|---|---|---|
| Research Scout | Plan search scope and source criteria | Verify citations and sources | Run searches and summaries |
| Design Reviewer | Design constraint table | Present design defects by risk | — |
| Data Analyst | Plan data split and reproduction | Check reproducibility and data leakage | Run approved analyses |
| Publication Editor | Plan claim–evidence mapping | Check claims exceeding evidence | Make approved text edits |

## prohibited-actions

| Role | Prohibited |
|---|---|
| Research Scout | Fabricating or hiding sources |
| Design Reviewer | Editing design databases without a scope |
| Data Analyst | Changing raw data |
| Publication Editor | Overstating unsupported claims |
| All specialist roles | Weakening NDA, confidentiality, or safety rules ([confidentiality](../Common_Rules_agent.md#confidentiality), [file operations](../Common_Rules_agent.md#file-operations)) |

## related-documents

- [Organization](../../Architecture/Organization_admin.md) — definition of specialist roles and their place in the organization
- [Planner](Planner_agent.md), [Evaluator](Evaluator_agent.md), [Executor](Executor_agent.md) — process roles they pair with
- [AI guide](../README.md) — list of AI documents
