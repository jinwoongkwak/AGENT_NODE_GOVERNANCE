---
type: agent-node-governance
layer: architecture
status: active
version: 1.6.1
updated: 2026-09-23
---

# 문서-체계

## overview

회사의 기억은 문서에 있습니다 ([운영 원칙](Operating_Model_admin.md#운영-원칙)). 이 문서는 어떤 문서가 정본이고, 작업은 어떤 문서로 관리하며, 어떤 정보를 어디에 두는지 정합니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [정본-문서](#정본-문서) | STATUS, Decisions, 프로젝트 색인, CONTEXT, Wiki | 운영 매뉴얼 |
| [작업-문서](#작업-문서) | TaskNote의 구조와 규칙 | 운영 매뉴얼 |
| [교환-기록](#교환-기록) | 역할 사이 기록의 보관 | 운영 매뉴얼 |
| [무엇을-어디에-두나](#무엇을-어디에-두나) | 정보 종류별 위치 | 운영 매뉴얼 |
| [문서-수명](#문서-수명) | 생성부터 보관까지 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 스키마와 기록 형식 | 운영 매뉴얼 |

## 정본-문서

정본은 현재 상태와 결정의 권위 있는 원본입니다. Markdown 문서가 정본이며, 시각화 파일은 연결을 보여 줄 뿐 결정을 소유하지 않습니다.

| 문서 | 역할 | 누가 쓰나 | 규칙 |
|---|---|---|---|
| STATUS | 프로젝트의 현재 상태. Agent가 가장 먼저 읽는 인계 문서 | 본문은 Agent (위험도 1), frontmatter의 `status`·`phase`·`next_deadline`은 HQ 결정 (위험도 2) | AI 분석만으로 상태를 바꾸지 않고 원 증거를 확인. AI가 쓴 초안은 `draft_by`를 달고 모르는 값은 "확인 필요" |
| Decisions | HQ 결정의 영구 기록 `DEC-<ID>-NNN` | Agent가 HQ가 결정한 내용을 기록 | 위치는 [`{decision-log}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로) |
| 프로젝트 색인 | HQ가 보는 프로젝트 요약 표, 각 STATUS로 링크 | Agent | 위치는 `{project-index}` |
| CONTEXT | 영역별 목적, 정본 목록, 기본 [쓰기 범위](../HQ/Control_Settings_admin.md#쓰기-범위), 기밀 영역 | HQ 결정으로 변경 | 위치는 [`{context-file}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로). 목록의 정본이 없으면 대체물을 만들지 않고 공백을 보고 |
| Wiki | 재사용하는 절차와 개념 | Agent | 두 번째 프로젝트가 필요로 할 때 프로젝트에서 승격하고, 원본을 복제하지 않음 |
| ROADMAP | 프로젝트의 방향과 다음 단계 3개. STATUS는 현재, ROADMAP은 앞으로 | Agent가 HQ 승인 후 작성 (위험도 1) | [로드맵](../AI/Roadmap_agent.md) 절차와 독립 확인을 거쳐 HQ가 승인한 버전만 둠. 사건이 생길 때 갱신 |
| 포트폴리오 로드맵 | 모든 프로젝트의 연결, 기술 동향, 다음 연구 방향 | Agent가 HQ 승인 후 작성 | 위치 `00_HQ/Portfolio_Roadmap.md`. 프로젝트 로드맵이 승인된 뒤에만 작성 |

STATUS 필드 값은 [회사 프로필](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#영역과-정본)의 영역별 정본 목록을 따릅니다. 변경 권한의 경계는 [위험도](Risk_and_Authority_admin.md#위험도)에 있습니다.

## 작업-문서

TaskNote는 AI 작업의 유일한 명령·보고 단위입니다. 작업 하나에 TaskNote 하나를 두고, 채팅으로 온 요청도 행동 전에 TaskNote부터 만듭니다. 위치는 [`{task-folder}`](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로)이고, 현재 파일 이름이 제목이자 식별자입니다. 확장 모드에서는 제목 변경에도 유지되는 `task_id`를 사용합니다.

| 구획 | 담는 것 | 주 독자 |
|---|---|---|
| `# 지시` | 목표, 산출물, 자료, 범위와 제외, 완료 기준 | HQ, AI |
| `# 현재 상태` | 단계, 요약, 막힘, 실행 전 확인 사항 | HQ |
| `# 결정 및 승인` | [결정표](../HQ/Commands_and_Approval_admin.md#결정표-작성), 승인 버전, 실행 경계 | HQ |
| `# 실행 계획` | 단계, 대상, 작업, 담당, 승인 필요 여부 | AI |
| `# 기록` | 버전 붙은 작업 기록 | HQ, 다음 Agent |
| `# 근거` (선택) | 긴 분석, 원본 위치, 검증 결과 | 필요할 때 |

- **위험도별 깊이:** 위험도 0은 지시·현재 상태·기록만, 위험도 1은 짧은 실행 계획을 더하고, 위험도 2는 전체 구조를 씁니다 ([위험도](Risk_and_Authority_admin.md#위험도)).

- **별도 파일 금지:** 지시서나 보고서 파일을 따로 만들지 않습니다. 원 데이터·이미지·로그는 원래 위치를 링크합니다.

- **필드:** frontmatter 필드와 허용 값은 [대표 task 필드](../AI/Task_and_Record_Schema_agent.md#primary-task-fields)에 있습니다. 문서 종류 전체를 한 형식으로 맞추는 규칙은 [frontmatter](Frontmatter_admin.md)에 있습니다.

## 교환-기록

[과정 역할](Organization_admin.md#과정-역할) 사이에 오간 instruction, plan, evaluation 같은 전달물을 교환 기록으로 남깁니다. 모든 반복을 저장하지만 HQ에게 모두 보여 주지는 않습니다.

| 규칙 | 내용 |
|---|---|
| 위치 | 대표 task 저장 폴더의 `R/` |
| 색인 | 작업 관리 도구의 작업으로 색인하지 않음. 기록 전용 뷰로 봄 |
| 이름 | 파일 이름이 기록 ID ([ID와 파일명](../AI/Task_and_Record_Schema_agent.md#ids-and-filenames)) |
| 필드 | 최대 4개 ([교환 기록 필드](../AI/Task_and_Record_Schema_agent.md#exchange-record-fields)) |
| 불변 | 발행한 기록은 고치지 않고, 정정은 새 기록으로 |
| 기록 범위 | 입력 목록, 산출물, 판단 근거 요약, 검증 결과, 다음 인계. 모델의 숨은 내부 사고 과정까지 기록하는 것은 아님 |

## 무엇을-어디에-두나

| 정보 | 두는 곳 | 두지 않는 곳 |
|---|---|---|
| 프로젝트의 현재 상태 | STATUS 본문 | TaskNote 기록 |
| HQ 결정 | Decisions의 DEC 항목 | 채팅에만 |
| 작업 지시·승인·실행·보고 | TaskNote | 별도 지시서·보고서 |
| 긴 분석, 증거 요약 | TaskNote `# 근거` | 새 보고서 파일 |
| 원 데이터·이미지·실행 로그 | 원래 위치 (링크만) | TaskNote에 복사 |
| 재사용 지식 | Technical·Theory Wiki | TaskNote |
| 운영 규칙 | 현재 활성화된 규약. AGENT_NODE_GOVERNANCE은 [채택 절차](../Setup/Adoption_admin.md#적용-상태) 완료 후 정본 | 여러 문서에 중복 |
| 역할 사이 전달물 (확장 사양) | [교환 기록](#교환-기록) | 대표 노트 본문 |

## 문서-수명

| 단계 | TaskNote | 교환 기록 (확장 사양) | 정본 |
|---|---|---|---|
| 생성 | 행동하기 전에 만듦 | 역할 산출물을 [Router](../AI/Routing_agent.md#router-role)가 발행 | 프로젝트 시작이나 HQ 결정 때 |
| 진행 | `# 현재 상태`와 `# 기록`을 갱신 | 추가만 하고 고치지 않음 | 검증된 결과만 반영 |
| 종료 | 완료 기준과 검증 통과 후 [종료](Command_and_Report_Flow_admin.md#작업-상태) | 대표 task와 함께 보존 | 유지 |
| 보관 | 이전 체계의 기록은 읽기 전용 보관소에 두고 새 기록을 이어 붙이지 않음 | 보존 | 끝난 프로젝트는 보관 영역으로 이동 |

## 관련-문서

- [작업과 기록 스키마](../AI/Task_and_Record_Schema_agent.md) — 문서 종류와 필드의 정확한 규칙
- [기록 형식](../AI/Reporting_Style_agent.md) — `# 기록`과 결정표를 쓰는 법
- [명령과 보고 체계](Command_and_Report_Flow_admin.md) — 문서가 흐름 속에서 쓰이는 순서
- [회사 프로필](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md) — 문서의 실제 경로
