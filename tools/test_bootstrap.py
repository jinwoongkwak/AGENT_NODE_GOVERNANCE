"""Behavior checks for new-company creation. Retains fixtures in the OS temp folder."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

import bootstrap
import check_workspace


class BootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix='jm-protocol-test-')).resolve()
        cls.config = json.loads((bootstrap.PROTOCOL/'Setup/company.example.json').read_text())
        print('Retained test workspace:', cls.root)

    def test_dry_run_does_not_write(self):
        dest = self.root/'dry-run'
        result = bootstrap.create(self.config, dest)
        self.assertEqual(result['mode'], 'dry-run')
        self.assertFalse(dest.exists())
        self.assertGreater(result['files'], 40)

    def test_complete_creation_and_manifest(self):
        dest = self.root/'complete'
        bootstrap.create(self.config, dest, apply=True)
        self.assertEqual(check_workspace.check(dest), [])
        manifest = json.loads((dest/'00_HQ/90_SYSTEM/bootstrap-manifest.json').read_text())
        for name, digest in manifest.items():
            self.assertEqual(hashlib.sha256((dest/name).read_bytes()).hexdigest(), digest)
            self.assertNotIn('.claude', Path(name).parts)
            self.assertNotIn('.git', Path(name).parts)
        local = json.loads((dest/'00_HQ/90_SYSTEM/company.json').read_text())
        self.assertEqual(local['deployment_status'], 'draft')
        self.assertEqual(local['mode'], 'basic')
        adoption = (dest/'00_HQ/90_SYSTEM/Protocol_Adoption.md').read_text(encoding='utf-8')
        self.assertIn('미승인', adoption)
        result = subprocess.run([sys.executable, str(dest/bootstrap.PROTOCOL_PATH/'tools/validate.py')], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        with self.assertRaises(ValueError):
            bootstrap.create(self.config, dest, apply=True)
        self.assertEqual(manifest, {p: hashlib.sha256((dest/p).read_bytes()).hexdigest() for p in manifest})

    def test_empty_folder_is_allowed(self):
        dest = self.root/'empty'
        dest.mkdir()
        bootstrap.create(self.config, dest, apply=True)
        self.assertEqual(check_workspace.check(dest), [])

    def test_existing_data_is_untouched(self):
        dest = self.root/'existing'
        dest.mkdir()
        (dest/'original.txt').write_text('keep me')
        for apply in [False, True]:
            with self.assertRaises(ValueError):
                bootstrap.create(self.config, dest, apply=apply)
        self.assertEqual(list(dest.iterdir()), [dest/'original.txt'])
        self.assertEqual((dest/'original.txt').read_text(), 'keep me')

    def test_project_traversal_and_duplicates_rejected(self):
        for pid in ['../escape', 'C:/escape', 'P01/escape', 123]:
            c = copy.deepcopy(self.config)
            c['projects'][0]['id'] = pid
            with self.assertRaises(ValueError):
                bootstrap.build(c)
        c = copy.deepcopy(self.config)
        c['projects'].append(copy.deepcopy(c['projects'][0]))
        with self.assertRaises(ValueError):
            bootstrap.build(c)

    def test_owner_and_multiline_rejected(self):
        for owner in ['ai', 'none', 'Invalid Owner']:
            c = dict(self.config, hq_owner=owner)
            with self.assertRaises(ValueError):
                bootstrap.build(c)
        with self.assertRaises(ValueError):
            bootstrap.build(dict(self.config, company='Company\n---'))

    def test_collaboration_and_empty_projects(self):
        c = copy.deepcopy(self.config)
        c['projects'][0]['kind'] = 'collaboration'
        files = bootstrap.build(c, copy_protocol=False)
        self.assertIn('20_PROJECTS/COLLABORATIONS/'+c['projects'][0]['id']+'/STATUS.md', files)
        files = bootstrap.build(dict(c, projects=[]), copy_protocol=False)
        self.assertFalse(any('/STATUS.md' in p for p in files))

    def test_config_cannot_set_approval_or_escape_workspace(self):
        with self.assertRaises(ValueError):
            bootstrap.build(dict(self.config, deployment_status='active'))
        dest = self.root/'escape-check'
        bootstrap.create(self.config, dest, apply=True)
        p = dest/'00_HQ/90_SYSTEM/company.json'
        c = json.loads(p.read_text())
        c['task_folder'] = '../outside'
        p.write_text(json.dumps(c), encoding='utf-8')
        self.assertIn('Path escapes workspace: task_folder', check_workspace.check(dest))


if __name__ == '__main__':
    unittest.main(verbosity=2)
