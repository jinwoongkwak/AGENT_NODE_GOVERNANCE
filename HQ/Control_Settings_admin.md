---
type: agent-node-governance
layer: hq
status: active
version: 1.5.0
updated: 2026-09-23
---

# 제어-설정

## overview

HQ가 작업마다 조절할 수 있는 값과 기본값입니다. 값은 [TaskNote](../Architecture/Document_System_admin.md#작업-문서)의 frontmatter나 `# 지시`에 적고, 채팅의 `승인:`·`수정:`으로도 바꿀 수 있습니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [조절-값-한눈에](#조절-값-한눈에) | 조절할 수 있는 값 전체 | 운영 매뉴얼 |
| [위험도와-실행-모드](#위험도와-실행-모드) | 위험도와 실행 모드를 고르는 법 | 운영 매뉴얼 |
| [보고-정책](#보고-정책) | AI가 보고하는 시점 | 운영 매뉴얼 |
| [쓰기-범위](#쓰기-범위) | AI가 수정할 수 있는 경로 | 운영 매뉴얼 |
| [예산과-반복-한도](#예산과-반복-한도) | 시간·호출·반복 상한 | 운영 매뉴얼 |
| [검토-깊이-선택](#검토-깊이-선택) | 경량·표준·엄격을 고르는 예 | 운영 매뉴얼 |
| [위임-범위](#위임-범위) | AI가 묻지 않고 고를 수 있는 선택 | 운영 매뉴얼 |
| [동시-실행-제한](#동시-실행-제한) | 동시에 실행하는 작업 수와 겹침 | 운영 매뉴얼 |
| [기본값](#기본값) | 따로 정하지 않았을 때의 값 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 정의 문서 | 운영 매뉴얼 |

## 조절-값-한눈에

| 값 | 적는 곳 | 선택지 | 정의 | 상태 |
|---|---|---|---|---|
| 위험도 | `risk` | 0, 1, 2 | [위험도](../Architecture/Risk_and_Authority_admin.md#위험도) | 운영 |
| 실행 모드 | `execution_mode` | autonomous, after-approval, manual | [실행 모드](../Architecture/Risk_and_Authority_admin.md#실행-모드) | 운영 |
| 보고 정책 | `report_policy` | decision-only, milestone, final | [보고 정책](#보고-정책) | 운영 |
| 쓰기 범위 | `write_scope` | 경로 목록 | [쓰기 범위](#쓰기-범위) | 운영 |
| 의존성 | `blockedBy` | 막고 있는 task 링크 | [대표 task 필드](../AI/Task_and_Record_Schema_agent.md#primary-task-fields) | 운영 |
| 일정 | `scheduled`, `due` | 작업 관리 도구의 값 | [tasknote 필드](../Architecture/Frontmatter_admin.md#tasknote-필드) | 운영 |
| 예산과 반복 한도 | `# 지시`의 [작업 계약](../AI/Roles/Coordinator_agent.md#contract-normalization) | 시간, 호출 수, 반복 횟수 | [예산과 반복 한도](#예산과-반복-한도) | 확장 사양 |
| 검토 깊이 | `# 현재 상태` | 경량, 표준, 엄격 | [검토 깊이](../Architecture/Risk_and_Authority_admin.md#검토-깊이) | 확장 사양 |
| 위임 범위 | `# 지시`의 작업 계약 | AI가 고를 수 있는 선택 목록 | [위임 범위](#위임-범위) | 확장 사양 |
| 자원 키 | `# 지시`의 작업 계약 | 라이선스·장비 이름 | [잠금과 예산](../AI/Roles/Coordinator_agent.md#locks-and-budget) | 확장 사양 |

## 위험도와-실행-모드

위험도와 실행 모드의 뜻은 [위험도와 권한](../Architecture/Risk_and_Authority_admin.md#위험도)에만 정의합니다. HQ가 할 수 있는 조절은 다음과 같습니다.

- **위험도 올리기:** AI가 제안한 위험도가 낮다고 보면 올립니다. 등급이 애매하면 높은 쪽을 씁니다.

- **더 엄격한 모드:** HQ는 언제든 더 엄격한 실행 모드를 고를 수 있습니다. 예를 들어 위험도 1 작업도 manual로 둘 수 있습니다.

- **바꾸는 방법:** TaskNote의 `risk`, `execution_mode`를 직접 고치거나 `승인:`에 조건으로 적습니다.

### 모드-선택-가이드-확장

| 상황 | 권장 모드 |
|---|---|
| 처음 맡기는 종류의 일 | after-approval 또는 manual |
| 절차가 검증된 반복 문서 정리 | autonomous |
| 실행 시점을 HQ가 직접 고르고 싶은 위험도 2 작업 | manual |
| 계획을 승인하면 바로 진행해도 되는 작업 | after-approval |

## 보고-정책

| 값 | AI가 보고하는 때 | 적합한 작업 |
|---|---|---|
| `decision-only` | 결정, 권한, 실패, 중단 조건이 생겼을 때만 | 오래 걸리는 반복 작업 |
| `milestone` | 번호가 붙은 milestone이 끝날 때 | 여러 단계로 나눈 도입 작업 |
| `final` | 완료하거나 중단했을 때 | 대부분의 작업 |

보고의 형식은 [기록 형식](../AI/Reporting_Style_agent.md#record-structure)을, 보고가 오가는 흐름은 [보고 흐름](../Architecture/Command_and_Report_Flow_admin.md#보고-흐름)을 봅니다.

## 쓰기-범위

- **정의:** `write_scope`는 AI가 수정할 수 있는 경로 목록입니다. AI는 여기에 적힌 경로만 [위험도](../Architecture/Risk_and_Authority_admin.md#위험도) 규칙 안에서 수정합니다.

- **기록 위치:** 작업 기록과 근거 요약은 경로와 상관없이 같은 TaskNote 안에 둡니다.

- **영역 기본값:** 영역마다 기본 쓰기 범위가 [CONTEXT](../Architecture/Document_System_admin.md#정본-문서)에 있으며, 작업은 이를 좁힐 수 있습니다.

- **확장:** 쓰기 범위를 넓히려면 새 승인이 필요합니다 ([판단 권한 경계](../Architecture/Risk_and_Authority_admin.md#판단-권한-경계)).

- **기밀 경로:** [기밀 영역](../Architecture/Company_Profile_admin.md#기밀-영역)이 들어가면 위험도 2이며, 작업이 경로를 명시해야 열 수 있습니다.

## 예산과-반복-한도

| 항목 | 기본값 | 넘으면 | 정의 |
|---|---|---|---|
| 계획 평가 | 최초 포함 3회 | HQ 보고 + 제안서 | [반복 한도](../AI/Roles/Evaluator_agent.md#iteration-limit) |
| 같은 blocking 발견 | 연속 2회 | 3회를 기다리지 않고 HQ | 같은 곳 |
| 결과 보완 | 같은 기준·범위 안에서 2회 | HQ | [검증 판정과 보완 한도](../AI/Roles/Evaluator_agent.md#verification-verdict-and-fix-limit) |
| 문서 계획 단계 | 활동 시간 30분, 모델 호출 10회 | 먼저 닿은 상한에서 멈추고 요약 | [잠금과 예산](../AI/Roles/Coordinator_agent.md#locks-and-budget) |
| 실행 시간·EDA 자원 | 작업 계약에 명시 | 문서 작업의 30분 한도를 적용하지 않음 | 같은 곳 |
| 새 유료 사용·라이선스 | 기존 허용 범위만 | HQ | [HQ로 올리는 조건](../AI/Roles/Coordinator_agent.md#escalation-to-hq) |

수치는 시범 운영의 초기값이며, HQ만 조정합니다. AI는 스스로 올리거나 내리지 않습니다.

## 검토-깊이-선택

[검토 깊이](../Architecture/Risk_and_Authority_admin.md#검토-깊이)는 AI가 접수할 때 정하고 진행 중에는 올리기만 합니다. HQ는 요청할 때 깊이를 지정하거나, AI가 정한 깊이를 낮출 수 있습니다.

| 작업의 예 | 권장 깊이 |
|---|---|
| 오탈자·링크 수정 | 경량 |
| 읽기만 하지만 연구 방향을 좌우하는 문헌 조사 | 표준 |
| 여러 단계의 분석 코드 작성 | 표준 |
| 제출용 수치 확정, 핵심 설계 결정 | 엄격 |

## 위임-범위

- **적는 곳:** 작업 계약에 AI가 묻지 않고 고를 수 있는 선택을 적습니다. 기본은 구현 방법, 작업 순서, 한도 안의 재시도입니다.

- **HQ에게 남는 것:** 목표, 완료 기준, 범위, 위험도의 변경은 항상 HQ가 결정합니다 ([확장 판단 경계](../Architecture/Risk_and_Authority_admin.md#판단-경계-확장)).

- **예:** 허용된 분석 코드의 처리 순서는 AI가 바꾸지만, 허용 오차를 완화하거나 새 회로 폴더를 수정하려면 HQ에게 올립니다.

- **반복 승인 없음:** 미리 위임한 선택은 다시 묻지 않습니다. 반대로 위임하지 않은 결정은 평가 점수가 높아도 AI가 대신하지 않습니다.

## 동시-실행-제한

| 규칙 | 내용 | 상태 |
|---|---|---|
| 프로젝트당 실행 작업 | 기본 1개 | 운영 |
| 쓰기 범위 겹침 | 겹치는 작업은 동시에 실행하지 않음. HQ가 명시적으로 지시하면 예외 | 운영 |
| 파일이 아닌 자원 | 라이선스·장비는 자원 키로 표시하고 같은 키의 작업을 동시에 실행하지 않음 | 확장 사양 |
| 실행 기기 | 시범 운영 기간에는 지정 기기 한 대의 Coordinator 하나만 실행 | 확장 사양 ([실행 기기 제한](../Architecture/Workspace_and_Tools_admin.md#실행-기기-제한-확장)) |

## 기본값

| 값 | 기본 | 상태 |
|---|---|---|
| 위험도 0–1의 실행 모드 | autonomous | 운영 |
| 위험도 2의 실행 모드 | manual | 운영 |
| 보고 정책 | final | 운영 |
| 프로젝트당 실행 작업 | 1개 | 운영 |
| 한 작업의 HQ 결정·행동 | 10개 이하 | 운영 |
| 계획 평가 횟수 | 최초 포함 3회 | 확장 사양 |
| 계획 통과 항목 하한 | 모든 항목 4/5 이상 | 확장 사양 |
| 결과 보완 | 2회 | 확장 사양 |

## 관련-문서

- [위험도와 권한](../Architecture/Risk_and_Authority_admin.md) — 조절 값의 정의
- [명령과 승인](Commands_and_Approval_admin.md) — 설정을 채팅으로 바꾸는 방법
- [Evaluator](../AI/Roles/Evaluator_agent.md) — 반복 한도와 통과 조건의 적용
- [HQ의 역할](HQ_Role_admin.md) — 설정을 고르는 사람의 책임
