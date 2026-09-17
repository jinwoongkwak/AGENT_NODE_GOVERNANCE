---
type: agent-node-governance
layer: hq
status: active
version: 1.3.1
updated: 2026-09-16
---

# hq의-역할

## overview

HQ가 책임지는 일, AI에게 넘기지 않는 판단, 운영 주기, 주의력을 아끼는 규칙을 설명합니다. HQ가 무엇인지는 [HQ와 AI의 뜻](../Architecture/Operating_Model_admin.md#hq와-ai의-뜻)에 정의되어 있습니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [hq의-책임](#hq의-책임) | 방향, 요청, 결정, 실행 지시, 검토, 규칙 관리 | 운영 매뉴얼 |
| [위임하지-않는-판단](#위임하지-않는-판단) | HQ에게 올라오는 결정의 종류 | 운영 매뉴얼 |
| [운영-주기](#운영-주기) | 필요할 때, 매주, 하지 않는 것 | 운영 매뉴얼 |
| [주의력-예산](#주의력-예산) | 한 번에 받는 결정의 양과 측정 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 설정과 명령 | 운영 매뉴얼 |

## hq의-책임

| 책임 | 내용 | 남는 곳 |
|---|---|---|
| 방향 설정 | 연구 목적, 성공 기준, 우선순위, 자원 배분 | 프로젝트 README·STATUS, [Decisions](../Architecture/Document_System_admin.md#정본-문서) |
| 작업 요청 | 어느 프로젝트에서 무엇을 어떤 기준으로 끝낼지. 나머지는 AI가 초안으로 채움 | [TaskNote](../Architecture/Document_System_admin.md#작업-문서) `# 지시` |
| 결정 | 결정표의 선택, [위험도](../Architecture/Risk_and_Authority_admin.md#위험도) 2 작업의 승인 | [결정표](Commands_and_Approval_admin.md#결정표-작성), `approved_version` |
| 실행 지시 | manual 작업의 시작과 중단 | [승인과 실행 지시](Commands_and_Approval_admin.md#승인과-실행-지시) |
| 검토 | 검토 대기 산출물 확인, 종료 또는 수정 요구 | [결과 검토](Review_and_Closure_admin.md#결과-검토) |
| 규칙 관리 | 운영 규칙 변경의 승인 | [변경 절차](Protocol_Governance_admin.md#변경-절차) |

HQ가 작업마다 조절하는 값은 [제어 설정](Control_Settings_admin.md#조절-값-한눈에)에 있습니다.

## 위임하지-않는-판단

AI가 스스로 처리하는 판단과 HQ가 맡는 판단의 경계는 [판단 권한 경계](../Architecture/Risk_and_Authority_admin.md#판단-권한-경계)에, HQ만 할 수 있는 행위는 [위임하지 않는 행위](../Architecture/Risk_and_Authority_admin.md#위임하지-않는-행위)에 정의되어 있습니다. HQ 입장에서 받게 되는 결정 요청은 다음과 같습니다.

| 결정 요청의 종류 | 예 |
|---|---|
| 위험도 2 작업의 승인 | 파일 이동, 설정 변경, commit·push, 기밀 영역 접근 |
| 목표·완료 기준·범위 변경 | 원래 계획에 없던 폴더나 데이터 추가 |
| 연구 방향과 trade-off | 효율·면적·과도응답 중 무엇을 우선할지 |
| 외부에 영향을 주는 행위 | 제출, 외부 발신, 원본 대체 |
| Agent가 할 수 없는 일 | 장비 조작, 외부 확인 |

### 결정-요청-증가-조건-확장

[과정 역할](../Architecture/Organization_admin.md#과정-역할)을 도입하면 계획 평가 한도 초과, 결과 보완 한도 초과, 검증 불가(`inconclusive`)도 HQ 결정 요청이 됩니다 ([HQ로 올리는 조건](../AI/Roles/Coordinator_agent.md#hq로-올리는-조건)).

## 운영-주기

| 주기 | HQ가 하는 일 | 비고 |
|---|---|---|
| 필요할 때 | 현황 요약 요청 ([`{status-command}`](../Architecture/Company_Profile_admin.md#도구-설정)) | [현황 보기](Review_and_Closure_admin.md#현황-보기) |
| 매주 | 프로젝트 STATUS를 훑고 다음 작업을 정함. 주간 결과는 각 STATUS의 이번 주 결과 구획에 적음 | 별도 주간·분기 계획 노트는 만들지 않음 |
| 매주 (요청할 때) | AI에게 7일 넘게 멈춘 작업, HQ 대기 작업, [쓰기 범위](Control_Settings_admin.md#쓰기-범위)가 겹치는 작업 목록을 요청 | [동시 실행 제한](Control_Settings_admin.md#동시-실행-제한) |

매일 확인하는 대시보드와 기본 일괄 실행 명령은 두지 않습니다.

## 주의력-예산

| 규칙 | 내용 | 상태 |
|---|---|---|
| 작업당 결정 상한 | 한 TaskNote에서 HQ가 처리할 결정과 행동은 합쳐 10개 이하. 넘으면 AI가 작업을 나눔 | 운영 |
| 선택지와 권장 | 결정표에는 선택지와 AI 권장이 함께 있음 | 운영 |
| 결정표는 한 곳 | HQ는 대표 TaskNote의 결정표 한 곳에만 답함 | 운영 |

### 주의력-측정-확장

| 규칙 | 내용 |
|---|---|
| 질문 묶기 | 같은 결과·승인 경계의 질문은 한 요청으로 묶고 권장 3개 이하 |
| 측정 | 작업당 HQ 질문 수, 중복 질문 수, 재작업 수를 기록 |
| 읽기 시간 | HQ가 알려 줄 때만 기록하고, 추정한 시간을 측정값처럼 보고하지 않음 |

## 관련-문서

- [제어 설정](Control_Settings_admin.md) — 작업마다 조절하는 값
- [명령과 승인](Commands_and_Approval_admin.md) — 결정과 승인을 전하는 방법
- [운영 모델](../Architecture/Operating_Model_admin.md) — "사람은 결정만" 원칙
- [HQ 안내](README.md) — HQ 문서 목록
