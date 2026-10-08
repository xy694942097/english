"""Download official English TED caption JSON and derive SRT using source timings."""
import argparse
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / 'references/ted/ted-100-catalog.json'
OUT = ROOT / 'materials/corpus/ted/english'
RESULTS = ROOT / 'references/ted/ted-100-download-results.json'


def stamp(ms):
    hours, rem = divmod(ms, 3600000)
    minutes, rem = divmod(rem, 60000)
    seconds, rem = divmod(rem, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{rem:03}'


def validate(data, talk):
    captions = data.get('captions')
    if not isinstance(captions, list) or len(captions) < 10:
        raise ValueError('Missing or implausibly short caption list')
    previous = -1
    for cue in captions:
        start, duration = cue['startTime'], cue['duration']
        if not isinstance(start, int) or not isinstance(duration, int):
            raise ValueError('Caption timing must be integer milliseconds')
        if start < previous or start < 0 or duration <= 0:
            raise ValueError('Invalid or backwards caption timing')
        if not isinstance(cue.get('content'), str) or not cue['content'].strip():
            raise ValueError('Empty caption content')
        previous = start
    end = max(c['startTime'] + c['duration'] for c in captions)
    expected = talk['duration_seconds'] * 1000
    if end > expected + 120000 or end < expected * 0.6:
        # Talk 2237: official transcript and player full.vtt both end at ~4 min,
        # despite the official page/player metadata reporting ~13 min.
        known_source_discrepancy = (str(talk['id']) == '2237' and len(captions) == 74
                                   and end == 244471
                                   and captions[0]['content'] == 'My first love was for the night sky.'
                                   and captions[-1]['content'] == '(Applause)')
        if not known_source_discrepancy:
            raise ValueError(f'Caption coverage suspicious: {end} vs video {expected}')
    return captions, end


def download(talk):
    url = f"https://www.ted.com/talks/subtitles/id/{talk['id']}/lang/en"
    stem = f"{talk['number']:03}-{talk['id']}.en"
    raw_path, srt_path = OUT / f'{stem}.json', OUT / f'{stem}.srt'
    result = {k: talk[k] for k in ('number', 'id', 'title', 'chinese_title', 'speaker', 'url', 'duration_seconds')}
    result['source_url'] = url
    try:
        if raw_path.exists():
            raw = raw_path.read_bytes()
            captions, end = validate(json.loads(raw), talk)
        else:
            for attempt in range(3):
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
                    with urllib.request.urlopen(req, timeout=30) as response:
                        raw = response.read()
                    captions, end = validate(json.loads(raw), talk)
                    break
                except Exception:
                    if attempt == 2:
                        raise
                    time.sleep(attempt + 1)
            raw_path.write_bytes(raw)
        srt = ''.join(f"{i}\n{stamp(c['startTime'])} --> {stamp(c['startTime'] + c['duration'])}\n{c['content'].strip()}\n\n" for i, c in enumerate(captions, 1))
        srt_path.write_text(srt, encoding='utf-8')
        result.update(status='downloaded', file=str(raw_path.relative_to(ROOT / 'materials')),
                      bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                      derived_file=str(srt_path.relative_to(ROOT / 'materials')),
                      derived_bytes=srt_path.stat().st_size,
                      derived_sha256=hashlib.sha256(srt_path.read_bytes()).hexdigest(),
                      caption_count=len(captions), first_start_ms=captions[0]['startTime'], last_end_ms=end)
        if str(talk['id']) == '2237':
            result['quality_notes'] = ('Official page duration is 13:32, but the official transcript and '
                                       'player full English VTT both contain 74 cues ending at ~4 minutes. '
                                       'Source discrepancy retained; no claim of complete 13-minute coverage.')
        print(f"OK {talk['number']:03} {len(captions)} captions", flush=True)
    except Exception as exc:
        result.update(status='failed', error=f'{type(exc).__name__}: {exc}')
        print(f"FAILED {talk['number']:03} {result['error']}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    talks = json.loads(CATALOG.read_text())['talks']
    OUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(download, talks))
    receipt = {'downloaded_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
               'source': 'TED official English caption endpoint',
               'format_note': 'Original JSON bytes preserved; SRT derived from exact startTime and duration, without guessed ends. Caption API times may exclude player intro; video-version sync not asserted.',
               'items': rows}
    RESULTS.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(f"TOTAL {len(rows)} OK {sum(r['status'] == 'downloaded' for r in rows)}", flush=True)


if __name__ == '__main__':
    main()
