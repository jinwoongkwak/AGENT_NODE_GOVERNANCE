---
type: jm-protocol
layer: architecture
status: draft
version: 0.2.0
updated: 2026-09-15
---

# 회사-프로필

## overview

JM_Protocol의 출처 회사(JouleMatter)의 값과 기존 규칙 출처를 모은 예시입니다. 다른 기업은 [로컬 프로필](../Setup/Templates.md#회사-프로필)과 [채택 기록](../Setup/Adoption.md)을 따로 작성합니다. 일반 문서의 `{이름}` 링크는 항목 설명을 가리키며, 실제 실행 값은 회사가 승인한 로컬 프로필에서 가져옵니다.

| 섹션 | 내용 | 상태 | 근거 |
|---|---|---|---|
| [회사-정보](#회사-정보) | 회사 이름, 연구 분야, 조직 형태 | adopted | DEC-HQ-001 |
| [사람과-역할-배정](#사람과-역할-배정) | HQ 담당자와 owner 값, AI 실행 환경 | adopted, proposed | DEC-HQ-001, 제안서 01 |
| [작업-공간-경로](#작업-공간-경로) | 진입 파일, 프로토콜, TaskNote, 결정 기록 경로 | adopted, proposed | DEC-HQ-005, 제안서 03·05 |
| [영역과-정본](#영역과-정본) | 영역별 목적과 정본 파일 | adopted | 기존 AI_Protocol §3 |
| [프로젝트-키](#프로젝트-키) | 프로젝트 키, `projects` 값, 저장 폴더 | adopted, proposed | DEC-HQ-003, 제안서 03 |
| [기밀-영역](#기밀-영역) | 열람과 전송을 제한하는 경로 | adopted | 기존 AI_Protocol §8 |
| [도구-설정](#도구-설정) | 작업 공간 계층별 도구와 설정 | adopted | DEC-HQ-002, DEC-HQ-005 |
| [버전-관리-설정](#버전-관리-설정) | 원격 저장소, 브랜치, 중첩 저장소 설정 | adopted | DEC-HQ-002 |
| [명명-규칙](#명명-규칙) | ID와 파일 이름 형식 | adopted | Conventions Naming |
| [근거-자료](#근거-자료) | JM_Protocol이 통합한 원문 경로 | adopted | 2026-09-15 확인 |
| [알려진-문제](#알려진-문제) | 확인된 운영 문제와 처리 위치 | adopted | 2026-09-15 확인 |
| [관련-문서](#관련-문서) | 이 값을 쓰는 문서 | — | — |

## 회사-정보

| 이름 | 값 |
|---|---|
| `{company}` | JouleMatter |
| 조직 형태 | 연구자 한 명이 HQ를 맡고 AI Agent가 실무를 맡는 [1인 기업 모델](Operating_Model.md#왜-1인-기업-모델인가) |
| 연구 분야 | 전력 전달·전력 변환 회로와 패키지의 공동 설계, 디지털 제어, 하이브리드 컨버터와 LDO |
| 작업 공간 | Obsidian Vault 하나 ([작업 공간 경로](#작업-공간-경로)) |
| 프로토콜 버전 | 0.2.0 초안, 운영 채택 대기 |

## 사람과-역할-배정

| 이름 | 값 | 쓰이는 곳 |
|---|---|---|
| `{hq-person}` | Jin | [HQ](Operating_Model.md#hq와-ai의-뜻) |
| `{hq-owner}` | `jin` | [작업 상태](Command_and_Report_Flow.md#작업-상태)의 `owner` 값 |
| AI 실행 환경 | 셸을 쓸 수 있는 코딩 Agent (Claude Code, Codex) | [공통 규칙](../AI/Common_Rules.md#지시의-출처) |
| 과정 역할 배정 (proposed) | 한 Agent 세션이 [Coordinator](../AI/Roles/Coordinator.md#역할-요약)를 맡고, 나머지 역할은 새 문맥 호출로 실행 | 제안서 01·06 |

## 작업-공간-경로

| 이름 | 값 | 상태 |
|---|---|---|
| `{workspace-root}` | Vault 루트 `JouleMatter/` (Dropbox 동기화 폴더 안) | adopted |
| `{entry-files}` | `CLAUDE.md`, `AGENTS.md` (Vault 루트) | adopted |
| `{protocol-folder}` | `00_HQ/90_SYSTEM/JM_Protocol/` | proposed (체크리스트 C9) |
| `{legacy-control-folder}` | `00_HQ/90_SYSTEM/AI_Control/` — 정본 교체 전까지 현행 규약의 원본 | adopted |
| `{task-folder}` | `00_HQ/10_PLANNING/TaskNotes/Tasks/AI/` | adopted |
| `{task-views}` | `00_HQ/10_PLANNING/TaskNotes/Views/` | adopted |
| `{templates}` | `00_HQ/90_SYSTEM/AI_Control/Templates/` | adopted |
| `{decision-log}` | `00_HQ/Decisions.md` (회사 전체), `20_PROJECTS/<ID>/10_NOTES/Decisions.md` (프로젝트) | adopted |
| `{project-index}` | `00_HQ/Project_Index.md` | adopted |
| `{context-file}` | 각 영역의 `_AI/CONTEXT.md` | adopted |
| `{trash}` | Vault 루트의 `.trash/` | adopted |
| `{assets-folder}` | Vault 밖 `JouleMatter_Assets/` (동영상, Vault 경로를 그대로 따름) | adopted |
| `{runtime-dir}` | `%LOCALAPPDATA%\JouleMatter\ai_runtime\` — 스테이징과 잠금 | proposed (제안서 03) |
| `{router}` | `00_HQ/90_SYSTEM/AI_Control/Tools/router.py` | proposed (제안서 03) |
| `{checkpoint-dir}` | `00_HQ/90_SYSTEM/AI_Control/Runtime/` | proposed (제안서 05 Q2) |

## 영역과-정본

각 영역의 AI 작업 안내는 [`{context-file}`](#작업-공간-경로)에 있습니다. 정본의 뜻은 [정본 문서](Document_System.md#정본-문서)를 봅니다.

| 영역 | 목적 | 정본 파일 | 기밀 |
|---|---|---|---|
| `00_HQ` | 프로젝트 전체 조정 | `Project_Index.md`, `Decisions.md`, AI TaskNote | 기밀 영역 목록 보유 |
| `10_INBOX` | 미분류 항목 분류 | `Files/` | 표시만 하고 전송하지 않음 |
| `20_PROJECTS` | 프로젝트 비교, 템플릿 관리 | `Project_Index.md`, 각 프로젝트 `README.md`·`STATUS.md` | `PEER_REVIEWS/` 제외 |
| `20_PROJECTS/<ID>` | 프로젝트 작업 | `README.md`, `STATUS.md`, `10_NOTES/Decisions.md`, `30_SOURCE/Repositories.md`, `30_SOURCE/Data_Index.md` | 프로젝트 CONTEXT |
| `20_PROJECTS/COLLABORATIONS/<ID>` | 다른 기관이 주도하는 협업 프로젝트 | 프로젝트와 같음 | 프로젝트 CONTEXT |
| `20_PROJECTS/PEER_REVIEWS` | 심사 마감과 상태만 | `Review_Index.md` | **예** |
| `20_PROJECTS/_PROJECT_TEMPLATE` | 템플릿. 여기서 작업하지 않음 | — | — |
| `30_TECHNICAL_WIKI` | 재사용 절차와 저장소 | `Technical_Index.md`, `Repositories/Repository_Catalog.md` | PDK·foundry·라이선스 문서 |
| `40_THEORY_WIKI` | 개념과 유도 | `Theory_Index.md` | — |
| `50_PSYLAB` | 연구실 안내·행정, 개인 연구실 기록, 동료 지원 | `PSyLab_Index.md`, `10_GUIDES/GUIDES_Metaguide.md` | `20_JIN/` |
| `90_ARCHIVE` | 끝난 작업, 읽기 전용 | 보관된 `README.md`, `STATUS.md`, `60_CLOSEOUT/Deliverables.md`, `PSYLAB/` | 읽기 전용 |

## 프로젝트-키

| 키 | `projects` 값 | 판정 경로 prefix | 저장 폴더 (proposed, 제안서 03) |
|---|---|---|---|
| `HQ` | `[[00_HQ/Project_Index]]` | `00_HQ/` | `HQ` |
| `P2501` | `[[20_PROJECTS/P2501_PKG_PD_CODESIGN/README\|P2501]]` | `20_PROJECTS/P2501_PKG_PD_CODESIGN/` | `P2501` |
| `P2502` | `[[20_PROJECTS/P2502_DIGITAL_BUCK_CTRL/README\|P2502]]` | `20_PROJECTS/P2502_DIGITAL_BUCK_CTRL/` | `P2502` |
| `P2602` | `[[20_PROJECTS/COLLABORATIONS/P2602_NGMM/README\|P2602]]` | `20_PROJECTS/COLLABORATIONS/P2602_NGMM/` | `P2602` |
| `P2604` | `[[20_PROJECTS/P2604_HYBRID_DEEPDIVE/README\|P2604]]` | `20_PROJECTS/P2604_HYBRID_DEEPDIVE/` | `P2604` |
| `P2605` | `[[20_PROJECTS/P2605_HYBRID_LDO/README\|P2605]]` | `20_PROJECTS/P2605_HYBRID_LDO/` | `P2605` |
| `TECH` | `[[30_TECHNICAL_WIKI/Technical_Index]]` | `30_TECHNICAL_WIKI/` | `TECH` |
| `THEORY` | `[[40_THEORY_WIKI/Theory_Index]]` | `40_THEORY_WIKI/` | `THEORY` |
| `PSYLAB` | `[[50_PSYLAB/PSyLab_Index]]` | `50_PSYLAB/` | `PSYLAB` |
| `UNSORTED` | `[[00_HQ/Project_Index]]` | 없음 | `UNSORTED` |

- **별칭:** 기존 task의 `[[30_TECHNICAL_WIKI/Repositories/Repository_Catalog]]`는 `TECH` 값으로 인정합니다.

- **AI 작업이 아닌 TaskNote:** `PowerCard`, `Infrastructure`, `study`, `misc` 네 값을 씁니다 (DEC-HQ-003).

- **번호:** 다음 새 프로젝트 번호는 P2606이며, 번호는 재사용하지 않습니다.

위 표를 쓰는 규칙은 [프로젝트 판정](../AI/Routing.md#프로젝트-판정)에 있습니다.

## 기밀-영역

기밀 규칙은 [공통 규칙의 기밀](../AI/Common_Rules.md#기밀)에 있고, 여기에는 경로만 둡니다.

| 경로 | 내용 | 제한 |
|---|---|---|
| `20_PROJECTS/PEER_REVIEWS/` | 심사 중인 원고 | AI 작업이 파일을 명시할 때만 열람. 외부 AI 서비스 전송 금지. 명시가 없으면 폴더·파일 이름만 다룸 |
| `50_PSYLAB/20_JIN/` | 개인 출장·재무 기록 | 같음 |
| 제한 자료 | PDK·foundry·NDA 자료, 라이선스 벤더 문서 (예: `30_TECHNICAL_WIKI/EDA_Workflows/RTL_Design_Bootcamp/Reference/`) | 업로드와 장문 인용 금지 |

## 도구-설정

| 계층 ([작업 공간 계층](Workspace_and_Tools.md#작업-공간-계층)) | 이 회사의 도구 | 설정 |
|---|---|---|
| 문서 저장소 | Obsidian | Markdown 링크 사용 (`useMarkdownLinks: true`), 이름 변경 시 링크 자동 갱신 |
| 작업 관리 | TaskNotes 4.11.1 | task 식별 `task` 태그, 의존성 필드 `blockedBy`, `tasksFolder` = `00_HQ/10_PLANNING/TaskNotes/Tasks`, 제외 폴더 `00_HQ/90_SYSTEM/Templates`·`20_PROJECTS/_PROJECT_TEMPLATE` |
| 뷰 | Obsidian Bases | [`{task-views}`](#작업-공간-경로)의 `tasks.base` 외 5개 |
| 버전 관리 | git, 중첩 저장소 15개 | [버전 관리 설정](#버전-관리-설정) |
| 동기화 | Dropbox | git 데이터와 `.venv`는 동기화 제외 (`com.dropbox.ignored`) |
| 대용량 미디어 | [`{assets-folder}`](#작업-공간-경로) | 목록은 `00_HQ/90_SYSTEM/External_Media_Index.md` |
| 스크립트 런타임 | 도입 시 실행 파일과 버전을 확인 | 이번 검사 환경: Python 3.12.12. 표준 라이브러리만 사용 |
| 다이어그램 | Mermaid | GitHub와 Obsidian 공용 |
| 현황 명령 `{status-command}` | `TaskNotes 현황 보여줘` | [채팅 명령](../HQ/Commands_and_Approval.md#채팅-명령) |
| TaskNote 기록의 링크 형식 `{record-link-format}` | 전체 Vault 경로 wikilink `[[경로\|표시 이름]]`. 표 안에서는 `\|`로 이스케이프, 폴더는 링크하지 않음, Vault 밖 파일은 `file:///` 링크 | [기록 형식의 링크](../AI/Reporting_Style.md#링크) |

## 버전-관리-설정

| 이름 | 값 |
|---|---|
| `{remote}` | `git@github.gatech.edu:jkwak77/JouleMatter.git` |
| 프로토콜 전용 remote | `https://github.com/jinwoongkwak/JM_Protocol.git` — 회사 Vault 이력과 분리 |
| `{main-branch}` | `main` — HQ만 merge |
| `{ai-branch}` | `ai/work` — AI 작업 브랜치 |
| `{git-data}` | `D:\GaTech\git_data\JouleMatter.git` (Vault의 `.git`은 위치만 가리키는 파일) |
| 커밋 메시지 | `<task 제목>: <변경 내용>`, task 하나에 commit 하나 |
| `{large-file-limit}` | 25MB (commit 전 staged 파일 크기 검사) |
| git에서 제외하는 것 | 기밀 폴더, 라이선스 자료, 바이너리(pdf·Office·Visio·eps·압축·미디어), OAuth secret이 있는 설정. 이들은 zip 백업과 Dropbox로 보관 |
| 중첩 저장소 설정 | `submodule.recurse = true`, `push.recurseSubmodules = check`, `fetch.recurseSubmodules = on-demand`, `status.submoduleSummary = true`, `diff.submodule = log`, `.gitmodules`의 `branch`와 `ignore = untracked` |
| 저장소 목록 | `30_TECHNICAL_WIKI/Repositories/Repository_Catalog.md` |
| 접근 권한 | github.gatech.edu SSH 키, `jkwak77`·`psylab`·`ECE-4804-F22` 읽기 권한. `upb-lea/Inkscape_electric_Symbols`는 github.com 공개 |

이 값을 쓰는 절차는 [버전 관리](../AI/Common_Rules.md#버전-관리)와 [중첩 저장소](../AI/Common_Rules.md#중첩-저장소)에 있습니다.

## 명명-규칙

| 대상 | 형식 | 예 |
|---|---|---|
| 프로젝트 | `PYYNN_SHORTNAME` (YY 시작 연도, NN 연내 순번) | `P2501_PKG_PD_CODESIGN` |
| 협업 프로젝트 | 같은 번호 체계, `20_PROJECTS/COLLABORATIONS/` | `P2602_NGMM` |
| 날짜 노트 | `YYYY-MM-DD_<주제>.md` | `2026-09-11_NGMM_Report.md` |
| 외부 산출물 | `YYYY-MM-DD_<ID>_<TYPE>_<주제>_v<NN>` (TYPE: RPT, TALK, PAPER, POSTER) | `2026-09-01_P2602_TALK_NGMM-Review_v03.pptx` |
| 데이터·시뮬레이션 결과 | `<ID>_<DATASET>_<YYYYMMDD>[_<조건>]` | `P2501_CapLUT_20260914_85C` |
| 결정 기록 | `DEC-<ID>-NNN` | `DEC-HQ-005`, `DEC-P2501-003` |
| Wiki 노트 | ID 없는 `Title_Case` | `Flip_Chip_Packaging` |
| 저장소 | 원래 이름 유지 | `power_card_rev2_pcb` |
| 심사 원고 | 저널 원고 ID | `JSSC-26-0317` |
| AI TaskNote | 할 일을 바로 나타내는 제목, `결정 -`·`작업 -`·`확인 -` 접두사 없음 | `P2501 커패시터 LUT 파이프라인` |
| JM_Protocol 문서 | 공백 없는 영어 `Title_Case` | `Command_and_Report_Flow.md` |

## 근거-자료

JM_Protocol 밖의 원문은 이 표에만 경로로 둡니다 ([링크와 연결](../HQ/Protocol_Governance.md#링크와-연결)).

| 원천 | 경로 | 반영한 문서 |
|---|---|---|
| AI 운영 규약 | `00_HQ/90_SYSTEM/AI_Control/AI_Protocol.md` | [공통 규칙](../AI/Common_Rules.md), [문서 체계](Document_System.md), [위험도와 권한](Risk_and_Authority.md), [작업 흐름](../AI/Workflow.md), [제어 설정](../HQ/Control_Settings.md) |
| 작업 인계 규약 | `00_HQ/90_SYSTEM/AI_Control/Handoff_Protocol.md` | [명령과 보고 체계](Command_and_Report_Flow.md), [명령과 승인](../HQ/Commands_and_Approval.md), [검토와 종료](../HQ/Review_and_Closure.md) |
| 권한과 안전 | `00_HQ/90_SYSTEM/AI_Control/Permissions_and_Safety.md` | [공통 규칙](../AI/Common_Rules.md) |
| 기록 형식 | `00_HQ/90_SYSTEM/AI_Control/Report_Style_Guide.md` | [기록 형식](../AI/Reporting_Style.md) |
| 전문 역할 | `00_HQ/90_SYSTEM/AI_Control/Agent_Roles.md` | [전문 역할](../AI/Roles/Specialist_Roles.md) |
| AI task 템플릿 | `00_HQ/90_SYSTEM/AI_Control/Templates/AI_TASK.md` | [작업과 기록 스키마](../AI/Task_and_Record_Schema.md) |
| Vault 규칙 | `00_HQ/90_SYSTEM/Conventions.md` | 이 문서 |
| HQ 결정 | `00_HQ/Decisions.md`의 DEC-HQ-001–005 | [운영 모델](Operating_Model.md), [명령과 보고 체계](Command_and_Report_Flow.md), [작업 공간과 도구](Workspace_and_Tools.md) |
| 운영체계 제안 | `00_HQ/10_PLANNING/TaskNotes/Tasks/AI/HQ 중심 다중 Agent 연구 운영체계 설계.md`, 같은 이름 폴더의 제안서 01–06과 `초안/AI_Protocol/` | [조직 구조](Organization.md), AI 폴더 전체 (proposed) |
| 문서화 작업 | `00_HQ/10_PLANNING/TaskNotes/Tasks/AI/JM_Protocol 문서화.md` | 최초 문서화 이력. 현재 승인 목록은 [README 마지막 섹션](../README.md#관리자-검토-체크리스트) |
| 구조 검토 작업 | `00_HQ/10_PLANNING/TaskNotes/Tasks/AI/JM_Protocol 구조 검토와 저장소 배포.md` | 0.2.0 개선·검증·배포 이력 |

## 알려진-문제

| 문제 (2026-09-15 확인) | 영향 | 처리 위치 |
|---|---|---|
| 현행 AI_Protocol·HQ CONTEXT·Decisions 등에 병합 충돌 표시가 남음 | 해당 문서는 정본 교체 전에 복구 필요. 과거의 전체 개수는 현재 검증값으로 재사용하지 않음 | TaskNote `Vault 병합 충돌 복구` |
| 현재 PC에는 Vault `.git` 포인터와 외부 git-data가 있고 ai/work로 연결됨. 인덱스 미병합 항목은 없으나 작업 트리 수정 다수 | 과거 “Git 부재” 기록은 다른 환경의 관찰. 기존 수정 보존과 실행 시 재점검 필요 | [이전 선행 조건](../Setup/Migration.md#선행-조건) |
| TaskNotes 제외 폴더에 AI 템플릿 폴더가 없음 | AI task 템플릿이 작업으로 색인될 수 있음 | 제안서 03 Q4 |
| 기존 규약의 `blocked_by`와 TaskNotes의 `blockedBy` 이름 불일치 | 의존성 표시가 어긋날 수 있음. 확장 모드 채택 때 task 링크와 외부 조건을 구분해 전환 | [스키마](../AI/Task_and_Record_Schema.md#대표-task-필드-변경-제안) |

## 관련-문서

- [작업 공간과 도구](Workspace_and_Tools.md) — 이 값들이 들어가는 일반 모델
- [다른 기업에 도입하기](../HQ/Protocol_Governance.md#다른-기업에-도입하기) — 이 문서를 바꿔 다른 기업에 적용하는 절차
- [용어집](Glossary.md) — `{이름}` 값이 쓰이는 용어
