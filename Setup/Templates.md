---
type: jm-protocol
layer: setup
status: draft
version: 0.2.0
updated: 2026-09-15
---

# 초기-템플릿

## overview

새 회사의 시작에 필요한 틀입니다. 코드 블록의 내용을 회사 저장소에 복사하고 자리표시자를 채웁니다. 이 문서 자체에는 `task` 태그가 없으며 작업으로 색인하지 않습니다.

| 섹션 | 내용 | 상태 | 근거 |
|---|---|---|---|
| [회사-프로필](#회사-프로필) | 회사별 값 | proposed | 검토 C1·C10 |
| [진입-파일](#진입-파일) | Agent 읽기 순서 | proposed | 검토 C9 |
| [영역-context](#영역-context) | 영역별 권한과 정본 | proposed | 검토 C9 |
| [작업-노트](#작업-노트) | 기본 모드 TaskNote | proposed | 검토 C4 |
| [프로젝트-상태](#프로젝트-상태) | STATUS 본문 | proposed | 검토 C9 |
| [결정-기록](#결정-기록) | 실제 HQ 결정 | proposed | 검토 C10 |
| [관련-문서](#관련-문서) | 설치와 스키마 | — | — |

## 회사-프로필

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

확장 모드를 도입할 때에는 [출처 프로필](../Architecture/Company_Profile.md)의 모든 `{이름}` 항목에 대응되는 로컬 값을 추가하고, Router가 그 로컬 프로필을 읽는지 시험합니다.

## 진입-파일

```markdown
# Agent 진입점

1. <로컬 Protocol_Adoption.md>에서 활성화된 프로토콜 commit과 모드를 확인한다.
2. <로컬 Company_Profile.md>와 <프로토콜>/AI/README.md를 읽는다.
3. 요청 TaskNote, 작업 대상의 가장 가까운 _AI/CONTEXT.md, 그 정본을 읽는다.
4. 승인된 범위에서 백업·실행·검증하고 TaskNote에 기록한다.
5. proposed 조항이나 저장소 업데이트를 운영 승인으로 간주하지 않는다.
```

## 영역-context

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

## 작업-노트

아래는 기본 모드의 위험도 1 작업 틀입니다. `title`은 실제 파일명과 맞추고 `owner`는 다음 행동 주체로 지정합니다. 위험도 2로 바꾸면 실행 모드와 승인 상태도 함께 조정합니다.

```markdown
---
title: <할 일>
tags: [task, ai]
status: to-do
owner: ai
hq: none
risk: 1
proposal_version: V1.0.0
approved_version: ""
execution_mode: autonomous
report_policy: final
projects: []
write_scope: []
blocked_by: []
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

의존성 필드는 기본 모드에서 현행 `blocked_by`를 유지합니다. TaskNotes용 `blockedBy` 전환은 [스키마](../AI/Task_and_Record_Schema.md#대표-task-필드-변경-제안) 승인 후 적용하며 외부 조건은 본문에 보존합니다.

## 프로젝트-상태

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

STATUS frontmatter의 상태·단계·우선순위·마감 값은 로컬 회사가 채택한 필드 규칙과 HQ 결정으로 설정합니다. 이 템플릿은 값을 임의로 확정하지 않습니다.

## 결정-기록

```markdown
# Decisions

## DEC-<영역>-<번호> — <날짜> — <결정 제목>

- Context: 결정해야 했던 이유
- Options: 선택지와 영향
- Decision: HQ의 실제 결정·조건·원문 근거
- Consequences: 적용 범위·후속 작업·대체되는 이전 결정
- Revisit trigger: 다시 판단할 조건
```

초안 선택지는 TaskNote에 두고, 실제 HQ 결정만 Decisions로 승격합니다.

## 관련-문서

- [설치와 도입](README.md) — 템플릿 사용 순서
- [회사 채택 기록](Adoption.md#승인-기록) — 버전·승인 양식
- [작업과 기록 스키마](../AI/Task_and_Record_Schema.md) — 확장 모드 형식
