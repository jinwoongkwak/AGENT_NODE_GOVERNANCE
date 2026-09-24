---
type: agent-node-governance
layer: root
status: active
version: 1.5.0
updated: 2026-09-23
---

# agent-node-governance-운영-매뉴얼

## overview

관리자가 1인 연구 회사를 이해하고 제어하며, AI가 같은 구조의 회사를 설립하고 자료를 배치할 수 있도록 정한 운영 매뉴얼입니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [바로-시작](#바로-시작) | 바로 시작 | 운영 매뉴얼 |
| [회사-운영-구조](#회사-운영-구조) | 회사 운영 구조 | 운영 매뉴얼 |
| [문서-지도](#문서-지도) | 문서 지도 | 운영 매뉴얼 |
| [상태-표시](#상태-표시) | 상태 표시 | 운영 매뉴얼 |
| [독자별-읽는-순서](#독자별-읽는-순서) | 독자별 읽는 순서 | 운영 매뉴얼 |
| [도입과-구조-개선](#도입과-구조-개선) | 도입과 구조 개선 | 운영 매뉴얼 |
| [버전과-변경-이력](#버전과-변경-이력) | 버전과 변경 이력 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 관련 문서 | 운영 매뉴얼 |
| [관리자-검토-체크리스트](#관리자-검토-체크리스트) | 관리자 검토 체크리스트 | 운영 매뉴얼 |

## 바로-시작

| 할 일 | 시작 문서 |
|---|---|
| 회사가 어떻게 작동하는지 이해·제어 | [관리자 운영 매뉴얼](HQ/Operating_Manual_admin.md) |
| 현재 작업을 맡길 Agent | [Agent 진입점](AI/Agent_Entry_agent.md) → 회사 로컬 프로필·채택 기록·TaskNote |
| 같은 형식의 새 회사를 설립 | [AI 회사 설립 지침](Setup/AI_Bootstrap_agent.md) |
| 기존 자료를 적절한 곳에 배치 | [자료 배치 기준](Setup/Material_Placement_agent.md) |
| 기존 회사를 전환 | [이전 절차](Setup/Migration_admin.md) |

이 매뉴얼 전체를 AI 컨텍스트로 제공하고 설립 지침의 요청 양식을 채우면 됩니다. 실제 회사의 목적·권한·기밀·자료 경로는 함께 제공해야 합니다.

## 회사-운영-구조

HQ가 목적·기준·우선순위·위임 밖의 결정을 맡고, Agent가 승인된 범위의 계획·실행·검증·기록을 맡습니다. 작업은 TaskNote, 현재 상태는 STATUS, 영구 결정은 Decisions에 남깁니다.

| 층 | 역할 |
|---|---|
| [Architecture](Architecture/README.md) | 회사의 역할·문서·작업 공간·권한 구조 |
| [HQ](HQ/README.md) | 관리자의 요청·승인·제어·결과 검토 |
| [AI](AI/README.md) | Agent의 읽기 순서·실행·검증·기록 |
| [Setup](Setup/README.md) | 새 회사 설립·기존 회사 이전·자료 배치 |

기본 모드는 단일 Agent와 TaskNote로 운영합니다. 확장 모드는 역할 분리·교환 기록·Router를 추가하는 선택 기능이며, 구현·시험 후에만 활성화합니다.

## 문서-지도

| 문서 | 용도 |
|---|---|
| [운영 모델](Architecture/Operating_Model_admin.md), [조직](Architecture/Organization_admin.md) | 역할과 책임 |
| [명령과 보고](Architecture/Command_and_Report_Flow_admin.md), [문서 체계](Architecture/Document_System_admin.md) | 정보 흐름과 정본 |
| [권한](Architecture/Risk_and_Authority_admin.md), [도구](Architecture/Workspace_and_Tools_admin.md) | 안전과 실행 환경 |
| [폴더 구조](Architecture/Workspace_Layout_admin.md), [회사 프로필](Architecture/Company_Profile_admin.md), [용어집](Architecture/Glossary_admin.md) | 경로·회사 값·개념 |
| [frontmatter](Architecture/Frontmatter_admin.md), [기계 판독판](Architecture/Frontmatter_agent.json) | 문서 종류별 frontmatter 필드와 허용 값 |
| [제어 설정](HQ/Control_Settings_admin.md), [명령·승인](HQ/Commands_and_Approval_admin.md), [검토·종료](HQ/Review_and_Closure_admin.md) | 관리자 실무 |
| [Agent 진입점](AI/Agent_Entry_agent.md) | 지시를 받은 Agent가 매번 먼저 읽는 판단 기준 |
| [공통 규칙](AI/Common_Rules_agent.md), [흐름](AI/Workflow_agent.md), [기록](AI/Reporting_Style_agent.md) | 기본 Agent 운영 |
| [스키마](AI/Task_and_Record_Schema_agent.md), [라우팅](AI/Routing_agent.md) | 확장 모드 사양 |
| [채택 기록](Setup/Adoption_admin.md), [템플릿](Setup/Templates_agent.md) | 회사별 설치·승인 |
| [설립 도구](tools/bootstrap.py), [구조 검사](tools/check_workspace.py), [문서 검사](tools/validate.py), [진입점 생성](tools/build_entry.py) | 제공되는 실행 도구 |

[기업 구조 비교](AI_Agent_Company_Comparison_admin.md)는 0.2.0 시점의 참고 분석입니다. 현행 규칙이나 현재 구현 상태의 정본이 아닙니다.

## 상태-표시

| 표시 | 의미 |
|---|---|
| active / 운영 | 승인된 공통 운영 매뉴얼 |
| specification / 확장 | 채택된 확장 사양. Router 런타임 구현 완료를 뜻하지 않음 |
| 회사 채택 상태 | 로컬 Protocol_Adoption.md의 draft·approved·active |
| 작업 승인 상태 | TaskNote의 실제 HQ 결정과 approved_version |

다른 회사는 원래 회사의 승인이나 기밀 정책을 상속하지 않습니다. 공통 매뉴얼, 회사 설정, 적용 버전을 분리합니다.

## 독자별-읽는-순서

관리자는 [운영 매뉴얼](HQ/Operating_Manual_admin.md), 실행 Agent는 [Agent 진입점](AI/Agent_Entry_agent.md), 새 회사 설립 Agent는 [설립 지침](Setup/AI_Bootstrap_agent.md)부터 읽습니다. 용어는 [용어집](Architecture/Glossary_admin.md)에서 찾습니다.

Agent는 진입점 한 문서로 판단을 끝내고, 나머지 문서는 [작업 유형별 경로](AI/Agent_Entry_agent.md#paths-by-task-type)가 요구할 때만 엽니다. 사람이 구조를 배우는 순서는 [Architecture 안내](Architecture/README.md#읽는-순서)에 있습니다.

## 도입과-구조-개선

공통 프로토콜·로컬 프로필·회사 채택 기록을 분리합니다. 기본/확장 모드, 경량 작업, 승인 전 계획 작성, 실행 권한 확인, 불변 기록·스키마 고정·중복 실행 방지 규칙을 일관되게 적용합니다. 초기 설립은 dry-run 가능한 생성기를 쓰고 자료 이동은 별도 대응표로 수행합니다.

## 버전과-변경-이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| 1.5.0 | 2026-09-23 | `_agent` 파일 17개 중 한국어가 있던 16개(Markdown 14·JSON 2)를 영어로 번역하고 제목·앵커를 영어로 바꿈. `_admin` 문서와 README는 한국어 유지, 링크만 새 앵커로 갱신. HQ에게 쓰는 기록·보고·결정표·채팅은 한국어라는 규칙을 [기록 구조](AI/Reporting_Style_agent.md#record-structure)에 추가. vault에 들어가는 템플릿·기록 토큰(`# 기록`, 기록 단계 등)은 한국어 유지. 검사기가 `_agent` 문서의 마지막 섹션 `related-documents`를 확인 |
| 1.4.0 | 2026-09-16 | HQ 검토가 남은 AI TaskNote를 `done` 대신 `in-progress / {hq-owner} / review`로 둠. `completedDate`는 종료일 때만 쓰고 검사기가 어긋남을 보고. HQ에게 넘기는 기록 단계 `검토 요청` 추가 |
| 1.3.1 | 2026-09-16 | 1.3.0 frontmatter 필드를 상태 표·HQ 매뉴얼·TaskNote 템플릿·bootstrap에 반영 (`hq` → `hq_todo`, `priority` 행 정리). 검사기가 값 없는 선택 키 누락·TaskNote 제목과 파일 이름 불일치·빈 필수 목록을 보고. 문서 정렬을 운영체제와 무관하게 고정 |
| 1.3.0 | 2026-09-16 | frontmatter 형식 승인. TaskNote `hq` → `hq_todo`, `priority`·`urgency` 삭제, `status`에 `delayed` 추가, AI가 쓴 문서에 `llm_model`, 제안서에 `recommended_model` 도입, 프로젝트 README `partners` → `collaborators`와 `codename` 삭제, 이론 Wiki 필드 정리 |
| 1.2.0 | 2026-09-16 | 문서 파일 이름에 주 독자 접미사 `_agent`·`_admin` 적용, 검사기가 Obsidian vault 경로 형식 링크를 해석, frontmatter 형식 초안(`Frontmatter_admin.md`·`Frontmatter_agent.json`)과 보고 전용 검사기 추가 |
| 1.1.0 | 2026-09-16 | Agent 진입점 문서와 컨텍스트 매니페스트 추가, 작업 유형별 읽기 경로, 확장 사양 표시, 생성물 드리프트 검사, 저장소 이름 AGENT_NODE_GOVERNANCE 반영 |
| 1.0.0 | 2026-09-16 | C1–C10 승인 반영, 기본 운영 매뉴얼, 회사 설정 분리, AI 설립·자료 배치 지침과 생성·검사 도구 |
| 0.2.0 | 2026-09-15 | 구조 검토, Setup·템플릿·이전 절차·관리자 체크리스트 |
| 0.1.0 | 2026-09-15 | 첫 통합 초안 |

업데이트는 [프로토콜 관리](HQ/Protocol_Governance_admin.md)를 따릅니다. 회사의 실제 적용 commit은 로컬 채택 기록에 고정합니다.

## 관련-문서

- [관리자 운영 매뉴얼](HQ/Operating_Manual_admin.md)
- [AI 회사 설립 지침](Setup/AI_Bootstrap_agent.md)
- [프로토콜 관리](HQ/Protocol_Governance_admin.md)

## 관리자-검토-체크리스트

**승인 이력:** 출처 회사 관리자가 v0.2.0의 C1–C10을 모두 승인했고 2026-09-16 적용을 지시했습니다. 아래 체크는 그 이력을 보존합니다. 현재 운영은 이 매뉴얼과 회사의 로컬 채택 기록을 따르며 새 회사의 승인으로 재사용하지 않습니다.

- [x] **C1 구조·재사용 범위** — [작업 공간 구조](Architecture/Workspace_Layout_admin.md#최소-구조), [설치와 도입](Setup/README.md#새-기업-시작), [문서 작성 규칙](HQ/Protocol_Governance_admin.md#문서-작성-규칙)을 검토합니다. Architecture·HQ·AI·Setup 구성, 로컬 프로필 분리, 상대 링크와 제목 규칙을 채택할지 확인합니다.

- [x] **C2 권한·승인 경계** — [위험도와 실행 모드](Architecture/Risk_and_Authority_admin.md#위험도), [승인과 실행 지시](HQ/Commands_and_Approval_admin.md#승인과-실행-지시), [실행 전 검사](AI/Roles/Executor_agent.md#pre-execution-check)를 검토합니다. 명시 실행 요청의 효력, 조건부 승인, autonomous의 권한 근거를 확인합니다.

- [x] **C3 역할과 도입 모드** — [기본·확장 모드](Setup/README.md#도입-모드), [책임 매트릭스](Architecture/Organization_admin.md#책임-매트릭스), [호출 규칙](AI/Roles/Coordinator_agent.md#invocation-rules)을 검토합니다. AI 권장: 기본 모드로 시작하고, 확장 모드는 구현·파일럿 통과 뒤 활성화합니다.

- [x] **C4 스키마·기록 보존** — [task 필드](AI/Task_and_Record_Schema_agent.md#primary-task-field-changes-extended), [불변식](AI/Task_and_Record_Schema_agent.md#invariants), [스키마 변경](AI/Task_and_Record_Schema_agent.md#schema-changes)을 검토합니다. task_id, blockedBy 전환, run별 스키마 고정, 과거 불변 기록 보존을 확인합니다.

- [x] **C5 Router와 작업 뷰** — [처리 순서](AI/Routing_agent.md#processing-order), [실패와 동시성](AI/Routing_agent.md#failures-and-concurrency), [HQ 행동 뷰](Architecture/Workspace_and_Tools_admin.md#hq-행동-뷰-확장)를 검토합니다. 구현 범위, 중복·부분 실패·경로 검증, 템플릿 제외와 done 상태의 검토 대기 표시를 확정합니다.

- [x] **C6 평가 기준·예산·증거** — [통과 조건](AI/Roles/Evaluator_agent.md#pass-conditions), [예산](HQ/Control_Settings_admin.md#예산과-반복-한도), [연구 증거 추적](AI/Roles/Evaluator_agent.md#research-evidence-tracing)을 검토합니다. AI 권장 B: 모든 항목 4/5·필수 gate·blocking 0을 통과 기준으로 하고 총점은 기록만 합니다. A를 원하면 총점 85 하한도 추가합니다. 선택과 예외를 채택 기록에 적습니다.

- [x] **C7 상태·중단·재개** — [작업 상태](Architecture/Command_and_Report_Flow_admin.md#작업-상태), [checkpoint](AI/Roles/Coordinator_agent.md#checkpoint-and-resume), [receipt](AI/Roles/Executor_agent.md#receipts-and-retries)를 검토합니다. 상태 6개, 단일 실행 기기, 성공 단계만 생략, 실행 중 job의 자원 예약을 확인합니다.

- [x] **C8 이전 전 환경·복구** — [알려진 문제](Architecture/Company_Profile_admin.md#알려진-문제), [선행 조건](Setup/Migration_admin.md#선행-조건), [백업](AI/Common_Rules_agent.md#backup)을 검토합니다. 기존 충돌 복구와 tracked·untracked·ignored 자료 백업, 실제 복원 시험을 이전의 선행 조건으로 확정합니다.

- [x] **C9 전체 재구조화 범위** — [이전 대응표](Setup/Migration_admin.md#이전-대응표), [실행과 복구](Setup/Migration_admin.md#실행과-복구), [정본 교체](HQ/Protocol_Governance_admin.md#정본-교체-절차)를 검토합니다. 기존 최상위 영역 유지, 진입 파일·규약·CONTEXT·템플릿 갱신, 실제 파일별 이동표를 바탕으로 실행 범위를 승인합니다.

- [x] **C10 채택·배포 정책** — [승인 기록](Setup/Adoption_admin.md#승인-기록), [저장소 운영](Setup/README.md#저장소-운영), [완료 기준](Setup/Migration_admin.md#완료-기준)을 검토합니다. 적용 commit·로컬 프로필·모드·예외·공개 범위·제3자 라이선스를 확정하고, 기존 운영 결정을 대체하는 실제 DEC를 기록합니다. 이미 요청한 GitHub push와 운영 활성화는 별개입니다.
