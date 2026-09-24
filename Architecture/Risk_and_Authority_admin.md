---
type: agent-node-governance
layer: architecture
status: active
version: 1.6.1
updated: 2026-09-23
---

# 위험도와-권한

## overview

어떤 일을 AI가 스스로 하고 어떤 일에 [HQ](Operating_Model_admin.md#hq와-ai의-뜻)의 승인이 필요한지 정의합니다. 위험도, 실행 모드, 검토 깊이, 판단 경계는 이 문서에서만 정의하고 다른 문서는 여기로 링크합니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [위험도](#위험도) | 0–2 등급과 필요한 문서 구조 | 운영 매뉴얼 |
| [실행-모드](#실행-모드) | autonomous, after-approval, manual | 운영 매뉴얼 |
| [검토-깊이](#검토-깊이) | 경량, 표준, 엄격 | 운영 매뉴얼 |
| [판단-권한-경계](#판단-권한-경계) | AI가 맡는 판단과 HQ가 맡는 판단 | 운영 매뉴얼 |
| [위임하지-않는-행위](#위임하지-않는-행위) | 누구에게도 자동으로 맡기지 않는 행위 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 설정과 확인 절차 | 운영 매뉴얼 |

## 위험도

| 위험도 | 예 | 필요한 TaskNote 구조 | 기본 실행 |
|---|---|---|---|
| 0 | 검색, 분석, 목록 작성 | `# 지시`, `# 현재 상태`, `# 기록` | autonomous, 최종 보고 1회 |
| 1 | 범위 안의 되돌릴 수 있는 텍스트 수정: 링크 수정, 노트 편집, STATUS 본문 갱신, DEC 기록, TaskNote 생성 | 위험도 0 구조 + 짧은 `# 실행 계획`. 먼저 [백업](../AI/Common_Rules_agent.md#backup) | autonomous (HQ가 더 엄격한 모드를 고를 수 있음) |
| 2 | 파일 이동·삭제, [버전 관리](../AI/Common_Rules_agent.md#version-control) 상태 변경, STATUS frontmatter 필드, [기밀 영역](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#기밀-영역), 외부 전송, 작업 공간 설정, 20개 넘는 파일의 일괄 수정 | 버전 붙은 전체 구조, [결정표](../HQ/Commands_and_Approval_admin.md#결정표-작성), 계획, 검증, 복구 방법 | manual: 먼저 승인, 실행 지시를 기다림 |

- **애매하면 높은 쪽:** 두 등급 사이에서 판단이 갈리면 높은 등급을 씁니다.

- **나눠서 피하지 않기:** 20개 넘는 일괄 변경을 여러 번으로 나눠 위험도 2를 피하지 않습니다.

## 실행-모드

| 모드 | 실행 권한이 생기는 때 | 승인 후 상태 |
|---|---|---|
| `autonomous` | 작성된 task와 [쓰기 범위](../HQ/Control_Settings_admin.md#쓰기-범위)가 위험도 0–1 실행을 허락 | `owner: ai`, `hq_todo: none` |
| `after-approval` | HQ 승인이 실행 권한도 줌 | `owner: ai`, `hq_todo: none` |
| `manual` | 승인은 계획만 기록하고, HQ가 별도로 실행을 지시 | `owner: {hq-owner}`, `hq_todo: dispatch` |

- **기본값:** 위험도 0–1은 autonomous, 위험도 2는 manual입니다.

- **더 엄격하게:** HQ는 언제든 더 엄격한 모드를 고를 수 있습니다 ([위험도와 실행 모드 설정](../HQ/Control_Settings_admin.md#위험도와-실행-모드)).

- **manual의 뜻:** manual 작업은 승인이 실행을 뜻하지 않습니다 ([실행 지시 흐름](Command_and_Report_Flow_admin.md#실행-지시-흐름)).

## 검토-깊이

위험도가 권한과 피해 가능성이라면, 검토 깊이는 작업에 들이는 검토량입니다. 파일을 읽기만 하는 위험도 0 문헌 분석도 핵심 연구 판단이면 표준 깊이가 될 수 있습니다.

| 깊이 | 조건 | 필수 절차 |
|---|---|---|
| 경량 | 위험도 0–1, 단순·가역적, 기존 절차와 객관적인 완료 기준이 분명 | instruction → 실행 → [독립 확인](../AI/Workflow_agent.md#independent-check) → report (위험도 0은 HQ 요청 시) |
| 표준 | 연구 판단, 여러 단계, 재작업 가능성이 큼 | 계획과 평가 반복 → 실행 → 독립 결과 검증 |
| 엄격 | 위험도 2, 핵심 설계, 공개 산출물, 오류 비용이 큼 | 표준 + HQ 권한 확인 + 작업별 검증 강화 |

접수할 때 정하고, 진행 중에는 올리기만 할 수 있습니다 ([검토 깊이와 위험도](../AI/Roles/Coordinator_agent.md#review-depth-and-risk-level)).

## 판단-권한-경계

위험도 0–1은 AI가 실행하고 기록하며, 위험도 2만 HQ 결정을 요청합니다. 승인된 결과·산출물·쓰기 범위·위험도가 바뀌면 새 승인이 필요합니다.

### 판단-경계-확장

| 판단 | 담당 | 예 |
|---|---|---|
| 정해진 기준 안의 구현 방법·작업 순서 | Planner + Evaluator | 데이터 처리 순서, 코드 모듈 분리 |
| 범위·원본 보존·예산을 지키는 수정과 재실행 | Executor + Evaluator | 실패한 분석 스크립트 수정, 검증 재실행 |
| 연구 방향, 기여 주장, 성능 trade-off | HQ | 효율·면적·과도응답 중 무엇을 우선할지 |
| 성공 기준, 산출물, 읽기·쓰기 범위 변경 | HQ | 원래 계획에 없던 회로나 데이터 추가 |
| 위험도 2 실행 | HQ가 승인한 모드에 따라 | 파일 이동, 설정 변경, commit·push, 기밀 접근 |
| tape-out, 제출, 외부 발신, 원본 대체 | HQ의 명시적 권한과 검토 | 제출용 수치·주장 확정과 실제 제출은 별도 행동 |
| Agent가 할 수 없는 장비 조작·외부 확인 | HQ 또는 지정 담당 | 필요한 조작, 기대 결과, 재개 조건을 짧게 요청 |

HQ가 미리 위임한 선택은 [작업 계약](../AI/Roles/Coordinator_agent.md#contract-normalization)에 적고 반복해서 승인받지 않습니다. 위임 범위가 없는 결정은 평가 점수로 대신하지 않습니다.

## 위임하지-않는-행위

| 행위 | 할 수 있는 주체 | 이유 |
|---|---|---|
| 주 브랜치([`{main-branch}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#버전-관리-설정))에 merge, commit, push | HQ | 정본 이력의 최종 관문 |
| 버전 관리 이력 재작성, 변경 폐기 | HQ | 되돌릴 수 없음 |
| 버전 관리에서 제외했던 파일을 추적 대상으로 변경 | HQ 결정 | 기밀·라이선스 자료 유출 위험 |
| 파일 영구 삭제 ([휴지통](../AI/Common_Rules_agent.md#file-operations) 비우기) | HQ | 복구 불가 |
| 외부 발신, 제출, tape-out | HQ의 명시적 권한 | 외부에 되돌릴 수 없는 영향 |
| 기밀 원문을 외부 AI 서비스로 전송 | 누구도 하지 않음 | 기밀 유지 의무 ([기밀](../AI/Common_Rules_agent.md#confidentiality)) |
| 원 데이터·원 보고서·EDA DB·제출 논문 덮어쓰기 | 누구도 하지 않음 | 증거 손실 |

## 관련-문서

- [제어 설정](../HQ/Control_Settings_admin.md) — HQ가 작업마다 위험도와 모드를 고르는 법
- [공통 규칙](../AI/Common_Rules_agent.md) — AI가 실행 전에 지키는 파일·백업·기밀 규칙
- [명령과 보고 체계](Command_and_Report_Flow_admin.md) — 승인과 실행 지시가 오가는 흐름
- [운영 모델](Operating_Model_admin.md) — "안전은 장치로" 원칙
