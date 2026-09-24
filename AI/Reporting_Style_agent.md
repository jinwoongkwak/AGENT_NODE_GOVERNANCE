---
type: agent-node-governance
layer: ai
status: active
version: 1.6.1
updated: 2026-09-23
---

# record-format

## overview

The format AI uses for a [TaskNote](../Architecture/Document_System_admin.md#작업-문서)'s `# 기록`, `# 결정 및 승인`, and `# 근거` sections and for the final chat report. A reader must grasp the status at a glance and open any needed decision or review item directly. Do not create separate report files.

| Section | Content | Applies |
|---|---|---|
| [record-structure](#record-structure) | Record entry template and report language | Operating manual |
| [tables-and-checklists](#tables-and-checklists) | Format by content type | Operating manual |
| [line-breaks](#line-breaks) | Layout that scans quickly | Operating manual |
| [links](#links) | File link rules | Operating manual |
| [fact-estimate-recommendation](#fact-estimate-recommendation) | Separating verified facts from estimates | Operating manual |
| [unresolved-and-handoff](#unresolved-and-handoff) | Recording remaining work and the review block | Operating manual |
| [related-documents](#related-documents) | Follow-up proposals and schema | Operating manual |

## record-structure

```markdown
### YYYY-MM-DD · AI · <계획|실행|검증|검토 요청|완료> · Vx.y.z

- **지시 버전:** Vx.y.z

- **승인된 버전:** Vx.y.z 또는 해당 없음

- **결과:**

- **입력·근거:**

- **변경 파일:**

- **검증:**

- **미해결:** 없음

- **다음 인계:** 없음

- **다음 버전 제안:** 없음
```

- **Write to HQ in Korean.** Records, reports, decision tables, and chat messages for HQ are in Korean; technical terms may stay in English. Governance documents and agent-to-agent records are in English.

- **Lead with the result.**

- **Analysis that changed no files** still records the inputs used and how it was verified.

- **Keep paragraphs to three sentences or fewer**; use a table for three or more parallel items.

- **Versions** follow the [version rules](../HQ/Commands_and_Approval_admin.md#버전-규칙).

## tables-and-checklists

| Content | Format | Required elements |
|---|---|---|
| Three or more items sharing attributes | Table | Item, action or judgment, status or result, basis |
| Items HQ must decide | [Decision table](../HQ/Commands_and_Approval_admin.md#결정표-작성) | Number, question, options, AI recommendation, decision |
| Items HQ must review | Checklist | File link, reason for review |
| Follow-up actions | Checklist | Owner, one-line completion condition |
| Progress comparison | Table | One of `완료`, `진행 중`, `대기`, `보류`, `확인 필요` |
| Execution plan | Numbered table | Step, target, action, owner, approval needed |
| Changed files | List by type | Created, modified, moved, trashed, with links |
| Unresolved items and handoffs | Checklist | Cause, owner, next action, blocking or not |

- Never bury decisions or user actions in a paragraph.

- Keep table cells short; put long explanations below the table.

- Decisions and actions for HQ in one TaskNote total 10 or fewer ([attention budget](../HQ/HQ_Role_admin.md#주의력-예산)).

## line-breaks

- Put a blank line between headings, tables, checklists, and paragraphs.

- Do not combine different results in one bullet.

- Put blank lines before and after checklists, and before any explanation that follows a table.

## links

Write links in task records in a format that opens directly in the workspace. This company's format is in [`{record-link-format}`](../Architecture/Company_Profile_admin.md#도구-설정). Links within AGENT_NODE_GOVERNANCE documents themselves follow [links and connections](../HQ/Protocol_Governance_admin.md#링크와-연결).

| Rule | Content |
|---|---|
| Full path | Link files with the full path from the workspace root and a short display name |
| In tables | Escape the display-name separator |
| Folders | Do not link folders; link the folder's README, STATUS, or index file. If none, write the path as code |
| Moved files | Link the current location of moved or trashed files |
| Outside the workspace | File URL links; web addresses as normal Markdown links |
| Confidential | Do not link confidential manuscripts or personal records; link only approved indexes ([confidentiality](Common_Rules_agent.md#confidentiality)) |
| Examples | Wrap examples and placeholders in code so link checks skip them |
| Check | When finishing a record, confirm new links open and note it under verification |

## fact-estimate-recommendation

- **Verified facts** are written with their source file or check method.

- **Estimates** are marked `추정` or `확인 필요`.

- **Recommendations** are marked `AI 권장` and kept separate from the available alternatives.

- **Counts and sizes** state the measurement method, such as `스크립트 집계` or `파일명 기준`.

## unresolved-and-handoff

When HQ confirmation remains, the record stage is `검토 요청` and the first line of the chat report is `검토 대기 — HQ 할 일 N개`. If any `미해결` or `다음 인계` item exists, write the next-version proposal under the [follow-up proposal](../HQ/Review_and_Closure_admin.md#후속-제안-처리) rules. Write the review request as follows.

```markdown
## 검토 요청

- [ ] <파일 링크> — 다음 행동이 실제 우선순위와 맞는지 확인

| # | 질문 | 선택지 | AI 권장 | 결정 |
|---|---|---|---|---|
| Q1 | 구현 방식 | A / B / C | C | |
```

### exchange-record-index-extended

When [process roles](../Architecture/Organization_admin.md#과정-역할) are adopted, the [Router](Routing_agent.md#router-role) adds one line per record to `## 교환 기록 색인` at the end of the primary note's `# 기록`. The format is `- R01 · 003 · evaluation · revise · <record link>`. The Coordinator writes an entry in the record structure above only on a verdict change, an HQ handoff, or completion.

## related-documents

- [Review and closure](../HQ/Review_and_Closure_admin.md) — how HQ reads these records
- [Task and record schema](Task_and_Record_Schema_agent.md) — fields and sections of record documents
- [Common rules](Common_Rules_agent.md) — inputs and checks to record
- [AI guide](README.md) — list of AI documents
