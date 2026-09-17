"""Report frontmatter that does not follow Architecture/Frontmatter_agent.json.

Read-only: it never edits a file. Company values come from a local JSON file
(for example NODE_PROFILE/Frontmatter_Local_agent.json). Only the frontmatter
block is read, and paths listed in the local ``exclude`` are skipped.
Python 3.10+, standard library only.
"""
from pathlib import Path
from collections import Counter
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'Architecture/Frontmatter_agent.json'
PLACEHOLDER = re.compile(r'\{([a-z-]+)\}')


def glob_regex(pattern):
    out = re.escape(pattern).replace(r'\*\*/', '(?:.*/)?').replace(r'\*\*', '.*').replace(r'\*', '[^/]*')
    return re.compile('^' + out + '$')


def parse(text):
    """Parse the YAML subset used in frontmatter.

    Returns (fields, order, problems). Each field is (style, value) where style is
    scalar, empty, block, inline or nested. None means there is no frontmatter.
    """
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---', 4)
    if end < 0:
        return None
    fields, order, problems, key = {}, [], [], None
    for line in text[4:end].split('\n'):
        if not line.strip():
            continue
        m = re.match(r'^([A-Za-z_][\w-]*):(?:\s(.*))?$', line)
        if m:
            key, raw = m.group(1), (m.group(2) or '').strip()
            if key in fields:
                problems.append(('duplicate-key', key))
            order.append(key)
            if unquote(raw) == '':
                fields[key] = ('empty', None)
            elif raw.startswith('[') and raw.endswith(']'):
                items = [unquote(x) for x in raw[1:-1].split(',') if x.strip()]
                fields[key] = ('inline', items)
            else:
                fields[key] = ('scalar', unquote(raw))
            continue
        item = re.match(r'^\s+-\s?(.*)$', line)
        if key and item and fields[key][0] in ('empty', 'block'):
            items = fields[key][1] if fields[key][0] == 'block' else []
            fields[key] = ('block', items + [unquote(item.group(1).strip())])
        elif key and line.startswith((' ', '\t')):
            fields[key] = ('nested', None)
        else:
            problems.append(('broken-line', line.strip()[:40]))
    return fields, order, problems


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
        return value[1:-1]
    return value


