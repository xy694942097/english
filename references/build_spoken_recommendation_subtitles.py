#!/usr/bin/env python3
"""Prepare the six requested English subtitle collections from preserved ZIPs."""
import collections
import json
from pathlib import Path
from document_paths import write_document
import re
import zipfile
from build_modern_family_subtitles import decode, digest, normalize_cue_spacing

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'references/subtitles/spoken-recommendations-sources.json'
INDEX = ROOT / 'references/subtitles/spoken-recommendations-index.json'
CUTOFF = '2026-10-08'
NAMES = {'the-good-place': 'The.Good.Place', 'superstore': 'Superstore',
         'ted-lasso': 'Ted.Lasso', 'shrinking': 'Shrinking',
         'the-intern-2015': 'The.Intern.2015', 'about-time-2013': 'About.Time.2013'}


def identify(member, source):
    if source.get('type') == 'movie':
        return 0, [1]
    match = re.search(r's(\d{1,2})e(\d{1,2})(?:(?:e|-e?)(\d{1,2}))?', member, re.I)
    if not match:
        match = re.search(r'(\d{1,2})x(\d{1,2})(?:-(\d{1,2}))?', member, re.I)
    if match:
        season, first = int(match[1]), int(match[2])
        last = int(match[3]) if match[3] else first
    else:
        match = re.match(r'(\d{1,2})\s', Path(member).name)
        assert match, f'Unknown episode filename: {member}'
        season, first = source['season'], int(match[1])
        last = first
    assert season == source['season'], member
    if source['show'] == 'the-good-place' and season in (2, 3) or source['show'] == 'shrinking' and season == 3:
        # These selected releases combine the two-part premiere into file 01.
        assert first == last, member
        return season, [1, 2] if first == 1 else [first + 1]
    return season, list(range(first, last + 1))


