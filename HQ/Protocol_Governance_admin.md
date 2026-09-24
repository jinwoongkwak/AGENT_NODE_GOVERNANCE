---
type: agent-node-governance
layer: hq
status: active
version: 1.6.1
updated: 2026-09-23
---

# 프로토콜-관리

## overview

AGENT_NODE_GOVERNANCE을 바꾸고, 정본으로 교체하고, 기여하고, 다른 기업에 옮기는 방법입니다. 대상은 [HQ](../Architecture/Operating_Model_admin.md#hq와-ai의-뜻), 기여자, 도입하려는 기업입니다.

| 섹션 | 내용 | 적용 |
|---|---|---|
| [변경-절차](#변경-절차) | 규칙을 바꾸는 순서와 버전 | 운영 매뉴얼 |
| [정본-교체-절차](#정본-교체-절차) | AGENT_NODE_GOVERNANCE을 현행 규칙의 원본으로 만드는 순서 | 운영 매뉴얼 |
| [문서-작성-규칙](#문서-작성-규칙) | 파일, frontmatter, 구성, 조항 번호 | 운영 매뉴얼 |
| [제목과-앵커](#제목과-앵커) | GitHub·Obsidian 공용 제목 규칙 | 운영 매뉴얼 |
| [링크와-연결](#링크와-연결) | 위키피디아 형식 연결과 인스턴스 값 링크 | 운영 매뉴얼 |
| [상태-표시-규칙](#상태-표시-규칙) | 운영·확장 사양 표시와 전환 | 운영 매뉴얼 |
| [기여-방법](#기여-방법) | 기여 순서와 제출 전 자가 검사 | 운영 매뉴얼 |
| [다른-기업에-도입하기](#다른-기업에-도입하기) | 이 구조를 다른 회사에 적용하는 단계 | 운영 매뉴얼 |
| [관련-문서](#관련-문서) | 함께 볼 문서 | 운영 매뉴얼 |

## 변경-절차

AGENT_NODE_GOVERNANCE의 운영 규칙 채택은 HQ 결정으로만 바뀝니다. 요청받은 초안 개선·검사·저장소 배포는 운영 채택과 별개이며, 새 규칙은 승인 전까지 초안으로 구분합니다. 확장 사양은 미승인이라는 뜻이 아니라 선택 기능의 적용 범위입니다. 변경은 일반 작업과 같은 [TaskNote](../Architecture/Document_System_admin.md#작업-문서)에서 [결정표](Commands_and_Approval_admin.md#결정표-작성)로 제안하고 승인받습니다.

| 순서 | 누가 | 할 일 |
|---:|---|---|
| 1 | HQ, AI Agent, 기여자 누구나 | 바꿀 규칙, 이유, 영향받는 문서와 섹션 앵커를 결정표로 제안 |
| 2 | HQ | [승인](Commands_and_Approval_admin.md#승인과-실행-지시)하거나 수정을 지시 |
| 3 | AI Agent | 승인 범위만 문서를 고치고 [상태 표시](#상태-표시-규칙)를 갱신 |
| 4 | AI Agent | [기여 방법](#기여-방법)의 자가 검사를 통과시킴 |
| 5 | AI Agent | 프로토콜 버전을 올리고 [변경 이력](../README.md#버전과-변경-이력)에 한 줄 추가 |
| 6 | AI Agent | 결정을 [Decisions](../Architecture/Document_System_admin.md#정본-문서)에 DEC로 기록 |

| 변경 | 프로토콜 버전 | 예 |
|---|---|---|
| 원칙, 폴더 구조, 역할 체계 변경 | major | 과정 역할 추가·삭제 |
| 규칙 추가·변경, 확장 사양를 운영로 전환 | minor | 평가 기준 수치 변경 |
| 표현·링크·오타 정정 (의미 불변) | patch | 앵커 수정 |

## 정본-교체-절차

정본 교체는 AGENT_NODE_GOVERNANCE을 현재 운영 규칙의 원본으로 만드는 일입니다. 교체할 때 기존 AI 제어 파일을 모두 새 규칙에 맞춰 갱신하고, 같은 규칙 본문을 두 곳에 남기지 않습니다.

| 순서 | 할 일 | 완료 확인 |
|---:|---|---|
| 1 | 선행 조건 해소: 작업 공간의 충돌 표시 제거, [백업](../AI/Common_Rules_agent.md#backup) 가능 상태 | [알려진 문제](../Architecture/Company_Profile_admin.md#알려진-문제)에 막힘 없음 |
| 2 | HQ가 승인 체크리스트를 모두 승인하고 실행 지시 | [승인과 실행 지시](Commands_and_Approval_admin.md#승인과-실행-지시) 기록 |
| 3 | [`{entry-files}`](../Architecture/Company_Profile_admin.md#작업-공간-경로)의 읽기 순서를 [AI 안내](../AI/README.md)로 변경 | Agent가 새 순서로 읽음 |
| 4 | [`{legacy-control-folder}`](../Architecture/Company_Profile_admin.md#작업-공간-경로)의 규약을 AGENT_NODE_GOVERNANCE 해당 섹션으로 가는 안내 문서로 교체 | 규칙 문장 중복 0 |
| 5 | 템플릿, 영역 CONTEXT, Vault 규칙 문서를 새 [스키마](../AI/Task_and_Record_Schema_agent.md#what-is-a-schema)와 경로로 갱신 | 옛 규칙 문장 0 |
| 6 | 승인된 확장 사양 내용을 운영로 바꾸고 새 DEC 기록 | 상태 표시와 결정 기록 일치 |
| 7 | [이전 절차](../Setup/Migration_admin.md#실행과-복구)에 따라 단계별 검증·commit. 실패하면 이후 사용자 변경을 보존하면서 승인된 변경분만 복구 | 새 깨진 링크 0, 복구 시험 통과 |

## 문서-작성-규칙

| 규칙 | 내용 |
|---|---|
| 파일 이름 | 공백 없는 영어 `Title_Case` + 주 독자 접미사 + 확장자. AI Agent가 주로 읽거나 기계가 읽는 파일은 `_agent`(`Common_Rules_agent.md`, `Context_Manifest_agent.json`), HQ·관리자가 읽는 설명 문서는 `_admin`(`Operating_Manual_admin.md`). 폴더 안내 문서 `README.md`와 `tools/`의 스크립트는 접미사를 붙이지 않음 |
| frontmatter | `type: agent-node-governance`, `layer`, `status`, `version`, `updated` 다섯 개만 |
| 첫 섹션 | `## overview` — 목적 1–3문장과 섹션 표 (섹션 링크 · 내용 · 적용 범위) |
| 마지막 섹션 | `_admin` 문서와 폴더 README는 `## 관련-문서`, `_agent` 문서는 `## related-documents`. 최상위 README만 관리자 검토 체크리스트를 마지막에 둠 |
| 언어 | `_agent` 문서는 영어(제목·앵커 포함), `_admin` 문서와 README는 한국어. 단 vault 문서에 그대로 들어가는 템플릿·기록 토큰(`# 기록`, 기록 단계, 검토 요청 블록 등)은 한국어로 둠. HQ에게 가는 보고는 한국어 ([기록 구조](../AI/Reporting_Style_agent.md#record-structure)) |
| 길이 | 문서당 250줄 이하 목표 |
| 문단 | 3문장 이하. 병렬 항목이 3개 이상이면 표 |
| 다이어그램 | Mermaid만 사용 |
| 적용 대상 | Architecture·HQ·AI·Setup의 설명 문서와 최상위 README. 템플릿 코드 블록·작업 기록·스크립트·설정에는 설명 문서의 제목·frontmatter 규칙을 적용하지 않음 |
| 쓰지 않는 문법 | 특정 편집기에서만 동작하는 문법 (위키 링크 `[[ ]]`, 임베드, `%%` 주석, `==` 강조) |
| 인스턴스 값 | 본문에 복사하지 않고 `{이름}` 형태로 [회사 프로필](../Architecture/Company_Profile_admin.md) 섹션에 링크 |
| 조항 번호 | 역할 조항은 `역할 약자-묶음 번호 1자리 + 순번 2자리` (예: `CO-101`). 번호는 재사용하지 않고, 없앤 조항은 `폐지`로 남김 |

새 문서는 아래 틀에서 시작합니다.

```markdown
---
type: agent-node-governance
layer: architecture
status: active
version: 1.6.1
updated: YYYY-MM-DD
---

# 문서-제목

## overview

이 문서의 목적 한두 문장.

| 섹션 | 내용 | 상태 | 근거 |
|---|---|---|---|
| [첫-섹션](#첫-섹션) | 한 줄 요약 | 운영 | DEC-XX-001 |
| [관련-문서](#관련-문서) | 함께 볼 문서 | — | — |

## 첫-섹션

## 관련-문서
```

## 제목과-앵커

GitHub는 제목에서 앵커를 만들 때 영문을 소문자로 바꾸고, 문장부호를 지우고, 공백을 `-`로 바꿉니다. Obsidian은 제목 문자열을 그대로 앵커로 씁니다. **제목을 처음부터 앵커 모양으로 쓰면** 두 곳에서 같은 링크가 동작합니다.

| 규칙 | 좋은 예 | 나쁜 예 | 이유 |
|---|---|---|---|
| 공백 대신 `-` | `## 결정-요청-형식` | `## 결정 요청 형식` | 공백은 링크에서 `%20`이 필요 |
| 영문은 소문자 | `## hq-결정-요청` | `## HQ-결정-요청` | GitHub 앵커는 `hq-결정-요청`이 됨 |
| 문장부호 없음 | `## 종료-취소-보류` | `## 종료·취소·보류` | GitHub가 `·`를 지워 앵커가 달라짐 |
| 번호 없음 | `## 작업-상태` | `## 3-작업-상태` | 순서를 바꾸면 앵커도 바뀜 |
| 문서 안 중복 없음 | `## 계획-금지`, `## 실행-금지` | 같은 문서에 `## 금지` 두 번 | GitHub가 두 번째 앵커에 `-1`을 붙임 |

- **허용 문자:** 한글, 영문 소문자, 숫자, `-`. 정규식 `^[0-9a-z가-힣]+(-[0-9a-z가-힣]+)*$`.

- **적용 범위:** H1부터 모든 수준의 제목에 적용합니다.

## 링크와-연결

문서는 위키피디아처럼 서로 연결합니다. 독자는 모르는 개념을 만났을 때 링크 한 번으로 정의에 도착해야 합니다.

| 규칙 | 내용 | 예 |
|---|---|---|
| `.md` 파일로 바로 링크 | 문서 사이 링크는 상대 경로 Markdown 링크 | `[실행 모드](../Architecture/Risk_and_Authority_admin.md#실행-모드)` |
| 가장 가까운 섹션 | 문서 전체보다 해당 섹션 앵커로 링크 | `#실행-모드` |
| 정의 위치 1곳 | 용어마다 정의 섹션이 하나이며 [용어집](../Architecture/Glossary_admin.md)의 `정의` 열에 있음 | — |
| 문서별 첫 언급 | 정의된 용어나 다른 문서의 규칙을 그 문서에서 처음 쓸 때 반드시 링크 | — |
| 섹션별 재링크 | 긴 문서에서는 주요 섹션마다 한 번 더 링크할 수 있음. 같은 섹션 안의 반복은 링크하지 않음 | — |
| 뜻 있는 단어에 링크 | "여기", "이 문서" 대신 개념 이름에 링크 | `[승인](Commands_and_Approval_admin.md#승인과-실행-지시)` |
| 관련 문서 | 문서 끝에 상위·하위·같은 수준 문서를 나열 | `## 관련-문서` |
| 고아 문서 금지 | 폴더 안내 문서 외에 다른 문서 1개 이상에서 링크됨 | — |
| 인스턴스 값 | `{이름}`을 회사 프로필의 섹션에 링크 | [`{trash}`](../Architecture/Company_Profile_admin.md#작업-공간-경로) |
| 프로토콜 밖 파일 | 본문에서 링크하지 않고 [근거 자료](../Architecture/Company_Profile_admin.md#근거-자료)에 경로로만 둠 | — |

프로토콜 밖 파일을 본문에서 링크하지 않기 때문에, AGENT_NODE_GOVERNANCE 폴더를 떼어 다른 저장소로 옮겨도 본문 링크가 깨지지 않습니다.

## 상태-표시-규칙

| 구분 | 표시·운영 방법 |
|---|---|
| 공통 운영 매뉴얼 | frontmatter active, overview 적용 열에 운영 매뉴얼 |
| 확장 모드 사양 | frontmatter specification, 해당 절차는 런타임 구현·시험·활성화 후 적용 |
| 회사별 채택 | 로컬 채택 기록의 draft·approved·active와 고정 commit |
| 변경 제안 | TaskNote에 초안과 선택지를 기록. 기존 규칙을 몰래 바꾸지 않음 |
| 과거 이력 | Git과 실제 DEC로 보존. 참고 분석은 작성 시점과 운영 효력 없음을 표시 |

관리자 매뉴얼은 현재 절차를 설명합니다. 옛 제안서 질문 번호를 알아야만 실행할 수 있는 규칙을 만들지 않습니다. 실제 운영 버전과 새 변경 초안을 구분합니다.

## 기여-방법

| 순서 | 할 일 |
|---:|---|
| 1 | [독자별 읽는 순서](../README.md#독자별-읽는-순서)의 기여자 경로를 읽음 |
| 2 | 바꿀 곳을 문서와 섹션 앵커로 특정 |
| 3 | 변경을 제안. 작업 공간 안에서는 TaskNote 결정표, 공개 저장소에서는 이슈나 풀 리퀘스트 설명에 같은 결정표 |
| 4 | 아래 자가 검사를 통과 |
| 5 | HQ 승인 뒤 [변경 절차](#변경-절차)대로 반영 |

제출 전 자가 검사는 다음과 같습니다.

- [ ] 모든 제목이 [제목과 앵커](#제목과-앵커) 규칙을 따름

- [ ] overview 표가 모든 H2 섹션을 링크하고 적용 범위가 있음

- [ ] 새 용어를 [용어집](../Architecture/Glossary_admin.md)에 추가하고, 문서별 첫 언급을 정의 섹션에 링크

- [ ] 인스턴스 값을 본문에 복사하지 않고 회사 프로필에 링크

- [ ] 깨진 링크 0, Mermaid 렌더링 확인

## 다른-기업에-도입하기

| 단계 | 할 일 | 참고 |
|---:|---|---|
| 1 | 적합성 확인 | [이 모델이 맞지 않는 경우](../Architecture/Operating_Model_admin.md#이-모델이-맞지-않는-경우) |
| 2 | [설치 안내](../Setup/README.md#새-기업-시작)에 따라 프로토콜 저장소를 독립 복제 | 회사 자료와 프로토콜 이력 분리 |
| 3 | [프로필 템플릿](../Setup/Templates_agent.md#company-profile)으로 로컬 프로필 작성 | 기존 회사의 경로·승인·기밀 목록을 상속하지 않음 |
| 4 | 쓰는 도구를 작업 공간 계층에 대응 | [도구 요구 조건](../Architecture/Workspace_and_Tools_admin.md#도구-요구-조건) |
| 5 | 위험도 예시와 기밀 영역을 다시 정의 | [위험도](../Architecture/Risk_and_Authority_admin.md#위험도), [기밀 영역](../Architecture/Company_Profile_admin.md#기밀-영역) |
| 6 | 역할 채택 범위 결정: 과정 역할 전체, 또는 단일 Agent로 시작 | [과정 역할](../Architecture/Organization_admin.md#과정-역할) |
| 7 | 가상 작업으로 시험: 정상, 평가 반려, 승인 대기, 중단 후 재개, 실패 경로 | [작업 흐름](../AI/Workflow_agent.md#loop-at-a-glance) |
| 8 | 상위 프로토콜 버전은 유지하고 회사 채택 버전을 별도로 시작 | [채택과 버전 고정](../Setup/Adoption_admin.md#버전-구분) |

## 관련-문서

- [HQ 안내](README.md) — HQ 문서 목록
- [명령과 승인](Commands_and_Approval_admin.md) — 변경 제안을 승인하는 방법
- [회사 프로필](../Architecture/Company_Profile_admin.md) — 도입할 때 바꾸는 문서
- [용어집](../Architecture/Glossary_admin.md) — 정의 위치 목록
- [설치 안내](../Setup/README.md) — 새 회사의 초기 파일과 도입 순서
- [채택 기록](../Setup/Adoption_admin.md) — 검토와 운영 활성화의 구분
