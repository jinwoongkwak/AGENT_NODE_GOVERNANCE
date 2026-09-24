"""Read-only checks for the protocol package; no third-party dependencies."""
from pathlib import Path
from collections import Counter
import json
import re
import sys
from urllib.parse import unquote

import build_entry

ROOT = Path(__file__).resolve().parents[1]
ENTRY_MAX_BYTES = 20000
ENTRY_MAX_LINES = 250
NAVIGATION = ['README.md', 'AI/README.md']
ERRORS = []


def require(condition, message):
    if not condition:
        ERRORS.append(message)


def prose(text):
    """Ignore examples in fenced and inline code when resolving links."""
    text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    return re.sub(r'`[^`\n]*`', '', text)


def main():
    ERRORS.clear()
    docs = sorted(ROOT.rglob('*.md'), key=lambda p: p.relative_to(ROOT).as_posix())
    docs = [p for p in docs if not any(x.startswith('.') for x in p.relative_to(ROOT).parts)]
    sources = {p: p.read_text(encoding='utf-8-sig') for p in docs}
    headings = {}
    incoming = Counter()
    link_count = 0
    for p, text in sources.items():
        label = p.relative_to(ROOT).as_posix()
        body = prose(text)
        hs = re.findall(r'^#{1,6} (.+)$', body, re.M)
        headings[p] = set(hs)
        require(len(hs) == len(set(hs)), f'{label}: duplicate heading')
        for h in hs:
            require(re.fullmatch(r'[0-9a-z가-힣]+(?:-[0-9a-z가-힣]+)*', h), f'{label}: heading {h}')
        require(not re.search(r'^(?:<{7}|={7}|>{7})(?:\s|$)', text, re.M), f'{label}: conflict marker')
        require(text.startswith('---\n'), f'{label}: missing frontmatter')
        front = text.split('---', 2)[1] if text.startswith('---') else ''
        for field in ['type', 'layer', 'status', 'version', 'updated']:
            require(re.search(rf'^{field}: .+', front, re.M), f'{label}: missing {field}')
        version = '0.2.0' if label == 'AI_Agent_Company_Comparison_admin.md' else '1.6.0'
        require(f'version: {version}' in front, f'{label}: release version mismatch')
        h2 = re.findall(r'^## (.+)$', body, re.M)
        require(h2 and h2[0] == 'overview', f'{label}: overview must be first')
        if p == ROOT / 'README.md':
            last = '관리자-검토-체크리스트'
        else:
            last = 'related-documents' if p.stem.endswith('_agent') else '관련-문서'
        require(h2 and h2[-1] == last, f'{label}: unexpected final section')
        overview = body.split('## overview', 1)[-1].split('\n## ', 1)[0]
        for h in h2[1:]:
            require(f'](#{h})' in overview, f'{label}: overview missing {h}')

    for p, text in sources.items():
        for target in re.findall(r'\]\(([^)]+)\)', prose(text)):
            if re.match(r'^[a-z]+://', target):
                continue
            target = unquote(target.strip('<>'))
            rel, _, anchor = target.partition('#')
            dest = build_entry.resolve_link(p, rel)
            require(dest.is_relative_to(ROOT), f'{p.name}: link outside package {target}')
            require(dest.is_file(), f'{p.name}: missing file {target}')
            if anchor and dest in headings:
                require(anchor in headings[dest], f'{p.name}: missing anchor {target}')
            if dest != p:
                incoming[dest] += 1
            link_count += 1
    for p in docs:
        require(incoming[p] > 0, f'{p.name}: orphan document')

    schema_text = sources[ROOT / 'AI/Task_and_Record_Schema_agent.md']
    blocks = re.findall(r'```json\n(.*?)\n```', schema_text, re.S)
    require(len(blocks) == 1, 'schema: expected exactly one JSON block')
    schema = json.loads(blocks[0])
    kinds = schema['record']['kinds']
    rows = {}
    for line in schema_text.splitlines():
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) == 5 and cells[0].strip('`') in kinds:
            rows[cells[0].strip('`')] = cells
    require(set(rows) == set(kinds), 'schema: kind table and JSON disagree')
    for kind, fields in kinds.items():
        require(fields['writer'] in {'coordinator', 'planner', 'evaluator', 'executor'}, f'{kind}: writer')
        for ref in fields['responds_to']:
            require(ref in kinds, f'{kind}: unknown reference {ref}')
        for section in fields['sections']:
            require(section in rows[kind][3], f'{kind}: section table mismatch {section}')
        for verdict in fields.get('verdict', []):
            require(f'`{verdict}`' in schema_text, f'{kind}: verdict absent from prose')
    for pattern in schema['task']['patterns'].values():
        re.compile(pattern)
    re.compile(schema['record']['filename'])
    require(len(schema['task']['state_combinations']) == 6, 'schema: state combinations')
    require(re.fullmatch(schema['task']['patterns']['approved_version'], '') is not None, 'schema: unapproved value')

    frontmatter = json.loads((ROOT / 'Architecture/Frontmatter_agent.json').read_text(encoding='utf-8'))
    for name, kind in frontmatter['kinds'].items():
        require(set(kind['order']) <= set(kind['fields']), f'frontmatter: {name} order has unknown fields')
        for field, spec in kind['fields'].items():
            require(spec['type'] in frontmatter['types'], f'frontmatter: {name}.{field} unknown type')

    entry_text, manifest_text = build_entry.render()
    for path, generated in [(build_entry.ENTRY, entry_text), (build_entry.MANIFEST, manifest_text)]:
        name = path.relative_to(ROOT).as_posix()
        current = path.read_text(encoding='utf-8') if path.is_file() else None
        require(current == generated, f'{name}: stale, run python tools/build_entry.py')
    entry_bytes = len(entry_text.encode('utf-8'))
    require(entry_bytes <= ENTRY_MAX_BYTES,
            f'Agent_Entry_agent.md: {entry_bytes} bytes over the {ENTRY_MAX_BYTES} budget')
    require(entry_text.count('\n') + 1 <= ENTRY_MAX_LINES, 'Agent_Entry_agent.md: over the line budget')

    extended = {p.relative_to(ROOT).as_posix() for p, text in sources.items()
                if 'status: specification' in text.split('---', 2)[1]}
    for label in NAVIGATION:
        page = ROOT / label
        for line in prose(sources[page]).splitlines():
            if not line.startswith('|') or '확장' in line:
                continue
            for target in re.findall(r'\]\(([^)]+)\)', line):
                dest = build_entry.resolve_link(page, unquote(target).split('#')[0])
                if dest.is_relative_to(ROOT) and dest.relative_to(ROOT).as_posix() in extended:
                    require(False, f'{label}: table row links {target} without a 확장 사양 marker')

    readme = sources[ROOT / 'README.md']
    review = readme.split('## 관리자-검토-체크리스트\n', 1)[-1]
    items = re.findall(r'^- \[[ x]\] \*\*(C\d+) ', review, re.M)
    require(items == [f'C{i}' for i in range(1, 11)], 'README: expected C1-C10 once in order')
    clauses = []
    for p, text in sources.items():
        clauses.extend(re.findall(r'^- \*\*((?:CO|PL|EV|EX)-\d{3}) ', prose(text), re.M))
    require(len(clauses) == len(set(clauses)), 'duplicate role clause ID')

    if ERRORS:
        print('\n'.join(f'ERROR {e}' for e in ERRORS))
        return 1
    print(f'PASS: {len(docs)} documents; {link_count} internal links; {len(kinds)} record kinds; '
          f'{len(clauses)} role clauses; C1-C10; entry {entry_bytes}B; release 1.6.0')
    print('Not checked: Obsidian UI, Mermaid rendering, Router runtime, HQ approval.')
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
