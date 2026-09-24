---
type: agent-node-governance
layer: architecture
status: active
version: 1.6.1
updated: 2026-09-23
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
| 1 | [운영 모델](Operating_Model_admin.md) | 왜 사람은 결정만 하고 AI가 나머지를 하는지 설명할 수 있음 |
| 2 | [조직 구조](Organization_admin.md) | HQ와 AI 역할의 책임을 구분할 수 있음 |
| 3 | [명령과 보고 체계](Command_and_Report_Flow_admin.md) | 지시 한 건이 보고로 끝나기까지의 경로를 따라갈 수 있음 |
| 4 | [문서 체계](Document_System_admin.md) | 어떤 정보를 어느 문서에 둘지 고를 수 있음 |
| 5 | [위험도와 권한](Risk_and_Authority_admin.md) | 어떤 일에 승인이 필요한지 판단할 수 있음 |
| 6 | [작업 공간과 도구](Workspace_and_Tools_admin.md) | 필요한 도구와 그 역할을 알 수 있음 |

[회사 프로필](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md)과 [용어집](Glossary_admin.md)은 처음부터 읽기보다 링크를 따라 필요할 때 엽니다.

이 순서는 사람이 구조를 배우는 경로입니다. 지시를 처리하는 Agent는 [Agent 진입점](../AI/Agent_Entry_agent.md)만 읽고, 나머지는 [작업 유형별 경로](../AI/Agent_Entry_agent.md#paths-by-task-type)가 요구할 때만 엽니다.

## 문서-목록

| 문서 | 답하는 질문 | 주요 섹션 |
|---|---|---|
| [운영 모델](Operating_Model_admin.md) | 왜 이런 구조인가 | [운영 원칙](Operating_Model_admin.md#운영-원칙), [HQ와 AI의 뜻](Operating_Model_admin.md#hq와-ai의-뜻) |
| [조직 구조](Organization_admin.md) | 누가 무엇을 책임지나 | [과정 역할](Organization_admin.md#과정-역할), [책임 매트릭스](Organization_admin.md#책임-매트릭스) |
| [명령과 보고 체계](Command_and_Report_Flow_admin.md) | 명령과 보고는 어떻게 오가나 | [전달 체계 한눈에](Command_and_Report_Flow_admin.md#전달-체계-한눈에), [작업 상태](Command_and_Report_Flow_admin.md#작업-상태) |
| [문서 체계](Document_System_admin.md) | 무엇을 어디에 기록하나 | [정본 문서](Document_System_admin.md#정본-문서), [무엇을 어디에 두나](Document_System_admin.md#무엇을-어디에-두나) |
| [위험도와 권한](Risk_and_Authority_admin.md) | 어디까지 맡기나 | [위험도](Risk_and_Authority_admin.md#위험도), [판단 권한 경계](Risk_and_Authority_admin.md#판단-권한-경계) |
| [작업 공간과 도구](Workspace_and_Tools_admin.md) | 어떤 도구 위에서 돌아가나 | [작업 공간 계층](Workspace_and_Tools_admin.md#작업-공간-계층), [도구 요구 조건](Workspace_and_Tools_admin.md#도구-요구-조건) |
| [작업 공간 구조](Workspace_Layout_admin.md) | 무엇을 어느 폴더에 두나 | [최소 구조](Workspace_Layout_admin.md#최소-구조), [배치 판단](Workspace_Layout_admin.md#배치-판단) |
| [회사 프로필](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md) | 이 회사의 실제 값은 무엇인가 | [작업 공간 경로](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#작업-공간-경로), [알려진 문제](AGENT_NODE_GOVERNANCE/Architecture/Company_Profile_admin.md#알려진-문제) |
| [용어집](Glossary_admin.md) | 이 말은 무슨 뜻이고 어디서 정의했나 | [작업 용어](Glossary_admin.md#작업-용어) |
| [frontmatter](Frontmatter_admin.md) | 문서 종류마다 frontmatter에 어떤 필드와 값을 쓰나 | [tasknote](Frontmatter_admin.md#tasknote), [hq-결정-기록](Frontmatter_admin.md#hq-결정-기록) |

## 관련-문서

- [AGENT_NODE_GOVERNANCE 안내](../README.md) — 전체 문서 지도와 독자별 경로
- [HQ 안내](../HQ/README.md) — 운영자가 할 일
- [AI 안내](../AI/README.md) — Agent가 일하는 방식
