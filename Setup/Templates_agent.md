---
type: agent-node-governance
layer: setup
status: active
version: 1.5.0
updated: 2026-09-23
---

# initial-templates

## overview

Forms needed to start a new company. Copy the code block contents into the company repository and fill in the placeholders. The templates stay in Korean to match the headings existing workspace documents use and because HQ reads the results; translating workspace documents is a separate decision. This document itself has no `task` tag and is not indexed as a task.

| Section | Content | Applies |
|---|---|---|
| [company-profile](#company-profile) | Company-specific values | Operating manual |
| [entry-file](#entry-file) | Agent reading order | Operating manual |
| [area-context](#area-context) | Per-area authority and canonical documents | Operating manual |
| [task-note](#task-note) | Basic mode TaskNote | Operating manual |
| [project-status](#project-status) | STATUS body | Operating manual |
| [decision-record](#decision-record) | Actual HQ decisions | Operating manual |
| [related-documents](#related-documents) | Setup and schema | Operating manual |

## company-profile

```markdown
# 회사 프로필

| 항목 | 값 |
|---|---|
| 회사·연구 분야 | <회사 이름·질문> |
| HQ 이름·owner 값 | <사람> / <owner slug> |
| workspace-root | <절대 경로> |
| protocol-folder·고정 commit | <경로> / <SHA> |
| 회사 채택 기록 | <로컬 Protocol_Adoption.md 경로> |
| entry-files | AGENTS.md, 필요 시 CLAUDE.md |
| task-folder·templates·task-views | <실제 경로·템플릿 제외 설정> |
| decision-log·project-index·context-file | <실제 경로> |
| trash·assets-folder | <복구·대용량 자료 경로> |
| remote·main-branch·ai-branch | <회사 Git remote> / main / ai/work |
| git-data·large-file-limit | <동기화 밖 경로> / <상한> |
| 도구와 버전·상태 명령·기록 링크 형식 | <현장에서 확인한 값> |
| 기밀·제한 경로 및 허용 처리 환경 | <없으면 없음, 미확인이면 미확인> |
| 도입 모드 | 기본 (Router 미사용) |
| runtime-dir·router·checkpoint-dir | 기본 모드: 미사용, 확장 시 지정 |

## 영역과 프로젝트 키

| 키 | projects 값 | 경로 prefix | task 저장 위치 | 정본 |
|---|---|---|---|---|
| <키> | <프로젝트 README 링크> | <경로> | <경로> | README·STATUS·Decisions·CONTEXT |

## 명명과 예외

<프로젝트 ID·결정 ID·자료 이름 규칙과 HQ 승인 예외>
```

When adopting extended mode, add a local value for every `{name}` item in the [source profile](../Architecture/Company_Profile_admin.md) and test that the Router reads that local profile.

## entry-file

```markdown
# Agent 진입점

1. <로컬 Protocol_Adoption.md>에서 활성화된 프로토콜 commit과 모드를 확인한다.
2. <로컬 Company_Profile.md>와 <프로토콜>/AI/README.md를 읽는다.
3. 요청 TaskNote, 작업 대상의 가장 가까운 _AI/CONTEXT.md, 그 정본을 읽는다.
4. 승인된 범위에서 백업·실행·검증하고 TaskNote에 기록한다.
5. 확장 사양 조항이나 저장소 업데이트를 운영 승인으로 간주하지 않는다.
```

## area-context

```markdown
# 영역 AI Context

## 목적
<이 영역이 책임지는 질문>

## 정본
- <README·STATUS·Decisions·데이터·저장소 색인의 실제 경로>

## 기본 범위
- 읽기: <허용 경로>
- 쓰기: <작업이 구체화해야 할 경로>
- 기밀: <제한 경로·외부 전달 금지>

## 검증
<결과를 확인할 명령·증거·수동 확인 조건>
```

## task-note

Below is the basic mode template for risk-level-1 work. Match `title` to the actual file name and set `owner` to the next actor. When changing to risk level 2, adjust the execution mode and approval state too. Key order and allowed values follow [TaskNote fields](../Architecture/Frontmatter_admin.md#tasknote-필드); keep the keys of optional fields even when they have no value.

```markdown
---
title: <할 일>
status: to-do
tags:
  - task
  - ai
projects: []
contexts: []
owner: ai
hq_todo: none
risk: 1
llm_model: <이 TaskNote를 쓴 모델>
proposal_version: V1.0.0
approved_version: ""
recommended_model: <작업 난이도에 맞는 모델>
execution_mode: autonomous
report_policy: final
write_scope: []
blockedBy: []
scheduled:
due:
completedDate:
timeEstimate:
dateCreated:
dateModified:
---

# 지시
목표·입력·산출물·범위·제외·완료 기준·검증 방법.

# 현재 상태
단계·다음 행동·막힘·권한 근거·백업·중단 조건.

# 결정 및 승인
실제 승인 원문·시각·버전·허용 행위만 기록. 없으면 미승인.

# 실행 계획
대상·작업·검증·복구 방법.

# 기록
결과·변경 파일·검증·미해결·다음 인계.
```

Write dependencies in `blockedBy` as a list of task links. The old `blocked_by` is a [retired key](../Architecture/Frontmatter_admin.md#tasknote-도구-관리-키와-폐기-키); replace it with `blockedBy` and keep external wait conditions in the body.

## project-status

```markdown
# 프로젝트 상태

## Current state
<현재 사실과 원 증거 링크>

## This week's outcome
<이번 주에 확인할 결과>

## Blockers and decisions needed
<담당·결정·해소 조건>

## Next milestone
<산출물·검증·목표 시점>
```

STATUS frontmatter values for status, stage, priority, and deadline are set by the local company's adopted field rules and HQ decisions. This template never fixes those values on its own.

## decision-record

```markdown
# Decisions

## DEC-<영역>-<번호> — <날짜> — <결정 제목>

- Context: 결정해야 했던 이유
- Options: 선택지와 영향
- Decision: HQ의 실제 결정·조건·원문 근거
- Consequences: 적용 범위·후속 작업·대체되는 이전 결정
- Revisit trigger: 다시 판단할 조건
```

Keep draft options in the TaskNote; promote only actual HQ decisions to Decisions.

## related-documents

- [Setup and adoption](README.md) — order for using the templates
- [Company adoption record](Adoption_admin.md#승인-기록) — version and approval form
- [Task and record schema](../AI/Task_and_Record_Schema_agent.md) — extended mode format
