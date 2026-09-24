"""Generate the agent hot-path entry blocks and the context manifest.

The entry document never restates a rule in its own words: every block between
``<!-- generated:<file>#<anchor> -->`` and ``<!-- /generated -->`` is extracted
from the canonical section, so the definition stays in exactly one place.
Python 3.10+, standard library only.
"""
from pathlib import Path
import argparse
import json
import posixpath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / 'AI/Agent_Entry_agent.md'
MANIFEST = ROOT / 'AI/Context_Manifest_agent.json'
OPEN_MARK = re.compile(r'^<!-- generated:(\S+) -->$', re.M)
CLOSE_MARK = '<!-- /generated -->'
MODES = {'active': 'basic', 'specification': 'extended', 'draft': 'reference'}


def docs():
    return sorted((p for p in ROOT.rglob('*.md')
                   if not any(x.startswith('.') for x in p.relative_to(ROOT).parts)),
                  key=lambda p: p.relative_to(ROOT).as_posix())


def outside_fences(lines):
    """Yield (index, line) for lines that are not inside a fenced code block."""
    fence = None
    for i, line in enumerate(lines):
        mark = re.match(r'^(```+|~~~+)', line)
        if mark and fence is None:
            fence = mark.group(1)[0] * 3
            continue
        if mark and line.startswith(fence):
            fence = None
            continue
        if fence is None:
            yield i, line


def section(text, anchor):
    """Return (heading level, body) for one section, stopping at the next heading."""
    lines = text.splitlines()
    outside = dict(outside_fences(lines))
    start = level = None
    for i, line in outside.items():
        m = re.match(r'^(#{1,6}) (.+)$', line)
        if m and m.group(2) == anchor:
            start, level = i, len(m.group(1))
            break
    if start is None:
        raise KeyError(anchor)
    end = len(lines)
    for i, line in outside.items():
        if i > start and re.match(r'^#{1,6} ', line):
            end = i
            break
    return level, '\n'.join(lines[start + 1:end]).strip('\n')


def drop_mermaid(body):
    return re.sub(r'^```mermaid\n.*?^```\n?', '', body, flags=re.M | re.S).strip('\n')


def resolve_link(src, rel):
    """Resolve a link path from ``src``.

    Obsidian may rewrite links as vault paths that start with the package
    folder name (``AGENT_NODE_GOVERNANCE/Architecture/...``); those resolve
    from the package root. Everything else is relative to the source file.
    """
    if not rel:
        return src
    head, _, rest = rel.partition('/')
    if head == ROOT.name and rest:
        return (ROOT / rest).resolve()
    return (src.parent / rel).resolve()


def rewrite_links(body, src, dest):
    """Re-anchor relative links so they resolve from the destination document."""
    lines = body.splitlines()
    fenced = set(range(len(lines))) - {i for i, _ in outside_fences(lines)}

    def one(match):
        target = match.group(1)
        if re.match(r'^[a-z]+://', target):
            return match.group(0)
        rel, _, anchor = target.partition('#')
        source = resolve_link(src, rel)
        new = posixpath.relpath(source.as_posix(), dest.parent.as_posix())
        return f']({new}#{anchor})' if anchor else f']({new})'

    return '\n'.join(line if i in fenced else re.sub(r'\]\(([^)]+)\)', one, line)
                     for i, line in enumerate(lines))


def block(spec):
    """Render one generated block body from a '<path>#<anchor>' specification."""
    rel, _, anchor = spec.partition('#')
    src = ROOT / rel
    level, body = section(src.read_text(encoding='utf-8'), anchor)
    body = rewrite_links(drop_mermaid(body), src, ENTRY)
    heading = '#' * (level + 1) + ' ' + anchor
    origin = posixpath.relpath(rel, ENTRY.parent.relative_to(ROOT).as_posix())
    return f'{heading}\n\nCanonical: [{anchor}]({origin}#{anchor})\n\n{body}'


def build_entry(text):
    out, pos = [], 0
    for mark in OPEN_MARK.finditer(text):
        end = text.index(CLOSE_MARK, mark.end())
        out.append(text[pos:mark.end()])
        out.append('\n\n' + block(mark.group(1)) + '\n\n')
        pos = end
    out.append(text[pos:])
    return ''.join(out)


def overview_summary(text):
    """First sentence of the overview, used as the manifest's reading trigger."""
    body = text.split('## overview', 1)[-1].lstrip('\n')
    paragraph = body.split('\n\n', 1)[0].replace('\n', ' ').strip()
    paragraph = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', paragraph).replace('`', '')
    if paragraph.startswith('|'):
        return ''
    head = re.split(r'(?<=다\.)\s|(?<=[a-z)]\.)\s', paragraph, maxsplit=1)[0]
    return head if len(head) <= 70 else head[:67] + '...'


def build_manifest(entry_text):
    """Index every document so the agent can decide what not to open."""
    entries = []
    for p in docs():
        text = entry_text if p == ENTRY else p.read_text(encoding='utf-8')
        status = re.search(r'^status: (.+)$', text.split('---', 2)[1], re.M).group(1).strip()
        entries.append({
            'path': p.relative_to(ROOT).as_posix(),
            'status': status,
            'mode': MODES[status],
            'bytes': len(text.encode('utf-8')),
            'when_to_read': overview_summary(text),
        })
    totals = {'documents': len(entries), 'bytes': sum(e['bytes'] for e in entries)}
    for mode in sorted(MODES.values()):
        totals[mode] = sum(e['bytes'] for e in entries if e['mode'] == mode)
    version = re.search(r'^version: (.+)$', entry_text.split('---', 2)[1], re.M).group(1).strip()
    return {
        'schema': 1,
        'protocol_version': version,
        'entry': ENTRY.relative_to(ROOT).as_posix(),
        'note': 'Only mode basic documents apply to basic operation. Open extended and reference '
                'documents only when the paths by task type in Agent_Entry_agent.md require them.',
        'totals': totals,
        'documents': entries,
    }


def render():
    entry = build_entry(ENTRY.read_text(encoding='utf-8'))
    manifest = json.dumps(build_manifest(entry), ensure_ascii=False, indent=1) + '\n'
    return entry, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='report drift without writing')
    args = parser.parse_args()
    entry, manifest = render()
    stale = [str(p.relative_to(ROOT)) for p, new in [(ENTRY, entry), (MANIFEST, manifest)]
             if not p.is_file() or p.read_text(encoding='utf-8') != new]
    if args.check:
        if stale:
            print('STALE ' + ', '.join(stale) + ' — run python tools/build_entry.py')
            return 1
        print('PASS: entry blocks and manifest match the canonical sections')
        return 0
    ENTRY.write_text(entry, encoding='utf-8', newline='\n')
    MANIFEST.write_text(manifest, encoding='utf-8', newline='\n')
    print(f'wrote {ENTRY.relative_to(ROOT)} ({len(entry.encode())} bytes) '
          f'and {MANIFEST.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
