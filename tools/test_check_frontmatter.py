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
tags:
  - task
  - ai
projects:
  - "[[Projects/P2601_DEMO/README|P2601]]"
contexts: []
owner: ai
hq_todo: none
risk: 1
llm_model: Claude Sonnet 5
proposal_version: V1.0.0
approved_version: ""
recommended_model: Claude Sonnet 5
execution_mode: autonomous
report_policy: final
write_scope:
  - Projects/P2601_DEMO/
blockedBy: []
scheduled:
due:
completedDate:
timeEstimate:
dateCreated: 2026-09-16
dateModified:
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
        text = AI_TASK.replace('tags:\n  - task\n  - ai\n', 'tags: [task, ai]\n').replace('llm_model: Claude Sonnet 5\n', '')
        text = text.replace('title: 좋은 작업\nstatus: to-do\n', 'status: to-do\ntitle: 좋은 작업\n')
        _, codes = self.codes('Tasks/AI/x.md', text)
        for code in ['inline-list', 'missing-required', 'key-order']:
            self.assertIn(code, codes)

    def test_state_combination_uses_local_owner(self):
        ok = AI_TASK.replace('owner: ai\nhq_todo: none', 'owner: boss\nhq_todo: decide')
        bad = AI_TASK.replace('owner: ai\nhq_todo: none', 'owner: boss\nhq_todo: none')
        self.assertNotIn('bad-state', self.codes('Tasks/AI/x.md', ok)[1])
        self.assertIn('bad-state', self.codes('Tasks/AI/x.md', bad)[1])

    def test_review_pending_task_is_not_done(self):
        review = AI_TASK.replace('status: to-do', 'status: in-progress').replace(
            'owner: ai\nhq_todo: none', 'owner: boss\nhq_todo: review')
        old = review.replace('status: in-progress', 'status: done')
        self.assertNotIn('bad-state', self.codes('Tasks/AI/x.md', review)[1])
        self.assertIn('bad-state', self.codes('Tasks/AI/x.md', old)[1])

    def test_completed_date_only_when_closed(self):
        dated = AI_TASK.replace('completedDate:\n', 'completedDate: 2026-09-16\n')
        review = dated.replace('status: to-do', 'status: in-progress').replace(
            'owner: ai\nhq_todo: none', 'owner: boss\nhq_todo: review')
        closed = dated.replace('status: to-do', 'status: done').replace('owner: ai', 'owner: none')
        self.assertIn('completed-date-open', self.codes('Tasks/AI/x.md', review)[1])
        self.assertNotIn('completed-date-open', self.codes('Tasks/AI/x.md', closed)[1])
        self.assertNotIn('completed-date-open', self.codes('Tasks/AI/x.md', AI_TASK)[1])

    def test_human_task_only_needs_common_fields(self):
        text = ('---\ntitle: 사람 일\nstatus: delayed\ntags:\n  - task\n  - admin\n'
                'contexts:\n  - Lab\nblockedBy: []\nscheduled:\ndue:\ncompletedDate:\ntimeEstimate:\n'
                'ForToday: false\nwaiting: true\ndateCreated:\ndateModified:\n---\n')
        self.assertEqual(self.codes('Tasks/Research/사람 일.md', text), ('tasknote', []))

    def test_missing_optional_keys_are_reported(self):
        text = AI_TASK.replace('scheduled:\ndue:\n', '')
        _, codes = self.codes('Tasks/AI/좋은 작업.md', text)
        self.assertEqual(codes, ['missing-optional', 'missing-optional'])
        human = ('---\ntitle: 사람 일\nstatus: to-do\ntags:\n  - task\n  - admin\n---\n')
        _, codes = self.codes('Tasks/Research/사람 일.md', human)
        self.assertEqual(codes.count('missing-optional'), 10)
        self.assertNotIn('missing-required', codes)

    def test_title_must_match_file_name(self):
        self.assertEqual(self.codes('Tasks/AI/다른 이름.md', AI_TASK), ('tasknote', ['title-mismatch']))

    def test_required_list_must_not_be_empty(self):
        text = AI_TASK.replace('write_scope:\n  - Projects/P2601_DEMO/\n', 'write_scope: []\n')
        self.assertEqual(self.codes('Tasks/AI/좋은 작업.md', text), ('tasknote', ['empty-required']))

    def test_human_task_without_admin_tag_and_dropped_fields(self):
        text = ('---\ntitle: 사람 일\nstatus: done\npriority: high\ntags:\n  - task\n'
                'contexts:\n  - Lab\nurgency: 3\n---\n')
        _, codes = self.codes('Tasks/Research/사람 일.md', text)
        self.assertEqual(codes.count('deprecated-key'), 2)
        self.assertIn('missing-tag', codes)

    def test_project_status_pattern_and_dropped_priority(self):
        text = ('---\nproject_id: bad id\nstatus: active\nphase: design\npriority: 1\n'
                'next_action: 다음 행동\nnext_deadline:\nupdated: 2026-09-16\n---\n')
        name, codes = self.codes('Projects/P2601_DEMO/STATUS.md', text)
        self.assertEqual(name, 'project_status')
        self.assertIn('bad-format', codes)
        self.assertIn('deprecated-key', codes)

    def test_project_readme_renamed_and_dropped_fields(self):
        text = ('---\nproject_id: P2601_DEMO\ntype: collaboration\ncodename: demo\n'
                'partners:\n  - 어떤 연구실\ncreated: 2026-09-16\n---\n')
        name, codes = self.codes('Projects/P2601_DEMO/README.md', text)
        self.assertEqual(name, 'project_readme')
        self.assertEqual(codes.count('deprecated-key'), 2)

    def test_roadmap_kinds_and_depth_limit(self):
        text = ('---\nproject_id: P2601_DEMO\ntype: project-roadmap\napproved_version: ""\n'
                'updated: 2026-09-23\nllm_model: Claude Opus 5.5\n---\n')
        self.assertEqual(self.codes('Projects/P2601_DEMO/ROADMAP.md', text), ('project_roadmap', []))
        self.assertEqual(self.codes('Projects/COLLAB/P2601_DEMO/ROADMAP.md', text)[0], 'project_roadmap')
        self.assertEqual(self.codes('Projects/P2601_DEMO/30_SOURCE/repo/ROADMAP.md', text), (None, []))
        portfolio = '---\ntype: portfolio-roadmap\napproved_version: V1.0.0\nupdated: 2026-09-23\nllm_model:\n---\n'
        self.assertEqual(self.codes('HQ/Portfolio_Roadmap.md', portfolio), ('portfolio_roadmap', []))

    def test_theory_wiki_requires_updated_and_drops_related(self):
        text = ('---\nauthor: 사람\naffiliation: 어딘가\ntags:\n  - theory\n'
                'created: 2026-09-16\nlanguage: KR\nsources:\n  - 어떤 책\n'
                'related:\n  - "[[Theory/x]]"\n---\n')
        name, codes = self.codes('Theory/x.md', text)
        self.assertEqual(name, 'theory_wiki')
        self.assertIn('missing-required', codes)
        self.assertIn('deprecated-key', codes)

    def test_repo_card_and_missing_frontmatter(self):
        self.assertEqual(self.codes('Tech/Repos/x.md', '# no frontmatter\n'), ('technical_wiki', ['no-frontmatter']))
        card = ('---\ntype: repo-card\nrepo: x\nremote: git@host:x.git\nlocal_path: Tech/Clones/x\n'
                'branch: main\nlast_checked_commit: zzz\nstatus: active\nupdated: 2026-09-16\nllm_model:\n---\n')
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
