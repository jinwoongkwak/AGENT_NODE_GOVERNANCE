---
type: agent-node-governance
layer: architecture
status: active
version: 1.6.1
updated: 2026-09-23
---

# 용어집

## overview

AGENT_NODE_GOVERNANCE에 나오는 용어의 뜻과 그 용어를 정의한 섹션입니다. 다른 문서는 문서마다 용어를 처음 쓸 때 `정의` 열의 섹션으로 링크합니다 ([링크와 연결](../HQ/Protocol_Governance_admin.md#링크와-연결)).

| 섹션 | 내용 | 적용 |
|---|---|---|
| [조직-용어](#조직-용어) | 사람과 역할 | 운영 매뉴얼 |
| [작업-용어](#작업-용어) | 작업 단위, 승인, 상태, 평가 | 운영 매뉴얼 |
| [문서-용어](#문서-용어) | 문서 종류와 형식 | 운영 매뉴얼 |
| [기술-용어](#기술-용어) | 도구와 실행 장치 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 용어가 많이 쓰이는 문서 | 운영 매뉴얼 |

## 조직-용어

| 용어 | 뜻 | 정의 | 상태 |
|---|---|---|---|
| 1인 기업 모델 | 한 사람은 결정만 맡고 나머지 일은 AI Agent가 끝내는 운영 방식 | [왜-1인-기업-모델인가](Operating_Model_admin.md#왜-1인-기업-모델인가) | 운영 |
| HQ | 목표·우선순위·승인을 결정하는 사람. 이 회사에서는 [`{hq-person}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#사람과-역할-배정) | [hq와-ai의-뜻](Operating_Model_admin.md#hq와-ai의-뜻) | 운영 |
| AI Agent | HQ의 지시를 받아 일을 수행하는 AI 실행 주체 | [hq와-ai의-뜻](Operating_Model_admin.md#hq와-ai의-뜻) | 운영 |
| 과정 역할 | 작업 순서에서 맡는 책임. Coordinator, Planner, Evaluator, Executor | [과정-역할](Organization_admin.md#과정-역할) | 확장 사양 |
| Coordinator | 작업 계약 고정, 호출 순서, 상태, 저장, HQ 인계를 맡는 역할 | [역할-요약](../AI/Roles/Coordinator_agent.md#role-summary) | 확장 사양 |
| Planner | 완료 기준을 만족하는 실행 가능한 계획을 쓰는 역할 | [역할-요약](../AI/Roles/Planner_agent.md#role-summary) | 확장 사양 |
| Evaluator | 계획을 평가하고 실행 결과를 검증하는 역할 | [역할-요약](../AI/Roles/Evaluator_agent.md#role-summary) | 확장 사양 |
| Executor | 통과·승인된 계획을 실행하고 증거를 모으는 역할 | [역할-요약](../AI/Roles/Executor_agent.md#role-summary) | 확장 사양 |
| 전문 역할 | 분야별 기준을 가진 역할. Research Scout, Design Reviewer, Data Analyst, Publication Editor | [전문-역할](Organization_admin.md#전문-역할) | 운영 |

## 작업-용어

| 용어 | 뜻 | 정의 | 상태 |
|---|---|---|---|
| TaskNote | AI 작업 하나의 지시·상태·결정·계획·기록을 담는 노트. 대표 노트라고도 부름 | [작업-문서](Document_System_admin.md#작업-문서) | 운영 |
| 작업 계약 | 목표·산출물·입력·범위·완료 기준·위임 권한·예산·보고 시점을 고정한 지시 | [계약-정규화](../AI/Roles/Coordinator_agent.md#contract-normalization) | 확장 사양 |
| 위험도 | 작업의 권한·피해 가능성 등급 0–2 | [위험도](Risk_and_Authority_admin.md#위험도) | 운영 |
| 실행 모드 | 승인과 실행을 어떻게 나눌지 정하는 값. autonomous, after-approval, manual | [실행-모드](Risk_and_Authority_admin.md#실행-모드) | 운영 |
| 검토 깊이 | 작업에 들이는 검토량. 경량, 표준, 엄격 | [검토-깊이](Risk_and_Authority_admin.md#검토-깊이) | 확장 사양 |
| 보고 정책 | HQ에게 언제 알릴지 정하는 값. decision-only, milestone, final | [보고-정책](../HQ/Control_Settings_admin.md#보고-정책) | 운영 |
| 쓰기 범위 | AI가 수정할 수 있는 경로 목록 (`write_scope`) | [쓰기-범위](../HQ/Control_Settings_admin.md#쓰기-범위) | 운영 |
| 작업 상태 | `status`·`owner`·`hq_todo` 값의 허용 조합 6가지 | [작업-상태](Command_and_Report_Flow_admin.md#작업-상태) | 운영 |
| 승인 | HQ가 제안 버전을 채택하는 행위 | [승인과-실행-지시](../HQ/Commands_and_Approval_admin.md#승인과-실행-지시) | 운영 |
| 실행 지시 | manual 작업을 시작하게 하는 별도 명령 (`<제목> 실행해`), dispatch라고도 부름 | [승인과-실행-지시](../HQ/Commands_and_Approval_admin.md#승인과-실행-지시) | 운영 |
| 버전 | 제안·승인 버전 `V<major>.<minor>.<patch>` | [버전-규칙](../HQ/Commands_and_Approval_admin.md#버전-규칙) | 운영 |
| 동시 실행 제한 | 프로젝트당 실행 작업 1개, 쓰기 범위가 겹치는 작업 동시 실행 금지 | [동시-실행-제한](../HQ/Control_Settings_admin.md#동시-실행-제한) | 운영 |
| 후속 제안 | 미해결·인계가 남을 때 쓰는 중복 없는 다음 버전 제안 | [후속-제안-처리](../HQ/Review_and_Closure_admin.md#후속-제안-처리) | 운영 |
| run | 한 계약 버전으로 진행하는 교환 기록 묶음 | [id와-파일명](../AI/Task_and_Record_Schema_agent.md#ids-and-filenames) | 확장 사양 |
| 필수 조건 | 하나라도 실패하면 계획을 실행하지 않는 조건 G1–G6 | [필수-조건](../AI/Roles/Evaluator_agent.md#required-conditions) | 확장 사양 |
| 판정 | 평가·검증 결과 값 (`verdict`) | [판정](../AI/Roles/Evaluator_agent.md#verdicts) | 확장 사양 |
| 발견 | Evaluator가 기록한 결함 (finding) | [발견-기록](../AI/Roles/Evaluator_agent.md#recording-findings) | 확장 사양 |
| checkpoint | 중단·대기 전에 저장하는 재개 정보 | [checkpoint와-재개](../AI/Roles/Coordinator_agent.md#checkpoint-and-resume) | 확장 사양 |
| receipt | 실행 단계가 끝났다는 기록 | [receipt와-재시도](../AI/Roles/Executor_agent.md#receipts-and-retries) | 확장 사양 |
| 독립 확인 | 기본 모드에서 작성과 분리된 새 문맥 subagent가 결과나 계획을 확인하는 절차 | [independent-check](../AI/Workflow_agent.md#independent-check) | 운영 매뉴얼 |

## 문서-용어

| 용어 | 뜻 | 정의 | 상태 |
|---|---|---|---|
| 정본 | 현재 상태와 결정의 권위 있는 원본 문서 | [정본-문서](Document_System_admin.md#정본-문서) | 운영 |
| STATUS | 프로젝트의 현재 상태 문서. Agent가 가장 먼저 읽는 인계 문서 | [정본-문서](Document_System_admin.md#정본-문서) | 운영 |
| Decisions | HQ 결정을 `DEC-<ID>-NNN`으로 남기는 영구 기록 | [정본-문서](Document_System_admin.md#정본-문서) | 운영 |
| CONTEXT | 영역별 AI 작업 안내 문서 | [정본-문서](Document_System_admin.md#정본-문서) | 운영 |
| 교환 기록 | 역할 사이에 오간 instruction, plan, evaluation 같은 기록 | [교환-기록](Document_System_admin.md#교환-기록) | 확장 사양 |
| 결정표 | 번호·질문·선택지·AI 권장·결정 열을 가진 표 | [결정표-작성](../HQ/Commands_and_Approval_admin.md#결정표-작성) | 운영 |
| 스키마 | 문서 종류·필드·본문 구획·문서 사이 규칙의 약속 | [스키마란](../AI/Task_and_Record_Schema_agent.md#what-is-a-schema) | 확장 사양 |
| 불변식 | 문서 사이에 항상 성립해야 하는 규칙 | [불변식](../AI/Task_and_Record_Schema_agent.md#invariants) | 확장 사양 |
| 조항 번호 | CO·PL·EV·EX로 시작하는 역할 조항 ID | [문서-작성-규칙](../HQ/Protocol_Governance_admin.md#문서-작성-규칙) | 확장 사양 |
| 로드맵 | 프로젝트나 포트폴리오의 방향, 다음 단계, 일정을 담은 HQ 승인 정본 | [roadmap](../AI/Roadmap_agent.md) | 운영 매뉴얼 |

## 기술-용어

| 용어 | 뜻 | 정의 | 상태 |
|---|---|---|---|
| 작업 공간 계층 | 문서 저장소, 작업 관리, 버전 관리, 동기화, 런타임 | [작업-공간-계층](Workspace_and_Tools_admin.md#작업-공간-계층) | 운영 |
| 휴지통 | 삭제 대신 파일을 옮기는 곳 ([`{trash}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로)) | [파일-작업](../AI/Common_Rules_agent.md#file-operations) | 운영 |
| 백업 | 수정 전에 만드는 복구 지점. git commit 또는 zip | [백업](../AI/Common_Rules_agent.md#backup) | 운영 |
| 중첩 저장소 | 작업 공간 안에 있는 git 저장소 (submodule) | [중첩-저장소](../AI/Common_Rules_agent.md#nested-repositories) | 운영 |
| Router | TaskNote와 교환 기록 파일을 만들고 제자리에 두는 명령줄 프로그램 | [router의-역할](../AI/Routing_agent.md#router-role) | 확장 사양 |
| 스테이징 | 역할이 본문을 먼저 써 두는 동기화 밖 임시 위치 | [런타임과-router](Workspace_and_Tools_admin.md#런타임과-router) | 확장 사양 |
| 잠금 | 같은 작업·경로를 두 세션이 동시에 쓰지 못하게 하는 표시 | [잠금과-예산](../AI/Roles/Coordinator_agent.md#locks-and-budget) | 확장 사양 |

## 관련-문서

- [조직 구조](Organization_admin.md) — 조직 용어가 모여 있는 문서
- [명령과 보고 체계](Command_and_Report_Flow_admin.md) — 작업 용어가 흐름 속에서 쓰이는 방식
- [링크와 연결](../HQ/Protocol_Governance_admin.md#링크와-연결) — 새 용어를 추가하고 링크하는 규칙
