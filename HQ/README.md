---
type: agent-node-governance
layer: hq
status: active
version: 1.3.1
updated: 2026-09-16
---

# hq

## overview

처음에는 [관리자 운영 매뉴얼](Operating_Manual_admin.md)을 읽습니다. HQ 폴더는 회사를 운영하는 사람([HQ](../Architecture/Operating_Model_admin.md#hq와-ai의-뜻))의 매뉴얼입니다. HQ가 무엇을 하고, 작업마다 무엇을 조절할 수 있으며, 어떻게 지시·승인·검토하는지 설명합니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [하루와-한-주](#하루와-한-주) | HQ가 실제로 하는 일의 흐름 | 운영 매뉴얼 |
| [문서-목록](#문서-목록) | HQ 문서와 답하는 질문 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 다른 폴더 안내 | 운영 매뉴얼 |

## 하루와-한-주

| 언제 | HQ가 하는 일 | 방법 |
|---|---|---|
| 맡길 일이 생겼을 때 | 채팅으로 요청하거나 초안만 요청 | [채팅 명령](Commands_and_Approval_admin.md#채팅-명령) |
| 결정 요청을 받았을 때 | 결정표를 채우고 승인 | [결정표 작성](Commands_and_Approval_admin.md#결정표-작성) |
| manual 작업을 시작할 때 | `<제목> 실행해` | [승인과 실행 지시](Commands_and_Approval_admin.md#승인과-실행-지시) |
| 궁금할 때 | 현황 요약 요청 | [현황 보기](Review_and_Closure_admin.md#현황-보기) |
| 검토 대기 작업이 있을 때 | 결과를 확인하고 종료하거나 수정 요청 | [결과 검토](Review_and_Closure_admin.md#결과-검토) |
| 매주 | 프로젝트 STATUS를 훑고 다음 작업을 정함 | [운영 주기](HQ_Role_admin.md#운영-주기) |

매일 확인해야 하는 대시보드나 기본 일괄 실행 명령은 없습니다.

## 문서-목록

| 문서 | 답하는 질문 | 주요 섹션 |
|---|---|---|
| [HQ의 역할](HQ_Role_admin.md) | HQ는 무엇을 책임지나 | [HQ의 책임](HQ_Role_admin.md#hq의-책임), [주의력 예산](HQ_Role_admin.md#주의력-예산) |
| [제어 설정](Control_Settings_admin.md) | 작업마다 무엇을 조절할 수 있나 | [조절 값 한눈에](Control_Settings_admin.md#조절-값-한눈에), [기본값](Control_Settings_admin.md#기본값) |
| [명령과 승인](Commands_and_Approval_admin.md) | 어떻게 지시하고 승인하나 | [채팅 명령](Commands_and_Approval_admin.md#채팅-명령), [버전 규칙](Commands_and_Approval_admin.md#버전-규칙) |
| [검토와 종료](Review_and_Closure_admin.md) | 결과를 어떻게 확인하고 닫나 | [결과 검토](Review_and_Closure_admin.md#결과-검토), [후속 제안 처리](Review_and_Closure_admin.md#후속-제안-처리) |
| [프로토콜 관리](Protocol_Governance_admin.md) | 이 규칙은 어떻게 바꾸고 옮기나 | [변경 절차](Protocol_Governance_admin.md#변경-절차), [다른 기업에 도입하기](Protocol_Governance_admin.md#다른-기업에-도입하기) |

## 관련-문서

- [AGENT_NODE_GOVERNANCE 안내](../README.md) — 전체 문서 지도
- [Architecture 안내](../Architecture/README.md) — 회사 구조
- [AI 안내](../AI/README.md) — AI가 HQ 지시를 받아 일하는 방식