class Checker:
    def __init__(self, schema, local):
        self.schema = schema
        self.values = {k: v.get('default') for k, v in schema['placeholders'].items()}
        self.values.update((local or {}).get('values', {}))
        self.exclude = [glob_regex(p) for p in (local or {}).get('exclude', [])]

    def one(self, name):
        """A placeholder as a single string: a string value or a one-key table."""
        value = self.values.get(name)
        if isinstance(value, dict) and len(value) == 1:
            return next(iter(value))
        return value if isinstance(value, str) else None

    def fill(self, text):
        """Replace {name} with its single local value; None if unresolved."""
        if any(self.one(n) is None for n in PLACEHOLDER.findall(text)):
            return None
        return PLACEHOLDER.sub(lambda m: self.one(m.group(1)), text)

    def kind_of(self, rel, fields):
        tags = self.items(fields.get('tags'))
        type_value = self.scalar(fields.get('type'))
        for name, kind in self.schema['kinds'].items():
            match = kind['match']
            if 'under' in match:
                under = self.fill(match['under'])
                if under is None or not rel.startswith(under.rstrip('/') + '/'):
                    continue
            if any(rel.startswith((self.fill(x) or '\0') + '/') for x in match.get('exclude_under', [])):
                continue
            if 'filename' in match and rel.rsplit('/', 1)[-1] != match['filename']:
                continue
            if 'depth_max' in match and rel.count('/') > match['depth_max']:
                continue
            if 'tag' in match and match['tag'] not in tags:
                continue
            if 'type_value' in match and type_value not in match['type_value']:
                continue
            if 'has_key' in match and match['has_key'] not in fields:
                continue
            return name
        return None

    @staticmethod
    def items(field):
        if not field:
            return []
        style, value = field
        return value if style in ('block', 'inline') else ([value] if style == 'scalar' else [])

    @staticmethod
    def scalar(field):
        return field[1] if field and field[0] == 'scalar' else None

    def allowed(self, spec):
        if 'values_from' in spec:
            values = self.values.get(spec['values_from'])
            return None if values is None else set(values)
        allowed = set()
        for key in spec.get('values', {}):
            names = PLACEHOLDER.findall(key)
            if not names:
                allowed.add(key)
            elif isinstance(self.values.get(names[0]), dict):
                allowed.update(self.values[names[0]])
            elif isinstance(self.values.get(names[0]), str):
                allowed.add(self.values[names[0]])
            else:
                return None
        return allowed

    def check_value(self, name, spec, value, out):
        kind = spec['type']
        if kind == 'enum':
            allowed = self.allowed(spec)
            if allowed is not None and value not in allowed:
                legacy = spec.get('legacy_values', {})
                out.append(('legacy-value' if value in legacy else 'bad-enum', f'{name}: {value}'))
            return
        if kind in self.schema['types'] and 'pattern' in self.schema['types'][kind]:
            if not re.match(self.schema['types'][kind]['pattern'], value):
                out.append(('bad-format', f'{name}: {value} ({kind})'))
                return
        pattern = spec.get('pattern') or (self.values.get(spec['pattern_from']) if 'pattern_from' in spec else None)
        if pattern and not re.match(pattern, value):
            out.append(('bad-format', f'{name}: {value}'))
        if 'range_from' in spec and isinstance(self.values.get(spec['range_from']), dict):
            bounds = self.values[spec['range_from']]
            if re.match(r'^-?[0-9]+$', value) and not bounds['min'] <= int(value) <= bounds['max']:
                out.append(('out-of-range', f'{name}: {value}'))
        if kind == 'text' and ('[[' in value or '**' in value):
            out.append(('text-not-plain', name))

    def check_file(self, rel, text):
        parsed = parse(text)
        if parsed is None:
            name = self.kind_of(rel, {})
            if name is None or any(rel.endswith(x) for x in self.schema['no_frontmatter']):
                return None, []
            return name, [('no-frontmatter', '')]
        fields, order, out = parsed
        name = self.kind_of(rel, fields)
        if name is None:
            return None, []
        kind = self.schema['kinds'][name]
        tags = self.items(fields.get('tags'))
        variant = 'ai' if 'ai' in tags else 'human'
        specs = kind['fields']
        known = set(specs) | set(kind.get('plugin_managed', []))
        for key, (style, value) in fields.items():
            if key in kind.get('deprecated', {}):
                out.append(('deprecated-key', f'{key} → {kind["deprecated"][key]}'))
                continue
            if key not in known:
                out.append(('unknown-key', key))
                continue
            if key not in specs:
                continue
            spec = specs[key]
            if spec.get('variant_only') and spec['variant_only'] != variant and name == 'tasknote':
                out.append(('variant-key', f'{key} ({variant})'))
            if style == 'inline' and value:
                out.append(('inline-list', key))
            if spec['type'] == 'list':
                if style == 'scalar':
                    out.append(('not-a-list', key))
                    value = [value]
                elif style == 'empty':
                    value = []
                if not value and self.required(spec, variant):
                    out.append(('empty-required', key))
                item_spec = dict(spec, type=spec['item_type'])
                for item in value or []:
                    found = []
                    self.check_value(key, item_spec, item, found)
                    out.extend(x for x in found if x[0] != 'text-not-plain')
                continue
            if style == 'empty':
                if not spec.get('allow_empty') and self.required(spec, variant):
                    out.append(('empty-required', key))
                continue
            if style != 'scalar':
                out.append(('not-a-scalar', key))
                continue
            self.check_value(key, spec, value, out)
        for key, spec in specs.items():
            if key not in fields and self.required(spec, variant):
                out.append(('missing-required', key))
            elif key not in fields and not spec['required'] and not (
                    name == 'tasknote' and spec.get('variant_only', variant) != variant):
                out.append(('missing-optional', key))
            for member in spec.get('must_include', {}).get(variant, []):
                if key in fields and member not in self.items(fields[key]):
                    out.append(('missing-tag', member))
        expected = [k for k in kind['order'] if k in fields]
        if [k for k in order if k in kind['order']] != expected:
            out.append(('key-order', ''))
        title = self.scalar(fields.get('title'))
        if name == 'tasknote' and title is not None and title != Path(rel).stem:
            out.append(('title-mismatch', title))
        if name == 'tasknote' and variant in kind.get('state_combinations_apply_to', 'ai'):
            keys = kind.get('state_combination_fields', ('status', 'owner', 'hq_todo'))
            combo = [self.scalar(fields.get(k)) for k in keys]
            allowed = [[self.fill(x) for x in c] for c in kind['state_combinations']]
            if None not in combo and not any(None in c for c in allowed) and combo not in allowed:
                out.append(('bad-state', '/'.join(combo)))
        return name, out

    @staticmethod
    def required(spec, variant):
        return 'all' in spec['required'] or variant in spec['required']

    def run(self, root, paths=None):
        root = Path(root).resolve()
        files = [Path(p).resolve() for p in paths] if paths else sorted(root.rglob('*.md'))
        report = []
        for path in files:
            rel = path.relative_to(root).as_posix()
            if any(rx.match(rel) for rx in self.exclude):
                continue
            head = path.read_text(encoding='utf-8-sig', errors='replace')[:20000]
            name, problems = self.check_file(rel, head)
            if name is None and not paths:
                continue
            report.append((rel, name, problems))
        return report


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, help='vault root')
    parser.add_argument('--local', help='company values JSON (e.g. NODE_PROFILE/Frontmatter_Local_agent.json)')
    parser.add_argument('--list', action='store_true', help='print every problem, not only the summary')
    parser.add_argument('paths', nargs='*', help='check only these files')
    args = parser.parse_args()
    checker = Checker(load(SCHEMA), load(args.local) if args.local else None)
    report = checker.run(args.root, args.paths)
    by_kind, by_code = Counter(), Counter()
    failing = 0
    for rel, name, problems in report:
        by_kind[name or '(unmatched)'] += 1
        failing += bool(problems)
        for code, _ in problems:
            by_code[code] += 1
        if problems and (args.list or args.paths):
            print(f'{rel} [{name}]')
            for code, detail in problems:
                print(f'  {code} {detail}'.rstrip())
    print(f'SUMMARY: {len(report)} files checked, {failing} with problems (schema status: {checker.schema["status"]})')
    print('  kinds: ' + ', '.join(f'{k} {v}' for k, v in sorted(by_kind.items())))
    print('  problems: ' + (', '.join(f'{k} {v}' for k, v in by_code.most_common()) or 'none'))
    print('Report only. No file was changed.')
    return 1 if failing else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
