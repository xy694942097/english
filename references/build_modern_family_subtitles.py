#!/usr/bin/env python3
"""Build UTF-8 episode subtitles from locally preserved SUBDL ZIPs; no network."""
import collections
import hashlib
import json
from pathlib import Path
from document_paths import write_document
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'materials/corpus/tv-subtitles/modern-family'
INDEX = ROOT / 'references/subtitles/modern-family-index.json'
EXPECTED = {s: (24 if s <= 6 else 22 if s <= 10 else 18) for s in range(1, 12)}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    for encoding in ('utf-8-sig', 'cp1252', 'latin-1'):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    raise ValueError('Cannot decode subtitle')


def episode_numbers(name):
    match = re.search(r's(\d{1,2})e(\d{1,2})(?:(?:e|-)(\d{1,2}))?', name, re.I)
    if not match:
        match = re.search(r'(\d{1,2})x(\d{1,2})(?:-(\d{1,2}))?', name, re.I)
    if not match:
        raise ValueError(f'No season/episode identity in {name}')
    season, first = int(match[1]), int(match[2])
    last = int(match[3]) if match[3] else first
    if last < first or last > EXPECTED.get(season, 0):
        raise ValueError(f'Unexpected episode range in {name}')
    return season, list(range(first, last + 1))


def normalize_cue_spacing(text):
    """Some packs insert blank lines within a cue, splitting it for SRT players."""
    pattern = (r'(?m)^[ \t]*\d+[ \t]*\n[ \t]*\d{1,2}:\d\d:\d\d[,.]\d{3}'
               r'[ \t]*-->[ \t]*\d{1,2}:\d\d:\d\d[,.]\d{3}[^\n]*\n')
    matches = list(re.finditer(pattern, text))
    assert matches and not text[:matches[0].start()].strip(), 'Unexpected non-SRT preamble'
    cues = []
    repaired = 0
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        segment = text[match.start():end].strip('\n')
        lines = segment.splitlines()
        repaired += sum(not line.strip() for line in lines)
        cues.append('\n'.join(line for line in lines if line.strip()))
    return '\n\n'.join(cues) + '\n', repaired


def build():
    sources = json.loads((DATA / 'archives/sources.json').read_text())
    reference = json.loads((DATA / 'episode-list.tvmaze.json').read_text())
    expected_pairs = {(e['season'], e['number']) for e in reference}
    declared_pairs = {(s, e) for s, count in EXPECTED.items() for e in range(1, count + 1)}
    assert expected_pairs == declared_pairs, 'Episode directory disagrees with expected 250 episodes'
    titles = {(e['season'], e['number']): e['name'] for e in reference}
    rows, covered, hashes = [], set(), set()
    for source in sources:
        if source.get('selection') == 'unused':
            continue
        archive = ROOT / 'materials' / source['archive']
        archive_bytes = archive.read_bytes()
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None, f'ZIP CRC error: {archive}'
            assert sum(i.file_size for i in z.infolist()) < 60_000_000, 'Oversized ZIP'
            for member in sorted(z.namelist()):
                if not member.lower().endswith('.srt'):
                    continue
                season, episodes = episode_numbers(member)
                assert season == source['season'], (member, source['season'])
                if source.get('supplement_episode') and episodes != [source['supplement_episode']]:
                    continue
                pairs = {(season, e) for e in episodes}
                assert not (pairs & covered), f'Duplicate episode assignment: {member}'
                assert z.getinfo(member).file_size < 2_000_000
                original = z.read(member)
                text, encoding = decode(original)
                text = text.replace('\r\n', '\n').replace('\r', '\n')
                text, repaired_blank_lines = normalize_cue_spacing(text)
                assert not re.search(r'<html|<!doctype', text, re.I), member
                times = re.findall(r'(?m)^\s*(\d{1,2}):(\d\d):(\d\d)[,.](\d{3})\s*-->', text)
                assert len(times) >= 100, f'Too few cues: {member}'
                starts = [int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms) for h,m,s,ms in times]
                words = re.findall(r'[a-z]+', text.lower())
                common = set('the a an i you he she we they is are was were to of and it that this in for my your me do don not have on'.split())
                english_ratio = sum(w in common for w in words) / max(len(words), 1)
                assert english_ratio > 0.15, f'English language check failed: {member}'
                label = f'S{season:02}E{episodes[0]:02}'
                if len(episodes) > 1:
                    label += f'-E{episodes[-1]:02}'
                target = DATA / f'S{season:02}' / f'Modern.Family.{label}.en.srt'
                target.parent.mkdir(exist_ok=True)
                output = text.encode('utf-8')
                assert digest(output) not in hashes, f'Identical subtitles assigned to different episodes: {member}'
                target.write_bytes(output)
                rows.append({'file': str(target.relative_to(ROOT)), 'season': season,
                             'episodes': episodes, 'titles': [titles[(season,e)] for e in episodes],
                             'bytes': len(output), 'sha256': digest(output), 'cues': len(times),
                             'source_encoding': encoding,
                             'removed_blank_lines_inside_cues': repaired_blank_lines,
                             'timeline_decreases': sum(b < a for a,b in zip(starts, starts[1:])),
                             'english_function_word_ratio': round(english_ratio, 4),
                             'source_page': source['source_page'], 'url': source['url'],
                             'release': source['release'], 'archive': source['archive'],
                             'archive_sha256': digest(archive_bytes), 'archive_member': member,
                             'original_member_sha256': digest(original)})
                covered.update(pairs)
                hashes.add(digest(output))
    assert covered == expected_pairs, f'Missing: {sorted(expected_pairs-covered)}; unexpected: {sorted(covered-expected_pairs)}'
    rows.sort(key=lambda x: (x['season'], x['episodes'][0]))
    INDEX.parent.mkdir(exist_ok=True)
    result = {'show': 'Modern Family', 'language': 'English', 'regular_episodes': 250,
              'subtitle_files': len(rows), 'episode_reference': 'https://www.tvmaze.com/shows/80/modern-family/episodes',
              'episode_metadata_license': 'CC BY-SA; TVmaze API https://www.tvmaze.com/api#licensing',
              'normalization': 'UTF-8, LF line endings, remove empty lines inside cues; dialogue, timestamps, credits and numbering unchanged',
              'files': rows}
    write_document(INDEX, json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for row in rows:
        assert digest((ROOT / row['file']).read_bytes()) == row['sha256']
    summary = collections.Counter()
    for row in rows:
        summary[row['season']] += len(row['episodes'])
    print(json.dumps({'covered': dict(summary), 'subtitle_files': len(rows),
                      'cues': sum(x['cues'] for x in rows), 'bytes': sum(x['bytes'] for x in rows),
                      'legacy_encoding_files': sum(x['source_encoding'] != 'utf-8-sig' for x in rows),
                      'cue_spacing_repaired_files': sum(bool(x['removed_blank_lines_inside_cues']) for x in rows),
                      'timeline_decrease_files': sum(bool(x['timeline_decreases']) for x in rows)}, indent=2))


if __name__ == '__main__':
    build()
