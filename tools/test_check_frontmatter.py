"""Behavior checks for the frontmatter reporter. Uses a throwaway vault in the OS temp folder."""
from pathlib import Path
import json
import tempfile
import unittest

import check_frontmatter

LOCAL = {
    'exclude': ['.trash/**'],
    'values': {
        'hq-owner': {'boss': 'HQ'},
        'task-folder': 'Tasks',
        'projects-folder': 'Projects',
        'technical-wiki': 'Tech',
        'theory-wiki': 'Theory',
        'contexts': {'Lab': 'lab'},
        'project-id-pattern': '^P[0-9]{4}_[A-Z]+$',
    },
}

AI_TASK = '''---
title: 좋은 작업
status: to-do
priority: normal
tags:
  - task
  - ai
projects:
  - "[[Projects/P2601_DEMO/README|P2601]]"
owner: ai
hq: none
risk: 1
proposal_version: V1.0.0
approved_version: ""
execution_mode: autonomous
report_policy: final
write_scope:
  - Projects/P2601_DEMO/
blockedBy: []
---

# 지시
'''


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(check_frontmatter.SCHEMA.read_text(encoding='utf-8'))
        self.checker = check_frontmatter.Checker(self.schema, LOCAL)

    def codes(self, rel, text):
        name, problems = self.checker.check_file(rel, text)
        return name, [code for code, _ in problems]

    def test_schema_is_internally_consistent(self):
        placeholders = set(self.schema['placeholders'])
        for name, kind in self.schema['kinds'].items():
            self.assertLessEqual(set(kind['order']), set(kind['fields']), name)
            for field, spec in kind['fields'].items():
                self.assertIn(spec['type'], self.schema['types'], f'{name}.{field}')
                if spec['type'] == 'enum' or spec.get('item_type') == 'enum':
                    self.assertTrue('values' in spec or 'values_from' in spec, f'{name}.{field}')
                for key in ['values_from', 'pattern_from', 'range_from']:
                    if key in spec:
                        self.assertIn(spec[key], placeholders, f'{name}.{field}')

    def test_valid_ai_task_passes(self):
        self.assertEqual(self.codes('Tasks/AI/좋은 작업.md', AI_TASK), ('tasknote', []))

    def test_wrong_values_are_reported(self):
        text = (AI_TASK.replace('status: to-do', 'status: shelved').replace('risk: 1', 'risk: 3')
                .replace('blockedBy: []', 'blocked_by: []').replace('owner: ai', 'owner: someone'))
        _, codes = self.codes('Tasks/AI/x.md', text)
        for code in ['legacy-value', 'bad-enum', 'deprecated-key']:
            self.assertIn(code, codes)

    def test_style_order_and_required_fields(self):
        text = AI_TASK.replace('tags:\n  - task\n  - ai\n', 'tags: [task, ai]\n').replace('priority: normal\n', '')
        text = text.replace('title: 좋은 작업\nstatus: to-do\n', 'status: to-do\ntitle: 좋은 작업\n')
        _, codes = self.codes('Tasks/AI/x.md', text)
        for code in ['inline-list', 'missing-required', 'key-order']:
            self.assertIn(code, codes)

    def test_state_combination_uses_local_owner(self):
        ok = AI_TASK.replace('owner: ai\nhq: none', 'owner: boss\nhq: decide')
        bad = AI_TASK.replace('owner: ai\nhq: none', 'owner: boss\nhq: none')
        self.assertNotIn('bad-state', self.codes('Tasks/AI/x.md', ok)[1])
        self.assertIn('bad-state', self.codes('Tasks/AI/x.md', bad)[1])

    def test_human_task_only_needs_common_fields(self):
        text = '---\ntitle: 사람 일\nstatus: done\npriority: high\ntags:\n  - task\ncontexts:\n  - Lab\nurgency: 3\n---\n'
        self.assertEqual(self.codes('Tasks/Research/사람 일.md', text), ('tasknote', []))

    def test_project_status_range_and_pattern(self):
        text = ('---\nproject_id: bad id\nstatus: active\nphase: design\npriority: 0\n'
                'next_action: 다음 행동\nnext_deadline:\nupdated: 2026-09-16\n---\n')
        name, codes = self.codes('Projects/P2601_DEMO/STATUS.md', text)
        self.assertEqual(name, 'project_status')
        self.assertIn('out-of-range', codes)
        self.assertIn('bad-format', codes)

    def test_repo_card_and_missing_frontmatter(self):
        self.assertEqual(self.codes('Tech/Repos/x.md', '# no frontmatter\n'), ('technical_wiki', ['no-frontmatter']))
        card = ('---\ntype: repo-card\nrepo: x\nremote: git@host:x.git\nlocal_path: Tech/Clones/x\n'
                'branch: main\nlast_checked_commit: zzz\nstatus: active\nupdated: 2026-09-16\n---\n')
        self.assertEqual(self.codes('Tech/Repos/x.md', card), ('repo_card', ['bad-format']))

    def test_run_skips_excluded_and_unmatched_files_and_never_writes(self):
        root = Path(tempfile.mkdtemp(prefix='frontmatter-test-'))
        files = {'Tasks/AI/좋은 작업.md': AI_TASK, '.trash/Tasks/old.md': AI_TASK.replace('risk: 1', 'risk: 9'),
                 'Notes/free.md': '---\nanything: goes\n---\n'}
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding='utf-8', newline='\n')
        before = {rel: (root / rel).read_bytes() for rel in files}
        report = self.checker.run(root)
        self.assertEqual([(rel, name, problems) for rel, name, problems in report],
                         [('Tasks/AI/좋은 작업.md', 'tasknote', [])])
        self.assertEqual(before, {rel: (root / rel).read_bytes() for rel in files})


if __name__ == '__main__':
    unittest.main(verbosity=2)
