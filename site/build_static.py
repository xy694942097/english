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
    reference_only = nav.get('reference_only', {})
    if not set(reference_only).issubset(paths):
        raise ValueError('来源入口必须在发布导航中登记')
    # Local-only full texts get explicit public source pages, including in clean clones.
    readable_nav = {'groups': [], 'maintenance': []}
    groups_by_path = {}
    for key in ['groups', 'maintenance']:
        for group in nav.get(key, []):
            entries = []
            for entry in group['items']:
                original = [entry] if isinstance(entry, str) else entry['items']
                for path in original:
                    groups_by_path[path] = group['title']
                selected = [path for path in original if path not in reference_only]
                if isinstance(entry, str):
                    entries.extend(selected)
                else:
                    entries.append({**entry, 'items': selected})
            readable_nav[key].append({**group, 'items': entries})
    items = catalog(nav=readable_nav)
    for path, page in reference_only.items():
        items.append({'id': path, 'group': groups_by_path[path],
                      'title': page['title'], 'body': page['body'], 'referenceOnly': True})
    if output.exists() and any(output.iterdir()):
        raise ValueError('输出目录必须为空；请指定新的目录')
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(STATIC, output, dirs_exist_ok=True)
    (output / '.nojekyll').touch()
    # Only explicit image dependencies may be exported; never copy raw material folders.
    for item in items:
        def export_image(match):
            target = match[2].strip('<>')
            if re.match(r'^[a-z]+:|^//', target, re.I):
                return match[0]
            image = (ROOT / item['id']).parent / unquote(target)
            image = image.resolve()
            if not image.is_relative_to(ROOT / 'course') or image.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}:
                return f'（原资料图片未在公开版提供：{match[1] or "插图"}）'
            if not image.is_file():
                return f'（原资料图片缺失：{match[1] or "插图"}）'
            dest = output / 'files' / image.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(image, dest)
            return match[0]
        item['body'] = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', export_image, item['body'])
    (output / 'catalog.json').write_text(json.dumps({'items': items,
        'nav': {'groups': nav['groups'], 'maintenance': nav.get('maintenance', [])},
        'aliases': {old: new for old, new in read_aliases().items() if new in paths}},
        ensure_ascii=False), encoding='utf-8')
    return len(items)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'site/dist')
    parser.add_argument('--nav', type=Path, default=ROOT / 'site/publish-nav.json')
    args = parser.parse_args()
    print(f'Built {build(args.output, args.nav)} read-only documents in {args.output}')
