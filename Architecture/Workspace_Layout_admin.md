---
type: agent-node-governance
layer: architecture
status: active
version: 1.4.0
updated: 2026-09-16
---

# 작업-공간-구조

## overview

폴더보다 정보의 소유권을 먼저 정합니다. 기존 최상위 영역을 유지하면서 회사 운영, 프로젝트 증거, 재사용 지식, 외부 협업을 구분하는 권장 구조입니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [최소-구조](#최소-구조) | 새 회사의 기본 폴더 | 운영 매뉴얼 |
| [프로젝트-수명](#프로젝트-수명) | 시작·실행·종료와 정본 | 운영 매뉴얼 |
| [배치-판단](#배치-판단) | 중복 없이 자료를 두는 기준 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 도입과 문서 규칙 | 운영 매뉴얼 |

## 최소-구조

```text
workspace/
  AGENTS.md
  00_HQ/
    README.md                 # 현재 우선순위와 문서 지도
    Project_Index.md          # STATUS를 요약하는 뷰
    Decisions.md              # 회사 차원의 결정
    10_PLANNING/TaskNotes/Tasks/AI/        # 지시·승인·실행·보고
    90_SYSTEM/
      AGENT_NODE_GOVERNANCE/            # 상위 프로토콜 저장소
      company.json            # 기계가 읽는 회사 설정
      Company_Profile.md      # 이 회사의 경로·도구·기밀 정책
      Protocol_Adoption.md    # 채택 commit·선택·승인
  10_INBOX/                   # 아직 소유자가 없는 입력
  20_PROJECTS/<project-id>/
    README.md                 # 목적·성공 기준·범위
    STATUS.md                 # 현재 상태·다음 행동
    10_NOTES/Decisions.md
    30_SOURCE/                # 코드 저장소·데이터 색인
    60_CLOSEOUT/               # 필요 시 납품·재현·종료 근거
    _AI/CONTEXT.md
  30_TECHNICAL_WIKI/          # 재사용 절차와 도구
  40_THEORY_WIKI/             # 개념과 유도
  90_ARCHIVE/                 # 종료된 자료의 보존
  .trash/                    # 사용자만 영구 삭제
```

이는 새 회사의 예시입니다. 기존 회사의 TaskNotes 경로와 연구실 영역은 [회사 프로필](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로)에 따라 유지합니다. `50_PSYLAB` 같은 기관별 영역은 선택 사항이며 모든 회사에 의무적으로 만들지 않습니다.

## 프로젝트-수명

| 단계 | 최소 산출물 | 다음 단계 조건 |
|---|---|---|
| 시작 | README: 질문·성공 기준·범위·책임, STATUS, CONTEXT | HQ가 목적과 완료 기준을 확인 |
| 실행 | TaskNote, 결정 기록, 코드·데이터 색인 | 주장·그림·결과에서 입력과 실행 버전을 추적 가능 |
| 종료 | 결과 위치·잔여 제한·재현 방법·후속 담당 | HQ가 종료 또는 보관을 결정 |

단계가 바뀔 때 폴더를 자동 이동하지 않습니다. STATUS를 갱신하고, 보관 이동은 승인된 이전 작업으로 수행합니다. 비어 있는 산출물 폴더를 일괄 생성하지 않습니다.

## 배치-판단

| 자료 | 정본 위치 | 다른 곳에서 쓰는 방법 |
|---|---|---|
| 작업 지시·실행 근거 | TaskNote와 원본 증거 위치 | HQ 색인에서 링크 |
| 특정 연구 결과·분석 | 해당 프로젝트 | Wiki는 일반화한 절차만 기록 |
| 재사용 코드 | 독립 Git repo 또는 submodule | commit과 저장소 색인을 링크 |
| 재사용 지식 | Technical·Theory Wiki | 프로젝트에서 링크 |
| 협업 | 책임 기관이 외부인 프로젝트 하위 영역 | 같은 프로젝트 ID와 기록 규칙 |
| 기밀 자료 | 회사 프로필의 제한 영역 | 공개 repo에 복사하지 않음 |
| 교환 기록 | 확장 모드에서만 task에 종속 | 별도 업무·보고 체계로 운영하지 않음 |

파일명·폴더가 애매하면 원본을 먼저 유지하고 이전 대응표에서 결정합니다. 구조 개선을 이유로 소유권·기밀 등급·코드 저장소 경계를 바꾸지 않습니다.

## 관련-문서

- [문서 체계](Document_System_admin.md) — 정본의 역할
- [설치와 도입](../Setup/README.md) — 새 회사 시작
- [이전 절차](../Setup/Migration_admin.md) — 기존 폴더의 실제 변경
