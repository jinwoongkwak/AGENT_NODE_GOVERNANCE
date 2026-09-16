import hashlib
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent / 'connect_repos.sh'
MARK = ':com.dropbox.ignored'


def find_bash():
    git = shutil.which('git')
    if git:
        for parent in Path(git).resolve().parents[:3]:
            candidate = parent / 'bin' / 'bash.exe'
            if candidate.exists():
                return str(candidate)
    return None


def force_rmtree(path):
    def retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)
    shutil.rmtree(path, onerror=retry)


def git(*args, cwd=None):
    result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def snapshot(root):
    files = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for name in filenames:
            if name == '.git':
                continue
            path = Path(dirpath) / name
            files[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def has_mark(path):
    try:
        with open(str(path) + MARK, encoding='utf-8') as fh:
            return fh.read().strip() == '1'
    except OSError:
        return False


@unittest.skipUnless(os.name == 'nt' and find_bash() and shutil.which('powershell.exe'),
                     'needs Windows, Git Bash, and PowerShell')
class ConnectReposTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bash = find_bash()
        cls.tmp = Path(tempfile.mkdtemp(prefix='pod connect test ')).resolve()
        cls.remotes = cls.tmp / 'remotes'
        cls.remotes.mkdir()

        seed_sub = cls.tmp / 'seed sub'
        seed_sub.mkdir()
        git('init', '-q', '-b', 'main', cwd=seed_sub)
        (seed_sub / 'lib.txt').write_text('library\n', encoding='utf-8')
        git('add', '.', cwd=seed_sub)
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'sub', cwd=seed_sub)
        cls.sub_remote = cls.remotes / 'sub.git'
        git('clone', '-q', '--bare', str(seed_sub), str(cls.sub_remote))

        seed = cls.tmp / 'seed app'
        seed.mkdir()
        git('init', '-q', '-b', 'main', cwd=seed)
        (seed / 'a.txt').write_text('alpha\n', encoding='utf-8')
        (seed / 'docs').mkdir()
        (seed / 'docs' / 'b.md').write_text('# beta\n', encoding='utf-8')
        git('add', '.', cwd=seed)
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base', cwd=seed)
        git('switch', '-q', '-c', 'feature/x', cwd=seed)
        git('-c', 'protocol.file.allow=always', 'submodule', 'add', '-q',
            cls.sub_remote.as_posix(), 'libs/sub', cwd=seed)
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'add sub', cwd=seed)
        cls.app_remote = cls.remotes / 'app.git'
        git('clone', '-q', '--bare', str(seed), str(cls.app_remote))

    @classmethod
    def tearDownClass(cls):
        force_rmtree(cls.tmp)

    def make_vault(self, name):
        vault = self.tmp / name
        repo = vault / 'Repos' / 'app one'
        repo.parent.mkdir(parents=True)
        git('-c', 'protocol.file.allow=always', 'clone', '-q', '-b', 'feature/x', '--recurse-submodules',
            self.app_remote.as_posix(), str(repo))
        return vault, repo

    def strip_git(self, repo):
        force_rmtree(repo / '.git')
        (repo / 'libs' / 'sub' / '.git').unlink()

    def write_manifest(self, vault, rows):
        manifest = vault / 'repositories.tsv'
        lines = ['path\tremote\tbranch\tconfig'] + ['\t'.join(r) for r in rows]
        manifest.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        return manifest

    def run_tool(self, vault, manifest, *extra):
        result = subprocess.run([self.bash, str(TOOL), '--root', str(vault), '--manifest', str(manifest), *extra],
                                capture_output=True, text=True, encoding='utf-8', stdin=subprocess.DEVNULL)
        return result.returncode, result.stdout + result.stderr

    def remote_refs(self):
        return git('for-each-ref', cwd=self.app_remote), git('for-each-ref', cwd=self.sub_remote)

    def test_connects_missing_git_without_touching_files(self):
        vault, repo = self.make_vault('vault connect')
        (repo / 'a.txt').write_text('alpha edited on another device\n', encoding='utf-8')
        self.strip_git(repo)
        before_files = snapshot(repo)
        before_refs = self.remote_refs()
        manifest = self.write_manifest(vault, [('Repos/app one', self.app_remote.as_posix(), 'feature/x',
                                               'core.longpaths=true')])

        code, out = self.run_tool(vault, manifest, '--apply')
        self.assertEqual(code, 0, out)
        self.assertIn('[CONNECTED]', out)
        self.assertEqual(snapshot(repo), before_files)
        self.assertEqual(git('symbolic-ref', '--short', 'HEAD', cwd=repo), 'feature/x')
        self.assertEqual(git('rev-parse', '--abbrev-ref', '@{u}', cwd=repo), 'origin/feature/x')
        self.assertEqual(git('config', 'core.longpaths', cwd=repo), 'true')
        self.assertEqual(git('status', '--porcelain', cwd=repo), 'M a.txt')
        self.assertTrue((repo / 'libs' / 'sub' / '.git').is_file())
        self.assertFalse(git('submodule', 'status', cwd=repo).startswith('-'))
        self.assertTrue(has_mark(repo / '.git'))
        self.assertTrue(has_mark(repo / 'libs' / 'sub' / '.git'))
        self.assertIn('/Connect_Repo.sh', (repo / '.git' / 'info' / 'exclude').read_text(encoding='utf-8'))
        self.assertEqual(self.remote_refs(), before_refs)

        code, out = self.run_tool(vault, manifest, '--apply')
        self.assertEqual(code, 0, out)
        self.assertIn('[OK]', out)
        self.assertEqual(snapshot(repo), before_files)
        self.assertEqual(git('status', '--porcelain', cwd=repo), 'M a.txt')
        self.assertEqual(self.remote_refs(), before_refs)

    def test_check_mode_changes_nothing(self):
        vault, repo = self.make_vault('vault check')
        self.strip_git(repo)
        manifest = self.write_manifest(vault, [('Repos/app one', self.app_remote.as_posix(), 'feature/x', '')])
        before_files = snapshot(vault)
        code, out = self.run_tool(vault, manifest)
        self.assertEqual(code, 0, out)
        self.assertIn('[WARN]', out)
        self.assertFalse((repo / '.git').exists())
        self.assertEqual(snapshot(vault), before_files)

    def test_skip_fail_warn_and_filter(self):
        vault, repo = self.make_vault('vault cases')
        broken = vault / 'Repos' / 'broken'
        broken.mkdir()
        (broken / 'x.txt').write_text('x\n', encoding='utf-8')
        manifest = self.write_manifest(vault, [
            ('Repos/app one', (self.remotes / 'other.git').as_posix(), 'feature/x', ''),
            ('Repos/missing', self.app_remote.as_posix(), 'main', ''),
            ('Repos/broken', (self.remotes / 'nope.git').as_posix(), 'main', ''),
        ])
        before_url = git('remote', 'get-url', 'origin', cwd=repo)

        code, out = self.run_tool(vault, manifest, '--apply')
        self.assertEqual(code, 1, out)
        self.assertIn('[WARN]', out)
        self.assertIn('[SKIP]', out)
        self.assertIn('[FAIL]', out)
        self.assertEqual(git('remote', 'get-url', 'origin', cwd=repo), before_url)

        code, out = self.run_tool(vault, manifest, '--apply', '--repo', 'Repos\\missing')
        self.assertEqual(code, 0, out)
        self.assertIn('[SKIP]', out)
        self.assertNotIn('Repos/broken', out)

        code, out = self.run_tool(vault, manifest, '--repo', 'Repos/unknown')
        self.assertEqual(code, 1, out)
        self.assertIn('목록에 없는 경로', out)

    def test_launchers(self):
        vault, repo = self.make_vault('vault launch')
        tools = vault / 'PROTO' / 'tools'
        tools.mkdir(parents=True)
        shutil.copy(TOOL, tools / 'connect_repos.sh')
        (vault / 'Profile').mkdir()
        manifest = self.write_manifest(vault / 'Profile', [
            ('Repos/app one', self.app_remote.as_posix(), 'feature/x', '')])
        result = subprocess.run([self.bash, str(tools / 'connect_repos.sh'), '--root', str(vault),
                                 '--manifest', str(manifest), '--apply', '--install-launchers'],
                                capture_output=True, text=True, encoding='utf-8', stdin=subprocess.DEVNULL)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((vault / 'Connect_Repos.sh').is_file())
        self.assertTrue((repo / 'Connect_Repo.sh').is_file())
        self.assertEqual(git('status', '--porcelain', cwd=repo), '')

        self.strip_git(repo)
        result = subprocess.run([self.bash, str(repo / 'Connect_Repo.sh')],
                                capture_output=True, text=True, encoding='utf-8', stdin=subprocess.DEVNULL)
        out = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, out)
        self.assertIn('[CONNECTED]', out)
        self.assertEqual(git('status', '--porcelain', cwd=repo), '')


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    unittest.main()
