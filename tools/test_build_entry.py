"""Behavior checks for the generated entry document and context manifest."""
from pathlib import Path
import json
import re
import unittest

import build_entry


class SectionTests(unittest.TestCase):
    def test_stops_at_the_next_heading(self):
        text = '## a\n\nkeep\n\n### a-확장\n\ndrop\n\n## b\n\ndrop\n'
        level, body = build_entry.section(text, 'a')
        self.assertEqual(level, 2)
        self.assertEqual(body, 'keep')

    def test_headings_inside_fences_do_not_end_a_section(self):
        text = '## a\n\n```markdown\n### 예시 제목\n```\n\ntail\n\n## b\n\ndrop\n'
        _, body = build_entry.section(text, 'a')
        self.assertIn('### 예시 제목', body)
        self.assertIn('tail', body)
        self.assertNotIn('drop', body)

    def test_missing_anchor_is_an_error(self):
        with self.assertRaises(KeyError):
            build_entry.section('## a\n\nbody\n', 'nope')


class RewriteTests(unittest.TestCase):
    def setUp(self):
        self.src = build_entry.ROOT / 'Architecture/Risk_and_Authority.md'
        self.dest = build_entry.ENTRY

    def rewrite(self, body):
        return build_entry.rewrite_links(body, self.src, self.dest)

    def test_sibling_and_parent_links_resolve_from_the_destination(self):
        out = self.rewrite('[a](Company_Profile.md#기밀-영역) [b](../AI/Common_Rules.md#백업)')
        self.assertIn('](../Architecture/Company_Profile.md#기밀-영역)', out)
        self.assertIn('](Common_Rules.md#백업)', out)

    def test_vault_path_links_resolve_from_the_package_root(self):
        name = build_entry.ROOT.name
        out = self.rewrite(f'[a]({name}/Architecture/Company_Profile.md#기밀-영역)')
        self.assertIn('](../Architecture/Company_Profile.md#기밀-영역)', out)

    def test_bare_anchor_points_back_at_the_source(self):
        self.assertIn('](../Architecture/Risk_and_Authority.md#위험도)', self.rewrite('[a](#위험도)'))

    def test_absolute_urls_and_fenced_examples_are_untouched(self):
        self.assertIn('](https://example.test/x)', self.rewrite('[a](https://example.test/x)'))
        self.assertIn('](Company_Profile.md#x)',
                      self.rewrite('```\n[a](Company_Profile.md#x)\n```'))

    def test_every_rewritten_link_in_the_entry_resolves(self):
        text = build_entry.ENTRY.read_text(encoding='utf-8')
        body = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
        targets = re.findall(r'\]\(([^)]+)\)', re.sub(r'`[^`\n]*`', '', body))
        self.assertTrue(targets)
        for target in targets:
            if target.startswith('http'):
                continue
            rel = target.split('#')[0]
            if rel:
                self.assertTrue((self.dest.parent / rel).resolve().is_file(), target)


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.entry, self.manifest = build_entry.render()

    def test_committed_files_are_current(self):
        self.assertEqual(build_entry.ENTRY.read_text(encoding='utf-8'), self.entry)
        self.assertEqual(build_entry.MANIFEST.read_text(encoding='utf-8'), self.manifest)

    def test_generation_is_idempotent(self):
        self.assertEqual(build_entry.build_entry(self.entry), self.entry)

    def test_edited_canonical_section_is_detected(self):
        source = build_entry.ROOT / 'Architecture/Risk_and_Authority.md'
        original = source.read_text(encoding='utf-8')
        try:
            source.write_text(original.replace('애매하면 높은 쪽', '애매하면 낮은 쪽'), encoding='utf-8', newline='\n')
            self.assertNotEqual(build_entry.render()[0], self.entry)
        finally:
            source.write_text(original, encoding='utf-8', newline='\n')
        self.assertEqual(build_entry.render()[0], self.entry)

    def test_entry_stays_within_budget(self):
        self.assertLessEqual(len(self.entry.encode('utf-8')), 11000)
        self.assertLessEqual(self.entry.count('\n') + 1, 250)

    def test_manifest_covers_every_document_with_a_mode(self):
        data = json.loads(self.manifest)
        listed = {d['path'] for d in data['documents']}
        on_disk = {p.relative_to(build_entry.ROOT).as_posix() for p in build_entry.docs()}
        self.assertEqual(listed, on_disk)
        self.assertEqual(data['totals']['documents'], len(on_disk))
        for doc in data['documents']:
            self.assertIn(doc['mode'], {'basic', 'extended', 'reference'})
            self.assertEqual(doc['bytes'], len(
                (build_entry.ROOT / doc['path']).read_bytes()))
            self.assertTrue(doc['when_to_read'])

    def test_extension_documents_are_marked_as_skippable(self):
        data = json.loads(self.manifest)
        by_path = {d['path']: d['mode'] for d in data['documents']}
        for path in ['AI/Routing.md', 'AI/Task_and_Record_Schema.md', 'AI/Roles/Coordinator.md']:
            self.assertEqual(by_path[path], 'extended')
        self.assertEqual(by_path['AI_Agent_Company_Comparison.md'], 'reference')
        self.assertEqual(by_path['AI/Agent_Entry.md'], 'basic')


if __name__ == '__main__':
    unittest.main(verbosity=2)
