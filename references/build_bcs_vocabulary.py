"""Validate cue evidence and render Better Call Saul vocabulary selections.

Usage: python3 references/build_bcs_vocabulary.py [--check-only]
Reads selection JSON only; it does not discover vocabulary or evaluate learner mastery.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'course/词汇/Better Call Saul：词汇与搭配积累.md'
DEDUP = ROOT / 'references/chunks/better-call-saul-s01-vocabulary-dedup.json'


def item_key(episode, item):
    return episode, item['word'], item['start_cue'], item['end_cue']


def reading_selections(selections):
    """Apply reviewed sense-level decisions; never auto-drop normalized words."""
    if not DEDUP.exists():
        return selections
    review = json.loads(DEDUP.read_text())
    decisions = review['excluded']
    available = {item_key(ep, item) for ep, data in selections for item in data['items']}
    excluded = {item_key(d['episode'], d) for d in decisions}
    if not excluded <= available or len(excluded) != len(decisions):
        raise ValueError('Stale or repeated cross-episode dedup decisions')
    refinements = {item_key(r['episode'], r): r for r in review.get('reading_refinements', [])}
    if not set(refinements) <= available - excluded:
        raise ValueError('Stale reading refinements')
    result = []
    for episode, data in selections:
        kept = []
        for item in data['items']:
            key = item_key(episode, item)
            if key in excluded:
                continue
            item = dict(item)
            if key in refinements:
                item.update(word=refinements[key]['reading_word'], meaning=refinements[key]['reading_meaning'])
            kept.append(item)
        result.append((episode, dict(data, items=kept)))
    return result


def read_cues(path):
    cues = {}
    for block in re.split(r'\n\s*\n', path.read_text(encoding='utf-8-sig').strip()):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit():
            continue
        number = int(lines[0])
        if number in cues:
            raise ValueError(f'Duplicate cue {number}: {path}')
        cues[number] = {
            'start': lines[1].split(' --> ')[0],
            'end': lines[1].split(' --> ')[1],
            'text': re.sub(r'<[^>]+>', '', ' '.join(lines[2:])),
        }
    return cues


def validated_selections():
    selections = []
    for path in sorted((ROOT / 'references/chunks').glob('better-call-saul-s??e??-vocabulary-selection.json')):
        data = json.loads(path.read_text())
        source = ROOT / data['source']
        if hashlib.sha256(source.read_bytes()).hexdigest() != data['sha256']:
            raise ValueError(f'Source hash mismatch: {path}')
        cues = read_cues(source)
        if data['subtitle_blocks_read'] != len(cues):
            raise ValueError(f'Block count mismatch: {path}')
        episode = re.search(r's\d\de\d\d', path.name).group().upper()
        last = 0
        for item in data['items']:
            selected = [cues[n] for n in sorted(cues) if item['start_cue'] <= n <= item['end_cue']]
            if not selected or item['start_cue'] not in cues or item['end_cue'] not in cues:
                raise ValueError(f'Missing cue endpoints: {episode} {item["word"]}')
            if item['start_cue'] < last:
                raise ValueError(f'Out of source order: {episode} {item["word"]}')
            last = item['start_cue']
            if item['quote'] != ' '.join(c['text'] for c in selected):
                raise ValueError(f'Quote mismatch: {episode} {item["word"]}')
            if item['start_time'] != selected[0]['start'] or item['end_time'] != selected[-1]['end']:
                raise ValueError(f'Time mismatch: {episode} {item["word"]}')
            if not item['word'].strip() or not item['meaning'].strip():
                raise ValueError(f'Empty item: {episode}')
        selections.append((episode, data))
    return selections


def render(selections):
    lines = ['# Better Call Saul：词汇与搭配积累', '']
    for episode, data in selections:
        lines += [f'## {episode}', '', '| 单词／搭配 | 本句意思 | 原句（时间码） |', '|---|---|---|']
        for item in data['items']:
            escape = lambda value: value.replace('|', r'\|').replace('\n', ' ')
            # Times remain exactly recorded in JSON; the reading table displays whole seconds.
            start, end = item['start_time'].split(',')[0], item['end_time'].split(',')[0]
            values = [item['word'], item['meaning'], f'{item["quote"]}（{start}–{end}）']
            lines.append('| ' + ' | '.join(escape(v) for v in values) + ' |')
        lines.append('')
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    originals = validated_selections()
    selections = reading_selections(originals)
    if not args.check_only:
        OUTPUT.write_text(render(selections))
    for episode, data in selections:
        print(f'{episode}: {len(data["items"])} items, {data["subtitle_blocks_read"]} source blocks verified')
    print(f'Total: {sum(len(d["items"]) for _, d in selections)} items; {len(selections)} episodes')
    print(f'Before cross-episode dedup: {sum(len(d["items"]) for _, d in originals)} candidates')
