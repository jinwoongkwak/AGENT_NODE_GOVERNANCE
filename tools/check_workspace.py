"""Read-only structural check. It does not read confidential folders or credentials."""
from pathlib import Path
import argparse,json,sys


def check(root):
    root=Path(root).resolve()
    errors=[]
    required=['AGENTS.md','CLAUDE.md','00_HQ/README.md','00_HQ/Project_Index.md',
              '00_HQ/Decisions.md','00_HQ/90_SYSTEM/Company_Profile.md',
              '00_HQ/90_SYSTEM/Protocol_Adoption.md','00_HQ/90_SYSTEM/company.json']
    for name in required:
        if not (root/name).is_file(): errors.append('Missing '+name)
    if errors: return errors
    config=json.loads((root/'00_HQ/90_SYSTEM/company.json').read_text(encoding='utf-8-sig'))
    for key in ['company','hq_owner','protocol_path','task_folder','templates','mode']:
        if not config.get(key): errors.append('Missing config '+key)
    if config.get('mode')!='basic': errors.append('This checker supports basic mode only')
    for key in ['protocol_path','task_folder','templates']:
        name=config.get(key,'')
        path=(root/name).resolve()
        if not path.is_relative_to(root): errors.append('Path escapes workspace: '+key)
        elif not path.is_dir(): errors.append('Missing folder: '+name)
    for name in required:
        text=(root/name).read_text(encoding='utf-8-sig')
        if '<<<<<<< HEAD' in text or '\n>>>>>>> ' in text: errors.append('Conflict: '+name)
    for project in config.get('projects',[]):
        if 'path' in project:
            base=project['path']
        else:
            base='20_PROJECTS/'+('COLLABORATIONS/' if project.get('kind')=='collaboration' else '')+project['id']
        path=(root/base).resolve()
        if not path.is_relative_to(root): errors.append('Project escapes workspace'); continue
        for name in ['README.md','STATUS.md','_AI/CONTEXT.md']:
            if not (path/name).is_file(): errors.append('Missing project file: '+base+'/'+name)
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('workspace'); args=p.parse_args()
    try: errors=check(args.workspace)
    except (OSError,ValueError,KeyError,TypeError) as e: errors=[str(e)]
    if errors:
        print('\n'.join('ERROR '+e for e in errors)); return 1
    print('PASS: workspace structure and basic configuration. Approval, plugin UI and data correctness are not asserted.')
    return 0


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
