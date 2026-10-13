#!/usr/bin/env python3
"""Build a reviewed subset of the book for static hosting such as GitHub Pages."""
import argparse
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote
from server import ROOT, STATIC, catalog, read_aliases, read_nav


def build(output, navigation):
    nav = json.loads(navigation.read_text(encoding='utf-8'))
    paths = set()
    def collect(entries):
        for entry in entries:
            if isinstance(entry, str):
                paths.add(entry)
            else:
                collect(entry['items'])
    for group in nav['groups'] + nav.get('maintenance', []):
        collect(group['items'])
    published_paths = paths.copy()
    paths.clear()
    for group in read_nav()['groups'] + read_nav().get('maintenance', []):
        collect(group['items'])
    if not published_paths.issubset(paths):
        raise ValueError('发布清单包含未在 nav.json 登记的文档')
    paths = published_paths
    items = catalog(nav=nav)
    if output.exists() and any(output.iterdir()):
        raise ValueError('输出目录必须为空；请指定新的目录')
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(STATIC, output, dirs_exist_ok=True)
    (output / 'catalog.json').write_text(json.dumps({'items': items, 'nav': nav,
        'aliases': {old: new for old, new in read_aliases().items() if new in paths}},
        ensure_ascii=False), encoding='utf-8')
    (output / '.nojekyll').touch()
    # Only explicit image dependencies may be exported; never copy raw material folders.
    for item in items:
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', item['body']):
            target = target.strip('<>')
            if re.match(r'^[a-z]+:|^//', target, re.I):
                continue
            image = (ROOT / item['id']).parent / unquote(target)
            image = image.resolve()
            if not image.is_relative_to(ROOT / 'course') or image.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}:
                raise ValueError(f'不允许公开的图片路径: {target}')
            if not image.is_file():
                raise ValueError(f'图片不存在: {image}')
            dest = output / 'files' / image.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(image, dest)
    return len(items)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'site/dist')
    parser.add_argument('--nav', type=Path, default=ROOT / 'site/publish-nav.json')
    args = parser.parse_args()
    print(f'Built {build(args.output, args.nav)} read-only documents in {args.output}')
