"""Create a NEW company workspace from explicit configuration. Default: dry-run.

Never migrates existing data, initializes Git, installs plugins, or grants approval.
Python 3.10+, standard library only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

PROTOCOL = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = '00_HQ/90_SYSTEM/AGENT_NODE_GOVERNANCE'
TASKS = '00_HQ/10_PLANNING/TaskNotes/Tasks/AI'
VERSION = '1.4.0'


def atom(value, label):
    if not isinstance(value, str) or not value.strip() or any(c in value for c in '\r\n\x00'):
        raise ValueError(f'{label}: nonempty single-line string required')
    if any(c in value for c in '|[]<>'):
        raise ValueError(f'{label}: Markdown control characters are not allowed')
    return value.strip()


def validate_config(c):
    if not isinstance(c, dict):
        raise ValueError('Configuration must be an object')
    allowed = {'company', 'hq_person', 'hq_owner', 'research_focus', 'projects'}
    if set(c) - allowed:
        raise ValueError('Unknown configuration keys: ' + ', '.join(sorted(set(c) - allowed)))
    for key in ['company', 'hq_person', 'hq_owner', 'research_focus']:
        atom(c.get(key), key)
    if not re.fullmatch(r'[a-z][a-z0-9_-]{0,31}', c['hq_owner']) or c['hq_owner'] in {'ai', 'none'}:
        raise ValueError('hq_owner must be a distinct lowercase slug')
    projects = c.get('projects', [])
    if not isinstance(projects, list):
        raise ValueError('projects must be a list')
    ids = set()
    for p in projects:
        if not isinstance(p, dict) or set(p) != {'id', 'title', 'kind'}:
            raise ValueError('Each project needs exactly id, title, kind')
        if not isinstance(p['id'], str) or not re.fullmatch(r'[A-Z][A-Z0-9_]{1,59}', p['id']):
            raise ValueError('Project id must be uppercase letters, digits or underscore')
        if p['id'] in ids:
            raise ValueError('Duplicate project id')
        ids.add(p['id'])
        atom(p['title'], 'project title')
        if p['kind'] not in {'research', 'collaboration'}:
            raise ValueError('Project kind must be research or collaboration')
    return c


def project_path(p):
    return '20_PROJECTS/' + ('COLLABORATIONS/' if p['kind'] == 'collaboration' else '') + p['id']


def task_template():
    return '''---
title: "<할 일>"
status: to-do
tags:
  - task
  - ai
projects: []
contexts: []
owner: ai
hq_todo: none
risk: 1
llm_model: "<이 TaskNote를 쓴 모델>"
proposal_version: V1.0.0
approved_version: ""
recommended_model: "<작업 난이도에 맞는 모델>"
execution_mode: autonomous
report_policy: final
write_scope: []
blockedBy: []
scheduled:
due:
completedDate:
timeEstimate:
dateCreated:
dateModified:
---

# 지시

목표·입력·산출물·범위·제외·완료 기준·검증 방법을 채웁니다.

# 현재 상태

단계·다음 행동·외부 대기 조건·권한 근거·백업·중단 조건.

# 결정 및 승인

실제 HQ 승인 원문·시각·버전·허용 행위만 기록합니다.

# 실행 계획

대상·작업·검증·복구 방법.

# 기록

결과·변경 파일·검증·미해결·다음 인계.
'''


def build(c, copy_protocol=True):
    c = validate_config(c)
    files = {}
    def put(path, value):
        files[path] = value.encode('utf-8')
    local = dict(c, protocol_version=VERSION, mode='basic', protocol_path=PROTOCOL_PATH,
                 task_folder=TASKS, templates='00_HQ/90_SYSTEM/AI_Control/Templates',
                 adoption='00_HQ/90_SYSTEM/Protocol_Adoption.md', ai_branch='ai/work',
                 confidential_paths=[], restricted_paths=[], deployment_status='draft')
    put('00_HQ/90_SYSTEM/company.json', json.dumps(local, ensure_ascii=False, indent=2)+'\n')
    entry = f'''# {c['company']} — Agent 진입점

1. `00_HQ/90_SYSTEM/Protocol_Adoption.md`의 활성화 상태·commit·모드를 확인합니다.
2. `00_HQ/90_SYSTEM/company.json`과 같은 폴더의 `Company_Profile.md`에서 경로·owner·기밀 범위를 확인합니다.
3. `{PROTOCOL_PATH}/AI/Agent_Entry_agent.md`를 읽습니다. 읽는 순서·위험도·실행 모드·상태 조합·금지 행위·기록 틀이 이 한 문서에 있습니다.
4. 해당 TaskNote와 작업 영역의 가장 가까운 `_AI/CONTEXT.md`, 그 CONTEXT가 지정한 정본을 읽습니다.
5. 그 밖의 프로토콜 문서는 Agent_Entry_agent.md의 작업 유형별 경로가 요구할 때만 엽니다. 전체 목록은 `{PROTOCOL_PATH}/AI/Context_Manifest_agent.json`이고, mode가 extended이거나 reference인 문서는 기본 운영에서 열지 않습니다.
6. 승인된 범위에서 백업·실행·검증·기록합니다. 기존 대화의 명시 권한은 다시 묻지 않습니다.
7. 기밀 원문은 명시 범위에서만 열고 외부 AI에 보내지 않습니다. 영구 삭제 금지, Git은 ai/work, main 병합은 HQ입니다.
8. draft 작업 공간은 설치·분류 계획만 준비합니다. 실제 운영은 HQ 승인·검증·채택 기록 후 활성화합니다.
'''
    put('AGENTS.md', entry)
    put('CLAUDE.md', entry)
    put('00_HQ/90_SYSTEM/Company_Profile.md', f'''# {c['company']} 회사 프로필

기계가 읽는 값은 [company.json](company.json)에 있습니다. 이 문서는 그 설정의 설명입니다.

| 항목 | 값 |
|---|---|
| 회사 | {c['company']} |
| HQ | {c['hq_person']} (`{c['hq_owner']}`) |
| 연구 분야 | {c['research_focus']} |
| 운영 모드 | basic |
| 프로토콜 | [{VERSION} 매뉴얼](AGENT_NODE_GOVERNANCE/README.md) |
| TaskNote | `{TASKS}/` |
| 기밀·제한 자료 | 도입 전에 HQ가 경로와 허용 처리 환경을 확인해야 함 |
| Git·백업·실행 기기 | 도입 시 실제 환경에서 지정·검증 |
| 자료 배치 | [배치 기준](AGENT_NODE_GOVERNANCE/Setup/Material_Placement_agent.md) |
''')
    put('00_HQ/90_SYSTEM/Protocol_Adoption.md', f'''# 프로토콜 채택 기록

| 항목 | 값 |
|---|---|
| 상태 | draft |
| 프로토콜 버전 | {VERSION} |
| 적용 commit | 설치 원본의 commit을 기록 |
| 회사 채택 버전 | V1.0.0 |
| 도입 모드 | basic |
| 승인자·시각·원문 | 미승인 |
| 기밀 경로 확인 | 미확인 |
| 백업·Git 확인 | 미확인 |
| 활성화 근거 | 미활성 |

생성 성공은 운영 승인이 아닙니다. 합성 작업 검증 후 HQ의 실제 승인으로 채웁니다.
''')
    put('00_HQ/README.md', f'''# {c['company']} 운영 홈

- [관리자 운영 매뉴얼](90_SYSTEM/AGENT_NODE_GOVERNANCE/HQ/Operating_Manual_admin.md)
- [프로젝트 현황](Project_Index.md)
- [HQ 결정](Decisions.md)
- [HQ 행동 보기](10_PLANNING/TaskNotes/Views/hq-actions.base)
- [회사 프로필](90_SYSTEM/Company_Profile.md)
- [채택 상태](90_SYSTEM/Protocol_Adoption.md)
''')
    put('00_HQ/Decisions.md', '# HQ Decisions\n\n실제 HQ 결정만 DEC-HQ-NNN으로 기록합니다.\n')
    index = '# Project Index\n\n각 프로젝트 STATUS가 정본입니다.\n\n| 프로젝트 | 상태 | 링크 |\n|---|---|---|\n'
    for p in c.get('projects', []):
        path = project_path(p)
        index += f'| {p["id"]}: {p["title"]} | 시작 전 | [STATUS](../{path}/STATUS.md) |\n'
        put(path+'/README.md', f'# {p["title"]}\n\n## 목적\n\nHQ가 연구 질문을 지정합니다.\n\n## Success criteria\n\n아직 확정되지 않았습니다.\n\n## 범위\n\nHQ 승인 범위를 기록합니다.\n')
        put(path+'/STATUS.md', '# 프로젝트 상태\n\n## Current state\n\n설립됨. 목표·기준 확인 전입니다.\n\n## This week\n\nHQ가 다음 결과를 정합니다.\n\n## Blockers\n\n성공 기준 미확정.\n\n## Next milestone\n\n첫 작업 계약.\n')
        put(path+'/10_NOTES/Decisions.md', '# Decisions\n\n실제 HQ 결정을 기록합니다.\n')
        put(path+'/30_SOURCE/Data_Index.md', '# Data Index\n\n원본 위치·dataset ID·버전·조건·접근 범위를 기록합니다. 원본을 덮어쓰지 않습니다.\n')
        put(path+'/30_SOURCE/Repositories.md', '# Repositories\n\nremote·경로·branch·commit·접근 조건을 기록합니다.\n')
        put(path+'/_AI/CONTEXT.md', f'# Project Context\n\n## 정본\n\n- `../README.md`\n- `../STATUS.md`\n- `../10_NOTES/Decisions.md`\n- `../30_SOURCE/Data_Index.md`\n- `../30_SOURCE/Repositories.md`\n\n## 범위\n\nTaskNote가 명시한 `{path}/` 하위만 수정합니다. 회사 기밀 정책을 따릅니다.\n')
    put('00_HQ/Project_Index.md', index)
    for folder, title in [('10_INBOX','미분류 자료'),('30_TECHNICAL_WIKI','재사용 절차'),('40_THEORY_WIKI','개념과 이론'),('90_ARCHIVE','종료 자료')]:
        put(folder+'/README.md', f'# {title}\n\n배치 기준은 [매뉴얼](../{PROTOCOL_PATH}/Setup/Material_Placement_agent.md)을 따릅니다.\n')
        put(folder+'/_AI/CONTEXT.md', f'# {title} Context\n\n정본은 `../README.md`와 개별 자료입니다. 작업 범위와 회사 기밀 정책을 확인합니다.\n')
    put('00_HQ/_AI/CONTEXT.md', '# HQ Context\n\n정본: `../Project_Index.md`, `../Decisions.md`, TaskNote. 판단 기준은 `../90_SYSTEM/AGENT_NODE_GOVERNANCE/AI/Agent_Entry_agent.md`, 회사 값은 `../90_SYSTEM/Company_Profile.md`.\n')
    put('20_PROJECTS/README.md', '# Projects\n\n[프로젝트 현황](../00_HQ/Project_Index.md)을 사용합니다.\n')
    put(TASKS+'/README.md', '# AI Tasks\n\n작업 하나당 TaskNote 하나. 템플릿은 `00_HQ/90_SYSTEM/AI_Control/Templates/AI_TASK.md`. 이 색인은 task가 아닙니다.\n')
    put('00_HQ/90_SYSTEM/AI_Control/Templates/AI_TASK.md', task_template())
    put('00_HQ/10_PLANNING/TaskNotes/Views/hq-actions.base', '''filters:
  and:
    - file.tags.contains("task")
    - file.tags.contains("ai")
    - '!file.path.contains("/Templates/")'
    - 'hq_todo == "decide" || hq_todo == "dispatch" || hq_todo == "review"'
views:
  - type: table
    name: HQ Actions
    order:
      - file.name
      - hq_todo
      - status
      - owner
      - projects
''')
    if copy_protocol:
        for p in sorted(PROTOCOL.rglob('*'), key=lambda p: p.relative_to(PROTOCOL).as_posix()):
            rel=p.relative_to(PROTOCOL)
            if p.is_file() and not any(x.startswith('.') or x in {'local','__pycache__'} for x in rel.parts[:-1]) and p.name != '.git':
                if p.suffix in {'.md','.py','.json'} or p.name in {'.gitignore','.gitattributes'}:
                    files[PROTOCOL_PATH+'/'+rel.as_posix()]=p.read_bytes()
    return files


def create(c, dest, apply=False):
    dest=Path(dest).absolute()
    if dest.is_symlink() or dest.resolve()!=dest:
        raise ValueError('Destination must not traverse a symlink or junction')
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise ValueError('Destination must be new or empty; existing workspace is never overwritten')
    files=build(c)
    for name in files:
        if not (dest/name).resolve().is_relative_to(dest):
            raise ValueError('Output escapes destination')
    manifest={p:hashlib.sha256(b).hexdigest() for p,b in files.items()}
    if apply:
        dest.mkdir(parents=True,exist_ok=True)
        for name,data in files.items():
            p=dest/name; p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f: f.write(data)
        manifest_path=dest/'00_HQ/90_SYSTEM/bootstrap-manifest.json'
        with manifest_path.open('x',encoding='utf-8') as f:
            json.dump(manifest,f,ensure_ascii=False,indent=2)
    return {'mode':'created' if apply else 'dry-run','destination':str(dest),'files':len(files),'paths':list(files)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',required=True)
    parser.add_argument('--dest',required=True)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    try:
        result=create(json.loads(Path(args.config).read_text(encoding='utf-8-sig')),args.dest,args.apply)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
