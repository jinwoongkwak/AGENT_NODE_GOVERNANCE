---
type: agent-node-governance
layer: setup
status: active
version: 1.6.0
updated: 2026-09-23
---

# ai-company-bootstrap-guide

## overview

Given to an AI as starting context, this document lets it found a company with the same operating structure. It never copies an existing company's approvals, confidentiality policy, or project content; it builds the profile from the new company's goals and actual materials.

| Section | Content | Applies |
|---|---|---|
| [input-contract](#input-contract) | Inputs needed for founding | Operating manual |
| [request-to-the-ai](#request-to-the-ai) | Instruction HQ copies and fills in | Operating manual |
| [bootstrap-order](#bootstrap-order) | Read, generate, place materials, verify | Operating manual |
| [generation-tools](#generation-tools) | Dry-run and actual generation | Operating manual |
| [acceptance-and-handoff](#acceptance-and-handoff) | Conditions for starting operation | Operating manual |
| [related-documents](#related-documents) | Detailed criteria | Operating manual |

## input-contract

| Input | Required content | If missing |
|---|---|---|
| Company | Name, research question, HQ and owner values | Prepare only a draft file structure |
| Destination | A new empty folder or an existing workspace | Never overwrite an existing folder with a new install |
| Projects | ID, title, internal research or external collaboration | Leave empty; never invent projects |
| Materials | Allowed read paths, owner, source, confidentiality grade | Never open unconfirmed sources or send them externally |
| Environment | Editor, Git, backup, execution devices, tools | Confirm in the actual installed environment |
| Execution scope | Which of create, edit, copy, move, remote deploy are allowed | Do only the allowed preparation |

AI never guesses research success criteria or authority a person has not yet decided and records them as approved. Ordinary folder and file names may use this manual's defaults.

## request-to-the-ai

HQ copies the block below (in Korean), fills in the placeholders, and gives it to the AI.

```text
이 AGENT_NODE_GOVERNANCE을 읽고 새 1인 연구 회사를 설립해줘.

회사 이름: <이름>
연구 목표: <질문과 원하는 결과>
관리자 이름 / owner: <이름> / <slug>
새 작업 공간: <절대 경로>
프로젝트: <ID, 제목, 자체 연구/외부 협업>
기존 자료: <허용된 경로와 소유자, 없으면 없음>
기밀·제한 범위: <경로와 허용 처리 환경>
허용한 작업: <빈 구조 생성, 분류 계획, 실제 복사/이동, Git 배포 등>

먼저 README → HQ/Operating_Manual → Architecture/Workspace_Layout →
Setup/AI_Bootstrap → Setup/Material_Placement를 읽어.
기본 모드로 시작하고 원본 자료를 보존해.
회사 프로필과 채택 기록을 별도로 만들고, 실제 권한·백업·검증 근거를 남겨.
설립 뒤 관리자가 어디서 상태를 보고 지시·승인·중단하는지 안내해.
```

## bootstrap-order

1. Fix the input contract and protocol version. Write the generation scope, material access scope, and completion criteria in the company TaskNote.
2. Build a file generation list matching the [workspace layout](../Architecture/Workspace_Layout_admin.md#최소-구조). For an existing workspace, use the [migration procedure](Migration_admin.md).
3. Create a new empty workspace and generate the profile, entry files, CONTEXT, project canonical documents, task templates, and HQ action views.
4. Classify each input into a per-file mapping table following the [material placement criteria](Material_Placement_agent.md). Never move originals, Git repos, or confidential material the same way as ordinary documents.
5. Execute only file placements within the allowed scope. Leave unknown material in place or in INBOX, with the question and reason recorded.
6. Pass the protocol check, structure check, synthetic task run, and recovery verification, then activate the adoption record on HQ's actual approval.

## generation-tools

Replace the values in the [example config](company.example_agent.json) with the new company's, then use the commands below. They take only company name, people, and projects; approvals and confidentiality policy are never inherited from the example.

```sh
python tools/bootstrap.py --config my-company.json --dest /absolute/new-workspace
python tools/bootstrap.py --config my-company.json --dest /absolute/new-workspace --apply
python tools/check_workspace.py /absolute/new-workspace
```

The first command only prints the generation list. `--apply` writes only to a new or empty folder and refuses if files exist. The target also receives copies of the protocol documents and tools, so it stays readable without access to the original repository.

The generator never moves existing material, initializes Git, installs plugins, or sends anything over the network. If using Git, review the target structure and visibility, then initialize a company repository; the protocol copy can be converted to a submodule pinned to a fixed commit. When doing so, keep the original copy and confirm the versions are identical.

Unconfirmed or unapproved confidential paths remain so after generation. Running the generator grants no operating authority.

## acceptance-and-handoff

| Criterion | How to confirm |
|---|---|
| Company values agree | Compare company.json, profile, entry files, adoption record |
| Each material has one canonical location | Check mapping table, before/after hashes, indexes |
| Work flows end to end | Run a synthetic TaskNote through request → authority → execution → verification → closure |
| Unapproved actions do not run | Unapproved risk-level-2 work stays in planning state |
| The admin can control it | Point to the operating home, HQ action view, STATUS, Decisions paths |
| Recoverable | Restore sample files from backup and compare hashes |

## related-documents

- [Material placement criteria](Material_Placement_agent.md) — deciding where inputs go
- [Initial templates](Templates_agent.md) — manual generation alternative
- [Admin operating manual](../HQ/Operating_Manual_admin.md) — operation after founding
- [Company profile](../Architecture/Company_Profile_admin.md) — local settings contract
