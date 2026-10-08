"""Download TED English captions in memory and save titled plain-text transcripts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'references/ted/ted-100-catalog.md'
OUT = ROOT / 'materials/corpus/ted/english'


def read_catalog():
    talks = []
    for line in CATALOG.read_text().splitlines():
        if not re.match(r'^\| \d{3} \|', line):
            continue
        cells = [s.strip() for s in re.split(r'(?<!\\)\|', line)[1:-1]]
        number, title, speaker, duration, year, ted_id = cells
        match = re.fullmatch(r'\[(.*?)\]\((https://www\.ted\.com/talks/[^)]+)\)<br>(.*)', title)
        if not match:
            raise ValueError(f'Invalid catalogue row: {number}')
        cn, url, en = match.groups()
        talks.append(dict(number=int(number), id=ted_id, title=en, chinese_title=cn,
                          speaker=speaker, year=year, duration=duration, url=url))
    if len(talks) != 100 or len({t['id'] for t in talks}) != 100:
        raise ValueError('Expected 100 distinct catalogue entries')
    return talks


def render(talk, captions):
    paragraphs, current = [], []
    for cue in captions:
        if cue.get('startOfParagraph') and current:
            paragraphs.append(' '.join(current))
            current = []
        current.append(re.sub(r'\s+', ' ', cue['content']).strip())
    if current:
        paragraphs.append(' '.join(current))
    if not paragraphs or any(not p for p in paragraphs):
        raise ValueError('Empty transcript')
    source = f"https://www.ted.com/talks/subtitles/id/{talk['id']}/lang/en"
    header = [f"TED {talk['number']:03}", f"Title: {talk['title']}",
              f"中文标题: {talk['chinese_title']}", f"Speaker: {talk['speaker']}",
              f"Year: {talk['year']}", f"Duration (official metadata): {talk['duration']}",
              f"TED ID: {talk['id']}", 'Language: English',
              f"Official URL: {talk['url']}", f"Caption source: {source}"]
    if str(talk['id']) == '2237':
        header.append('Note: Official duration is 13:32, but official transcript and player captions end at about 4 minutes. Source discrepancy retained.')
    return '\n'.join(header) + '\n\n--- Transcript ---\n\n' + '\n\n'.join(paragraphs) + '\n'


def download(talk, refresh=False):
    path = OUT / f"{talk['number']:03}-{talk['url'].rsplit('/', 1)[1]}.txt"
    if path.exists() and not refresh:
        return f"EXISTS {talk['number']:03}"
    source = f"https://www.ted.com/talks/subtitles/id/{talk['id']}/lang/en"
    request = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        captions = json.loads(response.read())['captions']
    if len(captions) < 10:
        raise ValueError(f"Missing captions: {talk['number']}")
    path.write_text(render(talk, captions), encoding='utf-8')
    return f"OK {talk['number']:03}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true', help='Fetch again even if TXT exists')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for message in pool.map(lambda t: download(t, args.refresh), read_catalog()):
            print(message, flush=True)
    print('TXT only; network JSON is not saved. Refreshes need manifest hash re-registration.')


if __name__ == '__main__':
    main()
