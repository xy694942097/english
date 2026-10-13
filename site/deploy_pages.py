#!/usr/bin/env python3
"""Build the public reading site and push only its files to gh-pages."""
import shutil
import subprocess
import tempfile
from pathlib import Path
from build_static import build
from server import ROOT


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


if __name__ == '__main__':
    remote = git('remote', 'get-url', 'origin')
    with tempfile.TemporaryDirectory(prefix='english-pages-') as temp:
        checkout = Path(temp) / 'checkout'
        output = Path(temp) / 'public'
        count = build(output, ROOT / 'site/publish-nav.json')
        checkout.mkdir()
        git('init', '-b', 'gh-pages', cwd=checkout)
        git('remote', 'add', 'origin', remote, cwd=checkout)
        git('config', 'user.name', git('config', 'user.name'), cwd=checkout)
        git('config', 'user.email', git('config', 'user.email'), cwd=checkout)
        if git('ls-remote', '--heads', 'origin', 'gh-pages', cwd=checkout):
            git('fetch', '--depth=1', 'origin', 'gh-pages', cwd=checkout)
            git('checkout', '-B', 'gh-pages', 'FETCH_HEAD', cwd=checkout)
            git('rm', '-r', '--ignore-unmatch', '.', cwd=checkout)
        shutil.copytree(output, checkout, dirs_exist_ok=True)
        git('add', '-A', cwd=checkout)
        if git('status', '--porcelain', cwd=checkout):
            git('commit', '-m', f'Publish {count} read-only documents', cwd=checkout)
            git('push', 'origin', 'HEAD:gh-pages', cwd=checkout)
        print(f'Published {count} documents to gh-pages; enable gh-pages / (root) in GitHub Pages.')
