---
type: agent-node-governance
layer: setup
status: active
version: 1.5.0
updated: 2026-09-23
---

# material-placement-criteria

## overview

Check ownership, purpose, lifespan, and access restrictions before file extension. The same PDF goes to a different location with different permissions depending on whether it is a reference, a submitted version, or a manuscript under review.

| Section | Content | Applies |
|---|---|---|
| [decision-order](#decision-order) | Priority for classifying inputs | Operating manual |
| [placement-table](#placement-table) | Canonical location by material type | Operating manual |
| [mapping-table-and-execution](#mapping-table-and-execution) | Move, copy, and link rules | Operating manual |
| [exceptions-and-preservation](#exceptions-and-preservation) | Ambiguity, duplicates, confidentiality, repos | Operating manual |
| [related-documents](#related-documents) | Founding and migration | Operating manual |

## decision-order

1. **Authority:** Confirm you may read or move this material. Apply confidentiality, NDA, and license policies first.
2. **Ownership:** Decide who is responsible: a specific project, the company as a whole, institutional work, or a personal record.
3. **Purpose:** Decide whether it is active research, a reusable procedure, theory, a work instruction, raw evidence, or a final deliverable.
4. **Lifespan:** Ongoing material goes in its current area; closed or submitted originals go in a preservation location. Never archive something only because its date is old.
5. **Confidence:** If grounds are insufficient, stop automatic placement and leave it in place or in the approved INBOX.

## placement-table

| Material | Canonical location | Grounds and action |
|---|---|---|
| Company priorities, coordination, operating decisions | HQ index, Decisions | Information that coordinates several projects |
| Instructions, approvals, work progress | TaskNote | One note per task |
| Hypotheses, meetings, alternatives for a specific study | Project `10_NOTES/` | Confirm ownership via research question and project ID |
| Circuit, structure, design rationale | Project design area | Follow the existing company's design paths |
| Code repositories | Project source or shared repo area | Preserve Git repo boundaries and connect as submodules |
| Raw data, simulation, measurement | Approved original storage | Record location, version, conditions, and hash in the vault's Data_Index |
| Working copies of reports, presentations, papers | The project's reports/publications area | Keep traceability between raw data and claims and figures |
| Submitted or delivered versions | Project closeout or approved preservation location | Never overwrite; keep the exact version |
| Reusable procedures, equipment, EDA settings | Technical Wiki | Procedures other projects also use |
| Concepts, formulas, derivations, theory study | Theory Wiki | Explanations not tied to a specific project |
| Institutional administration and guides | Institutional area in the local profile | Optional area; not created automatically for a new company |
| Manuscripts under review, personal finances | Local confidential area | Never place in ordinary projects or public repos |
| Not yet classifiable | INBOX or in place | Record why it is undecided and who acts next |
| Closed projects | Archive | Move after HQ's archive decision, verifying links and repos |

An existing company's subfolder names are set by its local profile and CONTEXT. Never copy the same content into a new classification folder and create two canonical copies.

## mapping-table-and-execution

```text
원본 경로 | 소유 영역 | 기밀 등급 | 배치 근거 | 대상 경로
유지/링크/복사/이동/휴지통 | 원본 hash | 백업 | 승인 근거
영향 링크·Canvas·설정 | 실행 결과 | 최종 hash | 미확정 이유
```

Fix the mapping table (columns above, written in Korean for HQ) in the task note before actually moving material. If the user's request explicitly allowed that move, record the grounds and execute without asking for the same permission again. Moves that newly widen the scope are left as a separate decision.

Items that are certain from file names alone may be classified by path, project ID, and index. Inspect content only within the allowed scope, and record the grounds and original location.

## exceptions-and-preservation

- Compare duplicate candidates by hash and confirm canonical ownership. Never permanently delete something just because it is identical.
- Never move a Git repo in a file explorer. Handle `git mv`, submodule paths, remotes, pointers, and document links together.
- If a new name collides with an existing file, never overwrite. Keep both originals and confirm version or ownership.
- Binaries, raw data, and submitted versions stay as immutable originals. Create converted or edited copies separately and link the original.
- Without permission to read material, handle only file names and approved indexes. Never send source text to an external service for classification.

## related-documents

- [AI company bootstrap guide](AI_Bootstrap_agent.md) — flow for founding a new company
- [Migration procedure](Migration_admin.md) — changing an existing company
- [Workspace layout](../Architecture/Workspace_Layout_admin.md) — responsibilities by area
