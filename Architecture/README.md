---
type: pod-protocol
layer: architecture
status: active
version: 1.0.0
updated: 2026-09-16
---

# architecture

## overview

Architecture 폴더는 회사가 어떻게 생겼는지 설명합니다. 누가 결정하고 누가 일하는지, 명령과 보고가 어떤 길로 오가는지, 무엇을 어디에 기록하는지, 어디까지 AI에게 맡기는지를 다룹니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [읽는-순서](#읽는-순서) | 처음 읽을 때의 순서 | 운영 매뉴얼 |
| [문서-목록](#문서-목록) | 문서마다 답하는 질문과 주요 섹션 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 다른 폴더 안내 | 운영 매뉴얼 |

## 읽는-순서

| 순서 | 문서 | 이 문서를 읽고 나면 |
|---:|---|---|
| 1 | [운영 모델](Operating_Model.md) | 왜 사람은 결정만 하고 AI가 나머지를 하는지 설명할 수 있음 |
| 2 | [조직 구조](Organization.md) | HQ와 AI 역할의 책임을 구분할 수 있음 |
| 3 | [명령과 보고 체계](Command_and_Report_Flow.md) | 지시 한 건이 보고로 끝나기까지의 경로를 따라갈 수 있음 |
| 4 | [문서 체계](Document_System.md) | 어떤 정보를 어느 문서에 둘지 고를 수 있음 |
| 5 | [위험도와 권한](Risk_and_Authority.md) | 어떤 일에 승인이 필요한지 판단할 수 있음 |
| 6 | [작업 공간과 도구](Workspace_and_Tools.md) | 필요한 도구와 그 역할을 알 수 있음 |

[회사 프로필](Company_Profile.md)과 [용어집](Glossary.md)은 처음부터 읽기보다 링크를 따라 필요할 때 엽니다.

## 문서-목록

| 문서 | 답하는 질문 | 주요 섹션 |
|---|---|---|
| [운영 모델](Operating_Model.md) | 왜 이런 구조인가 | [운영 원칙](Operating_Model.md#운영-원칙), [HQ와 AI의 뜻](Operating_Model.md#hq와-ai의-뜻) |
| [조직 구조](Organization.md) | 누가 무엇을 책임지나 | [과정 역할](Organization.md#과정-역할), [책임 매트릭스](Organization.md#책임-매트릭스) |
| [명령과 보고 체계](Command_and_Report_Flow.md) | 명령과 보고는 어떻게 오가나 | [전달 체계 한눈에](Command_and_Report_Flow.md#전달-체계-한눈에), [작업 상태](Command_and_Report_Flow.md#작업-상태) |
| [문서 체계](Document_System.md) | 무엇을 어디에 기록하나 | [정본 문서](Document_System.md#정본-문서), [무엇을 어디에 두나](Document_System.md#무엇을-어디에-두나) |
| [위험도와 권한](Risk_and_Authority.md) | 어디까지 맡기나 | [위험도](Risk_and_Authority.md#위험도), [판단 권한 경계](Risk_and_Authority.md#판단-권한-경계) |
| [작업 공간과 도구](Workspace_and_Tools.md) | 어떤 도구 위에서 돌아가나 | [작업 공간 계층](Workspace_and_Tools.md#작업-공간-계층), [도구 요구 조건](Workspace_and_Tools.md#도구-요구-조건) |
| [작업 공간 구조](Workspace_Layout.md) | 무엇을 어느 폴더에 두나 | [최소 구조](Workspace_Layout.md#최소-구조), [배치 판단](Workspace_Layout.md#배치-판단) |
| [회사 프로필](Company_Profile.md) | 이 회사의 실제 값은 무엇인가 | [작업 공간 경로](Company_Profile.md#작업-공간-경로), [알려진 문제](Company_Profile.md#알려진-문제) |
| [용어집](Glossary.md) | 이 말은 무슨 뜻이고 어디서 정의했나 | [작업 용어](Glossary.md#작업-용어) |

## 관련-문서

- [POD_PROTOCOL 안내](../README.md) — 전체 문서 지도와 독자별 경로
- [HQ 안내](../HQ/README.md) — 운영자가 할 일
- [AI 안내](../AI/README.md) — Agent가 일하는 방식
