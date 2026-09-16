---
type: agent-node-governance
layer: architecture
status: draft
version: 1.2.0
updated: 2026-09-16
---

# frontmatter

## overview

**초안입니다.** 작업 문서와 지식 문서의 frontmatter를 문서 종류별로 한 가지 형식으로 맞추기 위한 규칙입니다. HQ가 이 문서를 고쳐 승인하면, 같은 내용을 기계 판독판 [Frontmatter_agent.json](Frontmatter_agent.json)에 맞춰 넣고 그때부터 적용합니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [초안-상태](#초안-상태) | 승인 전 사용 범위와 파일 구성 | 초안 |
| [공통-표기](#공통-표기) | 모든 종류에 공통인 YAML 표기 | 초안 |
| [문서-종류](#문서-종류) | 종류별 위치와 식별 방법 | 초안 |
| [tasknote](#tasknote) | TaskNote 필드와 허용 값 | 초안 |
| [프로젝트-status](#프로젝트-status) | STATUS 필드와 허용 값 | 초안 |
| [프로젝트-readme](#프로젝트-readme) | 프로젝트 README 필드 | 초안 |
| [결정-기록과-색인](#결정-기록과-색인) | Decisions와 색인 문서 | 초안 |
| [기술-wiki와-저장소-카드](#기술-wiki와-저장소-카드) | 기술 Wiki와 repo-card | 초안 |
| [이론-wiki](#이론-wiki) | 이론 Wiki 노트 | 초안 |
| [hq-결정-필요](#hq-결정-필요) | 확정 전에 HQ가 정할 것 | 초안 |
| [관련-문서](#관련-문서) | 스키마·권한·검사기 | 초안 |

## 초안-상태

- **승인 전:** Agent는 이 규칙으로 기존 문서를 고치지 않습니다. 새 문서를 만들 때만 참고합니다.

- **표와 JSON:** 이 문서는 사람이 읽고 고치는 판입니다. 같은 규칙을 [Frontmatter_agent.json](Frontmatter_agent.json)이 기계가 읽는 형태로 담습니다. 승인 전에는 두 파일이 어긋날 수 있고, 승인 뒤에는 이 문서를 기준으로 JSON을 맞춥니다.

- **회사 값:** `{hq-owner}`, 폴더 경로, `contexts`, STATUS 값 목록은 회사 로컬 파일(이 회사는 `NODE_PROFILE/Frontmatter_Local_agent.json`)에 둡니다.

- **검사:** [check_frontmatter.py](../tools/check_frontmatter.py)가 위반을 보고만 하고 파일은 고치지 않습니다.

```text
python AGENT_NODE_GOVERNANCE/tools/check_frontmatter.py --root . --local NODE_PROFILE/Frontmatter_Local_agent.json --list
```

## 공통-표기

| 항목 | 규칙 | 예 |
|---|---|---|
| 목록 | 블록 목록. 빈 목록만 `[]` | `tags:` 다음 줄 `  - task` |
| 날짜 | `YYYY-MM-DD` | `2026-09-16` |
| 날짜와 시각 | 작업 관리 도구가 쓰는 ISO 8601 | `2026-09-16T10:30:00.000-04:00` |
| 링크 | vault 기준 전체 경로, 큰따옴표 | `"[[20_PROJECTS/P2501_PKG_PD_CODESIGN/README\|P2501]]"` |
| 필수 값을 모를 때 | 키는 두고 값을 비움. 본문에 "확인 필요" | `next_deadline:` |
| 선택 값이 없을 때 | 키를 생략 | — |
| 키 이름 | `snake_case`. 작업 관리 도구가 정한 키는 그 이름 그대로 | `blockedBy`, `dateCreated` |
| 키 순서 | 종류별 표의 순서. 표에 없는 도구 관리 키는 맨 뒤 | — |
| 텍스트 값 | 한 줄. 문장 설명·링크·강조는 본문에 | — |

## 문서-종류

| 종류 | 위치 | 식별 | 필수 필드 수 | 바꿀 권한 |
|---|---|---|---:|---|
| TaskNote (AI) | `{task-folder}` | `tags`에 `task`, `ai` | 13 | 필드별, [위험도](Risk_and_Authority_admin.md#위험도) |
| TaskNote (사람) | `{task-folder}` | `tags`에 `task`만 | 4 | 필드별 |
| 프로젝트 STATUS | 프로젝트 폴더의 `STATUS.md` | 파일 이름 | 7 | `status`·`phase`·`priority`·`next_deadline`은 HQ (위험도 2) |
| 프로젝트 README | 프로젝트 폴더의 `README.md` | `project_id` 있음 | 3 | Agent |
| 결정 기록 | `Decisions.md` | 파일 이름 | 3 | Agent |
| 색인 | 색인 문서 | `type` 값 | 2 | Agent |
| 저장소 카드 | 기술 Wiki | `type: repo-card` | 8 | Agent |
| 기술 Wiki | 기술 Wiki | 위치 | 2 | Agent |
| 이론 Wiki | 이론 Wiki | 위치 | 6 | Agent |
| 영역 CONTEXT | `_AI/CONTEXT.md` | 파일 이름 | frontmatter 없음 | HQ |

AGENT_NODE_GOVERNANCE 자체 문서의 frontmatter는 [문서 작성 규칙](../HQ/Protocol_Governance_admin.md#문서-작성-규칙)을 따릅니다.

## tasknote

### tasknote-필드

| 순서 | 필드 | 필수 | 형식 | 정하는 사람 |
|---:|---|---|---|---|
| 1 | `title` | AI·사람 | 텍스트, 파일 이름과 같음 | Agent |
| 2 | `status` | AI·사람 | 값 목록 | Agent |
| 3 | `priority` | AI·사람 | 값 목록 | HQ |
| 4 | `tags` | AI·사람 | 목록 | Agent |
| 5 | `projects` | AI | 링크 목록 | Agent |
| 6 | `contexts` | 선택 | 값 목록의 목록 | HQ |
| 7 | `owner` | AI | 값 목록 | Agent |
| 8 | `hq` | AI | 값 목록 | Agent |
| 9 | `risk` | AI | 값 목록 | Agent |
| 10 | `proposal_version` | AI | `V1.0.0` | Agent |
| 11 | `approved_version` | AI | `V1.0.0`, 미승인은 `""` | Agent (HQ 승인 원문 근거) |
| 12 | `execution_mode` | AI | 값 목록 | HQ |
| 13 | `report_policy` | AI | 값 목록 | HQ |
| 14 | `write_scope` | AI | vault 기준 경로 목록 | HQ |
| 15 | `blockedBy` | 선택 | task 링크 목록 | Agent |
| 16 | `scheduled` | 선택 | 날짜 또는 날짜와 시각 | HQ |
| 17 | `due` | 선택 | 날짜 또는 날짜와 시각 | HQ |
| 18 | `completedDate` | 선택 | 날짜 | 작업 관리 도구 |
| 19 | `timeEstimate` | 선택 | 분 단위 정수 | HQ |
| 20 | `urgency` | 사람 선택 | 정수 | HQ |
| 21 | `ForToday` | 사람 선택 | `true`/`false` | HQ |
| 22 | `waiting` | 사람 선택 | `true`/`false` | HQ |
| 23 | `dateCreated` | 선택 | 날짜와 시각 | 작업 관리 도구 |
| 24 | `dateModified` | 선택 | 날짜와 시각 | 작업 관리 도구 |

### tasknote-허용-값

| 필드 | 값 | 뜻 |
|---|---|---|
| `status` | `to-do` | 시작 전 |
| | `in-progress` | 진행 중 |
| | `done` | 완료 |
| | `archived` | 보관. 작업 관리 도구가 완료로 취급 |
| `priority` | `none` · `low` · `normal` · `high` | 가중치 0 · 1 · 2 (기본값) · 3 |
| `tags` | `task` | 필수. 작업 관리 도구가 task로 인식 |
| | `ai` | AI TaskNote에 필수 |
| | `archived` | 보관한 task. 그 밖의 태그는 자유 |
| `contexts` | 회사 값 (예: `GaTech`, `PSyLab`) | 일의 맥락 |
| `owner` | `ai` · `{hq-owner}` · `none` | 다음 행동 주체. `none`은 종료 |
| `hq` | `none` · `decide` · `dispatch` · `review` | HQ가 지금 할 일 |
| `risk` | `0` · `1` · `2` | [위험도](Risk_and_Authority_admin.md#위험도) |
| `execution_mode` | `autonomous` · `after-approval` · `manual` | [실행 모드](Risk_and_Authority_admin.md#실행-모드) |
| `report_policy` | `decision-only` · `milestone` · `final` | [보고 정책](../HQ/Control_Settings_admin.md#보고-정책) |

AI TaskNote의 `status`·`owner`·`hq`는 [작업 상태](Command_and_Report_Flow_admin.md#작업-상태)의 여섯 조합만 씁니다.

### tasknote-도구-관리-키와-폐기-키

| 구분 | 키 | 처리 |
|---|---|---|
| 도구 관리 | `timeEntries`, `recurrence`, `recurrence_anchor`, `recurrence_parent`, `complete_instances`, `skipped_instances`, `reminders`, `pomodoros`, `tasknotes_manual_order` | 사람·Agent가 직접 쓰지 않음 |
| 폐기 | `blocked_by` | `blockedBy`로 바꿈 |
| 폐기 | `project` | `projects`로 바꿈 |
| legacy 값 | `status: completed` | `done`으로 읽음 |
| legacy 값 | `status: shelved` | [Q1](#hq-결정-필요) |

## 프로젝트-status

| 순서 | 필드 | 필수 | 형식·허용 값 | 정하는 사람 |
|---:|---|---|---|---|
| 1 | `project_id` | 예 | 프로젝트 ID (예: `P2501_PKG_PD_CODESIGN`) | Agent |
| 2 | `status` | 예 | `idea` · `active` · `paused` · `closing` · `archived` | HQ |
| 3 | `phase` | 예 | `research` · `design` · `verification` · `publication` | HQ |
| 4 | `priority` | 예 | 정수 1–5, 1이 가장 높음 | HQ |
| 5 | `next_action` | 예 | 구체적 행동 하나 | Agent |
| 6 | `next_deadline` | 예 (빈 값 허용) | 날짜 | HQ |
| 7 | `updated` | 예 | 날짜 | Agent |
| 8 | `draft_by` | 선택 | AI 초안을 만든 TaskNote 제목 또는 legacy ID | Agent |

`status`·`phase` 값 목록과 `priority` 범위는 회사 로컬 값에서 바꿀 수 있습니다.

## 프로젝트-readme

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `project_id` | 예 | 프로젝트 ID |
| 2 | `type` | 예 | `project-brief` (일반) · `collaboration` (공동 연구) |
| 3 | `codename` | 선택 | 소문자 한 단어 |
| 4 | `partners` | 선택 | 목록 |
| 5 | `track` | 선택 | 회사 값 (예: `education`) |
| 6 | `created` | 예 | 날짜 |
| 7 | `draft_by` | 선택 | TaskNote 제목 또는 legacy ID |

## 결정-기록과-색인

| 종류 | 순서대로 필드 | 허용 값 |
|---|---|---|
| 결정 기록 | `project_id`, `type`, `updated` (모두 필수) | `project_id`: 프로젝트 ID 또는 `HQ` · `type`: `decision-log` |
| 색인 | `type`, `updated` (모두 필수) | `type`: `project-index` · `technical-index` · `theory-index` · `repository-catalog` |

## 기술-wiki와-저장소-카드

### 저장소-카드

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `type` | 예 | `repo-card` |
| 2 | `repo` | 예 | 저장소 이름 |
| 3 | `remote` | 예 | git remote 주소 |
| 4 | `local_path` | 예 | vault 기준 clone 경로 |
| 5 | `branch` | 예 | 확인한 branch |
| 6 | `last_checked_commit` | 예 | commit 해시 7–40자 |
| 7 | `status` | 예 | `active` · `archived` |
| 8 | `updated` | 예 | 날짜 |

### 기술-wiki-노트

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `title` | 선택 | 텍스트 |
| 2 | `type` | 선택 | `note` · `external-media` |
| 3 | `tags` | 예 | 목록 |
| 4 | `source_project` | 선택 | 처음 나온 프로젝트 ID |
| 5 | `status` | 선택 | `active` · `done`. 진행 설명 문장은 본문에 |
| 6 | `created` | 선택 | 날짜 |
| 7 | `updated` | 예 | 날짜 |
| 8 | `related` | 선택 | 링크 목록 |

## 이론-wiki

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `author` | 예 | 텍스트 |
| 2 | `affiliation` | 예 | 텍스트 |
| 3 | `tags` | 예 | 목록 |
| 4 | `aliases` | 선택 | 목록 |
| 5 | `created` | 예 | 날짜 |
| 6 | `updated` | 선택 | 날짜 |
| 7 | `language` | 예 | `KR` · `EN` |
| 8 | `translation` | 선택 | 다른 언어판 링크 |
| 9 | `sources` | 예 | 목록 |
| 10 | `related` | 선택 | 링크 목록 |

## hq-결정-필요

| # | 대상 | 결정할 것 | 현재 초안 |
|---|---|---|---|
| Q1 | TaskNote `status` | legacy 값 `shelved`를 `archived`로 볼지, `to-do`에 태그를 붙일지 | legacy 값으로 보고만 함 |
| Q2 | 사람 TaskNote | `urgency`·`ForToday`·`waiting`을 유지할지, `priority`·`scheduled`·`blockedBy`로 합칠지 | 사람 task 선택 필드로 유지 (tasks.base가 사용) |
| Q3 | 사람 TaskNote `projects` | 링크 대신 쓰인 일반 문자열(`Infrastructure` 등)을 허용할지 | 링크만 허용 |
| Q4 | STATUS `priority` | `0`을 허용할지 | 1–5 |
| Q5 | 공동 연구 README `type` | `collaboration`과 `project-brief` 중 무엇을 쓸지 | 둘 다 허용 |
| Q6 | 기술 Wiki | frontmatter가 없는 노트에 최소 필드를 요구할지, `status`의 설명 문장을 본문으로 옮길지 | `tags`·`updated` 필수, 문장 금지 |
| Q7 | 전체 | 값이 없는 선택 필드를 키 생략으로 할지 빈 값으로 둘지 | 키 생략 |

## 관련-문서

- [Frontmatter_agent.json](Frontmatter_agent.json) — 같은 규칙의 기계 판독판
- [check_frontmatter.py](../tools/check_frontmatter.py) — 보고 전용 검사기
- [작업과 기록 스키마](../AI/Task_and_Record_Schema_agent.md#대표-task-필드) — 확장 모드의 대표 task 필드
- [문서 체계](Document_System_admin.md) — 문서마다의 역할
- [위험도와 권한](Risk_and_Authority_admin.md) — 필드를 바꿀 권한
