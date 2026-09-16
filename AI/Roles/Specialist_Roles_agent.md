---
type: agent-node-governance
layer: ai
status: active
version: 1.3.0
updated: 2026-09-16
---

# 전문-역할

## overview

전문 역할은 분야별 기준을 가진 역할입니다. 제품이나 모델 이름이 아니라 책임으로 정의하며, 역할의 기본 정의는 [조직 구조의 전문 역할](../../Architecture/Organization_admin.md#전문-역할)에 있습니다. 이 문서는 각 역할이 적용하는 기준과 [과정 역할](../../Architecture/Organization_admin.md#과정-역할)과 결합하는 방법을 설명합니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [전문-역할-목록](#전문-역할-목록) | 역할마다 적용하는 기준 | 운영 매뉴얼 |
| [과정-역할과-결합](#과정-역할과-결합) | 과정 역할과 짝지을 때 맡는 일 | 운영 매뉴얼 |
| [금지-행위](#금지-행위) | 전문 역할이 좁힐 수는 있어도 약하게 할 수 없는 규칙 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 조직 구조와 과정 역할 | 운영 매뉴얼 |

## 전문-역할-목록

| 역할 | 적용하는 기준 | 기대 산출 |
|---|---|---|
| Research Scout | 출처의 신뢰도, 검색 범위와 제외 기준, 인용의 추적 가능성 | 인용이 달린 근거 요약 |
| Design Reviewer | 설계 체크리스트, 위험 순위, spec과의 일치 | 위험 순으로 정렬한 발견 |
| Data Analyst | 재현성, 원 데이터 불변, 학습·검증 데이터 분리 | 재현 가능한 분석 보고 |
| Publication Editor | 주장과 근거의 대응, 투고처 조건, 과장 여부 | 수정안과 남은 공백 |

작업마다 이 기본값을 좁힐 수 있습니다. 예를 들어 특정 저널의 투고 규정만 보도록 Publication Editor의 범위를 줄일 수 있습니다.

## 과정-역할과-결합

과정 역할은 "언제 무엇을 넘기나"를, 전문 역할은 "어떤 전문 기준으로 보나"를 정합니다. Coordinator가 호출할 때 결합할 전문 역할을 정해 전달물에 적습니다 ([호출 순서](Coordinator_agent.md#호출-순서)).

| 전문 역할 | [Planner](Planner_agent.md#전문-역할-결합)와 결합 | [Evaluator](Evaluator_agent.md#필수-조건)와 결합 | [Executor](Executor_agent.md#실행)와 결합 |
|---|---|---|---|
| Research Scout | 검색 범위·출처 기준 계획 | 인용·출처 검증 | 검색·요약 실행 |
| Design Reviewer | 설계 제약 표 | 설계 결함을 위험 순으로 제시 | — |
| Data Analyst | 데이터 분리·재현 계획 | 재현성·데이터 누수 검사 | 승인된 분석 실행 |
| Publication Editor | 주장–근거 대응 계획 | 근거를 넘는 주장 검사 | 승인된 문장 수정 |

## 금지-행위

| 역할 | 금지 |
|---|---|
| Research Scout | 출처를 지어내거나 숨김 |
| Design Reviewer | 범위 없이 설계 데이터베이스 수정 |
| Data Analyst | 원 데이터 변경 |
| Publication Editor | 근거 없는 주장을 과장 |
| 모든 전문 역할 | NDA·기밀·안전 규칙을 약하게 만드는 일 ([기밀](../Common_Rules_agent.md#기밀), [파일 작업](../Common_Rules_agent.md#파일-작업)) |

## 관련-문서

- [조직 구조](../../Architecture/Organization_admin.md) — 전문 역할의 정의와 조직 속 위치
- [Planner](Planner_agent.md), [Evaluator](Evaluator_agent.md), [Executor](Executor_agent.md) — 결합하는 과정 역할
- [AI 안내](../README.md) — AI 문서 목록
