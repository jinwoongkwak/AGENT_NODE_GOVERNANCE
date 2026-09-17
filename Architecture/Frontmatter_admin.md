---
type: agent-node-governance
layer: architecture
status: active
version: 1.4.0
updated: 2026-09-16
---

# frontmatter

## overview

작업 문서와 지식 문서의 frontmatter를 문서 종류별로 한 가지 형식으로 맞추는 규칙입니다. HQ가 승인했고, 같은 규칙의 기계 판독판이 [Frontmatter_agent.json](Frontmatter_agent.json)입니다. 이 문서가 사람이 읽는 정본이고, 규칙을 바꾸려면 이 문서를 먼저 고쳐 승인받습니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [적용-상태](#적용-상태) | 적용 범위와 파일 구성 | 운영 매뉴얼 |
| [공통-표기](#공통-표기) | 모든 종류에 공통인 YAML 표기 | 운영 매뉴얼 |
| [문서-종류](#문서-종류) | 종류별 위치와 식별 방법 | 운영 매뉴얼 |
| [tasknote](#tasknote) | TaskNote 필드와 허용 값 | 운영 매뉴얼 |
| [프로젝트-status](#프로젝트-status) | STATUS 필드와 허용 값 | 운영 매뉴얼 |
| [프로젝트-readme](#프로젝트-readme) | 프로젝트 README 필드 | 운영 매뉴얼 |
| [결정-기록과-색인](#결정-기록과-색인) | Decisions와 색인 문서 | 운영 매뉴얼 |
| [기술-wiki와-저장소-카드](#기술-wiki와-저장소-카드) | 기술 Wiki와 repo-card | 운영 매뉴얼 |
| [이론-wiki](#이론-wiki) | 이론 Wiki 노트 | 운영 매뉴얼 |
| [hq-결정-기록](#hq-결정-기록) | HQ가 정한 것과 반영한 곳 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 스키마·권한·검사기 | 운영 매뉴얼 |

## 적용-상태

- **적용 범위:** 새로 만드는 문서는 이 규칙을 따릅니다. 기존 문서는 그 문서를 고치는 작업에서 함께 맞추고, 전체를 한 번에 바꾸는 일은 [TaskNote](Document_System_admin.md#작업-문서)로 제안해 승인받습니다.

- **표와 JSON:** 이 문서는 사람이 읽고 고치는 정본이고, 같은 규칙을 [Frontmatter_agent.json](Frontmatter_agent.json)이 기계가 읽는 형태로 담습니다. 규칙을 바꿀 때는 이 문서를 먼저 고쳐 승인받고 JSON을 맞춥니다.

- **회사 값:** `{hq-owner}`, 폴더 경로, `contexts`, `recommended_model` 모델 목록, STATUS 값 목록은 회사 로컬 파일(이 회사는 `NODE_PROFILE/Frontmatter_Local_agent.json`)에 둡니다.

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
| 링크 | vault 기준 전체 경로, 큰따옴표. 연결할 문서가 있으면 항상 링크로 쓰고, 링크를 만들 수 없을 때만 텍스트 | `"[[20_PROJECTS/P2501_PKG_PD_CODESIGN/README\|P2501]]"` |
| 필수 값을 모를 때 | 키는 두고 값을 비움. 본문에 "확인 필요" | `next_deadline:` |
| 선택 값이 없을 때 | 키는 두고 값을 비움. 키를 지우지 않음 | `track:` |
| 키 이름 | `snake_case`. 작업 관리 도구가 정한 키는 그 이름 그대로 | `blockedBy`, `dateCreated` |
| 키 순서 | 종류별 표의 순서. 표에 없는 도구 관리 키는 맨 뒤 | — |
| 텍스트 값 | 한 줄. 문장 설명·링크·강조는 본문에 | — |
| AI 작성 표시 | AI가 초안을 쓰거나 고친 문서는 `llm_model`에 모델 이름을 적음. 사람이 쓴 문서는 키를 두고 값을 비움 | `llm_model: Claude Sonnet 5` |

## 문서-종류

| 종류 | 위치 | 식별 | 필수 필드 수 | 바꿀 권한 |
|---|---|---|---:|---|
| TaskNote (AI) | `{task-folder}` | `tags`에 `task`, `ai` | 14 | 필드별, [위험도](Risk_and_Authority_admin.md#위험도) |
| TaskNote (사람) | `{task-folder}` | `tags`에 `task`, `admin` | 3 | 필드별 |
| 프로젝트 STATUS | 프로젝트 폴더의 `STATUS.md` | 파일 이름 | 6 | `status`·`phase`·`next_deadline`은 HQ (위험도 2) |
| 프로젝트 README | 프로젝트 폴더의 `README.md` | `project_id` 있음 | 3 | Agent |
| 결정 기록 | `Decisions.md` | 파일 이름 | 3 | Agent |
| 색인 | 색인 문서 | `type` 값 | 2 | Agent |
| 저장소 카드 | 기술 Wiki | `type: repo-card` | 8 | Agent |
| 기술 Wiki | 기술 Wiki | 위치 | 2 | Agent |
| 이론 Wiki | 이론 Wiki | 위치 | 7 | Agent |
| 영역 CONTEXT | `_AI/CONTEXT.md` | 파일 이름 | frontmatter 없음 | HQ |

AGENT_NODE_GOVERNANCE 자체 문서의 frontmatter는 [문서 작성 규칙](../HQ/Protocol_Governance_admin.md#문서-작성-규칙)을 따릅니다.

## tasknote

### tasknote-필드

| 순서 | 필드 | 필수 | 형식 | 정하는 사람 |
|---:|---|---|---|---|
| 1 | `title` | AI·사람 | 텍스트, 파일 이름과 같음 | Agent |
| 2 | `status` | AI·사람 | 값 목록 | Agent |
| 3 | `tags` | AI·사람 | 목록 | Agent |
| 4 | `projects` | AI | 링크 목록. 링크를 만들 수 없을 때만 텍스트 | Agent |
| 5 | `contexts` | 선택 | 값 목록의 목록 | Agent (HQ 확인) |
| 6 | `owner` | AI | 값 목록 | Agent |
| 7 | `hq_todo` | AI | 값 목록 | Agent |
| 8 | `risk` | AI | 값 목록 | Agent |
| 9 | `llm_model` | AI | 모델 이름 | Agent |
| 10 | `proposal_version` | AI | `V1.0.0` | Agent |
| 11 | `approved_version` | AI | `V1.0.0`, 미승인은 `""` | Agent (HQ 승인 원문 근거) |
| 12 | `recommended_model` | AI | 값 목록 | Agent (HQ가 바꿀 수 있음) |
| 13 | `execution_mode` | AI | 값 목록 | HQ |
| 14 | `report_policy` | AI | 값 목록 | HQ |
| 15 | `write_scope` | AI | vault 기준 경로 목록 | HQ |
| 16 | `blockedBy` | 선택 | 막고 있는 task의 링크 목록 | Agent |
| 17 | `scheduled` | 선택 | 날짜 또는 날짜와 시각 | HQ |
| 18 | `due` | 선택 | 날짜 또는 날짜와 시각 | HQ |
| 19 | `completedDate` | 선택 | 날짜. AI TaskNote는 종료일 때만 | 작업 관리 도구 |
| 20 | `timeEstimate` | 선택 | 분 단위 정수 | HQ |
| 21 | `ForToday` | 사람 선택 | `true`/`false` | HQ |
| 22 | `waiting` | 사람 선택 | `true`/`false` | HQ |
| 23 | `dateCreated` | 선택 | 날짜와 시각 | 작업 관리 도구 |
| 24 | `dateModified` | 선택 | 날짜와 시각 | 작업 관리 도구 |

### tasknote-허용-값

| 필드 | 값 | 뜻 |
|---|---|---|
| `status` | `to-do` | 시작 전 |
| | `in-progress` | 진행 중 |
| | `delayed` | 미루었거나 다시 볼 조건을 기다림 |
| | `done` | 완료. AI TaskNote는 종료에만 씀 |
| | `archived` | 보관. 작업 관리 도구가 완료로 취급 |
| `tags` | `task` | 필수. 작업 관리 도구가 task로 인식 |
| | `ai` | AI TaskNote에 필수 |
| | `admin` | 사람 TaskNote에 필수 |
| | `archived` | 보관한 task. 그 밖의 태그는 자유 |
| `contexts` | 회사 값 (예: `GaTech`, `PSyLab`) | 일의 맥락. AI가 쓰고 HQ가 확인 |
| `owner` | `ai` · `{hq-owner}` · `none` | 다음 행동 주체. `none`은 종료 |
| `hq_todo` | `none` · `decide` · `dispatch` · `review` | HQ가 지금 할 일 |
| `risk` | `0` · `1` · `2` | [위험도](Risk_and_Authority_admin.md#위험도) |
| `llm_model` | 실제로 쓴 모델 이름 (예: `Claude Opus 5`, `Claude Sonnet 5`, `GPT-5`) | 이 문서를 쓴 모델 |
| `recommended_model` | `Claude Haiku 4.5` · `GPT-5 mini` | 난이도 낮음: 정해진 절차, 단순 수집·편집 |
| | `Claude Sonnet 5` · `GPT-5` | 난이도 보통: 일반 실행, 문서 작성, 코드 수정 |
| | `Claude Opus 5` · `GPT-5 Pro` | 난이도 높음: 설계·다단계 추론, 위험도 2 작업 |
| `execution_mode` | `autonomous` · `after-approval` · `manual` | [실행 모드](Risk_and_Authority_admin.md#실행-모드) |
| `report_policy` | `decision-only` · `milestone` · `final` | [보고 정책](../HQ/Control_Settings_admin.md#보고-정책) |

AI TaskNote의 `status`·`owner`·`hq_todo`는 [작업 상태](Command_and_Report_Flow_admin.md#작업-상태)의 여섯 조합만 씁니다. HQ 검토가 남은 작업은 `in-progress`라서 작업 관리 도구에서 완료로 보이지 않고, `completedDate`는 종료(`done / none / none`)할 때만 적습니다. `recommended_model`은 제안서에서 실행할 작업의 난이도에 맞는 모델을 AI가 추천하는 값이고, 실제로 그 문서를 쓴 모델은 `llm_model`에 남깁니다.

### tasknote-도구-관리-키와-폐기-키

| 구분 | 키 | 처리 |
|---|---|---|
| 도구 관리 | `timeEntries`, `recurrence`, `recurrence_anchor`, `recurrence_parent`, `complete_instances`, `skipped_instances`, `reminders`, `pomodoros`, `tasknotes_manual_order` | 사람·Agent가 직접 쓰지 않음 |
| 폐기 | `blocked_by` | `blockedBy`로 바꿈 |
| 폐기 | `project` | `projects`로 바꿈 |
| 폐기 | `hq` | `hq_todo`로 바꿈 |
| 폐기 | `priority`, `urgency` | 필드를 지움 |
| legacy 값 | `status: completed` | `done`으로 읽음 |
| legacy 값 | `status: shelved` | `delayed`로 바꿈 |

## 프로젝트-status

| 순서 | 필드 | 필수 | 형식·허용 값 | 정하는 사람 |
|---:|---|---|---|---|
| 1 | `project_id` | 예 | 프로젝트 ID (예: `P2501_PKG_PD_CODESIGN`) | Agent |
| 2 | `status` | 예 | `idea` · `active` · `paused` · `closing` · `archived` | HQ |
| 3 | `phase` | 예 | `research` · `design` · `verification` · `publication` | HQ |
| 4 | `next_action` | 예 | 구체적 행동 하나 | Agent |
| 5 | `next_deadline` | 예 (빈 값 허용) | 날짜 | HQ |
| 6 | `updated` | 예 | 날짜 | Agent |
| 7 | `draft_by` | 선택 | AI 초안을 만든 TaskNote 링크 또는 legacy ID | Agent |
| 8 | `llm_model` | AI 작성 시 | 초안을 만든 모델 이름 | Agent |

`status`·`phase` 값 목록은 회사 로컬 값에서 바꿀 수 있습니다. `draft_by`가 있으면 `llm_model`에 그 초안을 만든 모델 이름을 함께 남깁니다.

## 프로젝트-readme

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `project_id` | 예 | 프로젝트 ID |
| 2 | `type` | 예 | `project-brief` (일반) · `collaboration` (공동 연구) |
| 3 | `collaborators` | 선택 | 목록. 사람·기관 문서가 있으면 링크 |
| 4 | `track` | 선택 | 회사 값 (예: `education`) |
| 5 | `created` | 예 | 날짜 |
| 6 | `draft_by` | 선택 | TaskNote 링크 또는 legacy ID |
| 7 | `llm_model` | AI 작성 시 | 초안을 만든 모델 이름 |

## 결정-기록과-색인

| 종류 | 순서대로 필드 | 허용 값 |
|---|---|---|
| 결정 기록 | `project_id`, `type`, `updated` (모두 필수), `llm_model` (AI 작성 시) | `project_id`: 프로젝트 ID 또는 `HQ` · `type`: `decision-log` |
| 색인 | `type`, `updated` (모두 필수), `llm_model` (AI 작성 시) | `type`: `project-index` · `technical-index` · `theory-index` · `repository-catalog` |

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
| 9 | `llm_model` | AI 작성 시 | 카드를 만든 모델 이름 |

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
| 9 | `llm_model` | AI 작성 시 | 노트를 쓴 모델 이름 |

frontmatter가 없는 기술 Wiki 노트에는 이 표의 필드를 모두 넣습니다. 값을 모르면 키만 두고 비웁니다.

## 이론-wiki

| 순서 | 필드 | 필수 | 형식·허용 값 |
|---:|---|---|---|
| 1 | `author` | 예 | 텍스트 |
| 2 | `affiliation` | 예 | 텍스트 |
| 3 | `tags` | 예 | 목록 |
| 4 | `created` | 예 | 날짜 |
| 5 | `updated` | 예 | 날짜 |
| 6 | `language` | 예 | `KR` · `EN` |
| 7 | `sources` | 예 | 목록 |
| 8 | `llm_model` | AI 작성 시 | 노트를 쓴 모델 이름 |

## hq-결정-기록

| # | 대상 | 결정 | 반영한 곳 |
|---|---|---|---|
| Q1 | TaskNote `status` | legacy 값 `shelved`는 `delayed`로 바꾸고 `delayed`를 허용 값에 추가 | [tasknote-허용-값](#tasknote-허용-값) |
| Q2 | 사람 TaskNote | `urgency`만 삭제. `ForToday`·`waiting`은 `true`/`false`로 유지하고 `blockedBy`는 별도 링크 필드로 둠 | [tasknote-필드](#tasknote-필드) |
| Q3 | 참조 값 | 연결할 문서가 있으면 링크로 쓰고, 링크를 만들 수 없을 때만 텍스트 | [공통-표기](#공통-표기) |
| Q4 | `priority` | 모든 문서 종류에서 삭제 | [tasknote-필드](#tasknote-필드), [프로젝트-status](#프로젝트-status) |
| Q5 | 공동 연구 README `type` | `collaboration` | [프로젝트-readme](#프로젝트-readme) |
| Q6 | 기술 Wiki | frontmatter가 없는 노트에 최신 필드 구성을 모두 넣고, `status`에는 설명 문장을 쓰지 않음 | [기술-wiki-노트](#기술-wiki-노트) |
| Q7 | 전체 | 값이 없는 선택 필드도 키는 보여 주고 값만 비움 | [공통-표기](#공통-표기) |

## 관련-문서

- [Frontmatter_agent.json](Frontmatter_agent.json) — 같은 규칙의 기계 판독판
- [check_frontmatter.py](../tools/check_frontmatter.py) — 보고 전용 검사기
- [작업과 기록 스키마](../AI/Task_and_Record_Schema_agent.md#대표-task-필드) — 확장 모드의 대표 task 필드
- [문서 체계](Document_System_admin.md) — 문서마다의 역할
- [위험도와 권한](Risk_and_Authority_admin.md) — 필드를 바꿀 권한