def build():
    jobs = json.loads(SOURCES.read_text())
    references, expected = {}, {}
    for slug in ('the-good-place', 'superstore', 'ted-lasso', 'shrinking'):
        data = ROOT / 'materials/corpus/tv-subtitles' / slug
        show = json.loads((data / 'episode-list.tvmaze.json').read_text())
        episodes = [e for e in show['_embedded']['episodes'] if e['number'] is not None and e['airdate'] and e['airdate'] <= CUTOFF]
        references[slug] = {(e['season'], e['number']): e['name'] for e in episodes}
        expected[slug] = set(references[slug])
    # This episode is counted as an Olympics special by some directories.
    references['superstore'][(2, 0)] = 'Olympics Special'
    expected['superstore'].add((2, 0))
    candidates, exclusions = collections.defaultdict(list), []
    for source in jobs:
        archive = ROOT / 'materials' / source['archive']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None, archive
            assert sum(i.file_size for i in z.infolist()) < 60_000_000
            for member in sorted(z.namelist()):
                if not member.lower().endswith('.srt') or '__MACOSX' in member:
                    continue
                assert z.getinfo(member).file_size < 3_000_000
                raw = z.read(member)
                text, encoding = decode(raw)
                text = text.replace('\r\n', '\n').replace('\r', '\n')
                cue_count = len(re.findall(r'(?m)^\s*\d{1,2}:\d\d:\d\d[,.]\d{3}\s*-->', text))
                if cue_count < 100:
                    exclusions.append({'archive': source['archive'], 'member': member,
                                       'reason': 'Metadata/short file, not an episode subtitle', 'cues': cue_count})
                    continue
                season, episodes = identify(member, source)
                text, repaired = normalize_cue_spacing(text)
                key = (source['show'], season, tuple(episodes))
                hi = bool(re.search(r'(?:^|[._\[\]\s-])(?:hi|sdh)(?:$|[._\[\]\s-])', member, re.I))
                candidates[key].append({'member': member, 'source': source, 'text': text,
                                        'encoding': encoding, 'repaired': repaired, 'hi': hi,
                                        'original_sha256': digest(raw)})
    rows, covered, seen_hashes = [], collections.defaultdict(set), set()
    for (slug, season, episodes), variants in sorted(candidates.items()):
        selected = min(variants, key=lambda x: (x['hi'], x['member']))
        for other in variants:
            if other is not selected:
                exclusions.append({'archive': other['source']['archive'], 'member': other['member'],
                                   'reason': 'Alternative HI/non-HI version of selected episode'})
        pairs = {(season, e) for e in episodes}
        movie = selected['source'].get('type') == 'movie'
        if not movie:
            assert pairs <= expected[slug], (slug, pairs - expected[slug])
            assert not covered[slug] & pairs, (slug, pairs)
            covered[slug].update(pairs)
        text = selected['text']
        assert not re.search(r'<html|<!doctype', text, re.I)
        words = re.findall(r'[a-z]+', text.lower())
        common = set('the a an i you he she we they is are was were to of and it that this in for my your me do don not have on'.split())
        ratio = sum(w in common for w in words)/max(len(words), 1)
        assert ratio > 0.15, f'English language screening failed: {slug}, {selected["member"]}'
        times = re.findall(r'(?m)^\s*(\d{1,2}):(\d\d):(\d\d)[,.](\d{3})\s*-->', text)
        starts = [int(h)*3600000+int(m)*60000+int(s)*1000+int(ms) for h,m,s,ms in times]
        if len(episodes) == 2:
            assert starts[-1] > 35*60*1000, f'Merged premiere too short: {slug}'
        data = ROOT / 'materials/corpus' / ('movie-subtitles' if movie else 'tv-subtitles') / slug
        label = f'S{season:02}E{episodes[0]:02}'
        if len(episodes) > 1:
            label += f'-E{episodes[-1]:02}'
        folder = data if movie else data/f'S{season:02}'
        folder.mkdir(exist_ok=True)
        target = folder/(NAMES[slug]+('' if movie else '.'+label)+'.en.srt')
        output = text.encode('utf-8')
        sha = digest(output)
        assert sha not in seen_hashes, f'Identical files across episodes: {slug} {label}'
        seen_hashes.add(sha)
        target.write_bytes(output)
        src = selected['source']
        rows.append({'show': slug, 'file': str(target.relative_to(ROOT)), 'season': season,
                     'episodes': list(episodes), 'titles': [references[slug][(season,e)] for e in episodes] if not movie else [NAMES[slug]],
                     'bytes': len(output), 'sha256': sha, 'cues': len(times),
                     'source_encoding': selected['encoding'], 'hearing_impaired': selected['hi'],
                     'removed_blank_lines_inside_cues': selected['repaired'],
                     'timeline_decreases': sum(b<a for a,b in zip(starts,starts[1:])),
                     'english_function_word_ratio': round(ratio,4), 'archive': src['archive'],
                     'archive_sha256': digest((ROOT/'materials'/src['archive']).read_bytes()),
                     'archive_member': selected['member'], 'original_member_sha256': selected['original_sha256'],
                     'release': src['release'], 'url': src['url'], 'source_page': src['page']})
    for slug, wanted in expected.items():
        assert covered[slug] == wanted, f'{slug} missing: {sorted(wanted-covered[slug])}'
    stats = {}
    for slug in NAMES:
        items = [x for x in rows if x['show'] == slug]
        stats[slug] = {'files': len(items), 'covered_episodes': len(covered[slug]) if slug in expected else None,
                       'seasons': dict(sorted(collections.Counter(s for s,e in covered[slug]).items())) if slug in expected else None,
                       'cues': sum(x['cues'] for x in items)}
    result = {'cutoff': CUTOFF, 'language': 'English', 'statistics': stats,
              'episode_reference': 'TVmaze show APIs; Superstore Olympics additionally identified via SUBDL S02E00',
              'episode_metadata_license': 'TVmaze CC BY-SA https://www.tvmaze.com/api#licensing',
              'normalization': 'UTF-8/LF; remove blank lines inside cues; preserve dialogue, timestamps and numbering',
              'files': rows, 'excluded_members': exclusions}
    write_document(INDEX, json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(stats,indent=2))
    print('Totals:', len(rows), 'SRT files;', sum(x['cues'] for x in rows), 'cues;', len(exclusions), 'excluded variants/metadata')


if __name__ == '__main__':
    build()
