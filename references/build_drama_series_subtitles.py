#!/usr/bin/env python3
"""Prepare the six drama/comedy collections from preserved local sources."""
import collections
from html.parser import HTMLParser
import json
from pathlib import Path
from document_paths import write_document
import re
import zipfile
from build_modern_family_subtitles import decode, digest, normalize_cue_spacing

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'references/subtitles/drama-series-sources.json'
INDEX = ROOT / 'references/subtitles/drama-series-index.json'
NAMES = {'breaking-bad': 'Breaking.Bad', 'better-call-saul': 'Better.Call.Saul',
         'the-big-bang-theory': 'The.Big.Bang.Theory', 'bojack-horseman': 'BoJack.Horseman',
         'horace-and-pete': 'Horace.and.Pete', 'this-is-us': 'This.Is.Us'}


class OriginalCaptions(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth, self.in_paragraph, self.parts, self.captions = 0, False, [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if self.depth:
                self.depth += 1
            elif 'orig-text' in dict(attrs).get('class', '').split():
                self.depth = 1
        if self.depth and tag == 'p':
            self.in_paragraph, self.parts = True, []
        if self.in_paragraph and tag == 'br':
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if self.depth and tag == 'p':
            self.captions.append(''.join(self.parts))
            self.in_paragraph = False
        if tag == 'div' and self.depth:
            self.depth -= 1

    def handle_data(self, text):
        if self.in_paragraph:
            self.parts.append(text)


def recover_english(source):
    """Original English text and same-page parallel SRT; no translation or guessed times."""
    html = (ROOT / 'materials' / source['text_html']).read_bytes()
    parser = OriginalCaptions()
    parser.feed(html.decode('utf-8'))
    timing = (ROOT / 'materials' / source['archive']).read_bytes()
    text, _ = decode(timing)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    pattern = r'(?m)^(\d+)\n(\d\d:\d\d:\d\d,\d{3}\s*-->[^\n]+)\n'
    matches = list(re.finditer(pattern, text))
    rows = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        rows.append((match[1], match[2], bool(text[match.end():end].strip())))
    assert sum(nonempty for _, _, nonempty in rows) == len(parser.captions) == 571
    assert parser.captions[0] == 'Come on, come on, make the--'
    assert parser.captions[-1].startswith('Repair and Synchronization')
    iterator = iter(parser.captions)
    result = '\n\n'.join(f'{number}\n{times}\n{next(iterator) if nonempty else ""}'
                          for number, times, nonempty in rows) + '\n'
    return result.encode('utf-8'), {'reconstruction': '571 original English webpage paragraphs aligned one-to-one with nonempty cues of the same-page Dutch SRT; empty cues preserved; not video-verified',
                                 'text_html': source['text_html'], 'text_html_sha256': digest(html),
                                 'timing_source_sha256': digest(timing)}


def source_members(source):
    path = ROOT / 'materials' / source['archive']
    if source.get('type') == 'reconstructed':
        data, info = recover_english(source)
        yield 'S01E04.recovered.en.srt', data, info
    elif source.get('type') == 'srt':
        yield path.name, path.read_bytes(), {}
    else:
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None, path
            assert sum(i.file_size for i in z.infolist()) < 60_000_000
            for member in sorted(z.namelist()):
                if member.lower().endswith('.srt') and '__MACOSX' not in member:
                    assert z.getinfo(member).file_size < 3_000_000
                    yield member, z.read(member), {}


def identify(member, source):
    if source.get('episodes'):
        return source['season'], source['episodes']
    match = re.search(r's(\d{1,2})e(\d{1,2})(?:(?:e|-e?)(\d{1,2}))?', member, re.I)
    if not match:
        match = re.search(r'(\d{1,2})x(\d{1,2})(?:-(\d{1,2}))?', member, re.I)
    if match:
        assert int(match[1]) == source['season'], member
        return int(match[1]), list(range(int(match[2]), int(match[3] or match[2])+1))
    match = re.match(r'(\d{1,2})[\s._-]', Path(member).name)
    if match:
        return source['season'], [int(match[1])]
    return None


def build():
    jobs = json.loads(SOURCES.read_text())
    titles = {}
    for show in NAMES:
        ref = json.loads((ROOT/'materials/corpus/tv-subtitles'/show/'episode-list.tvmaze.json').read_text())
        titles[show] = {(e['season'],e['number']):e['name'] for e in ref['_embedded']['episodes'] if e['number'] is not None}
    groups, exclusions = collections.defaultdict(list), []
    for source in jobs:
        if source.get('selection') == 'unused':
            continue
        for member, original, info in source_members(source):
            text, encoding = decode(original)
            text = text.replace('\r\n','\n').replace('\r','\n')
            cues = len(re.findall(r'(?m)^\s*\d{1,2}:\d\d:\d\d[,.]\d{3}\s*-->',text))
            identity = identify(member,source)
            if not cues or identity is None or any((identity[0],e) not in titles[source['show']] for e in identity[1]):
                exclusions.append({'archive':source['archive'],'member':member,'reason':'Metadata, recap, or non-regular episode'})
                continue
            season, episodes = identity
            text, repaired = normalize_cue_spacing(text)
            words = re.findall(r'[a-z]+',text.lower())
            common = set('the a an i you he she we they is are was were to of and it that this in for my your me do don not have on'.split())
            ratio = sum(w in common for w in words)/max(len(words),1)
            assert ratio > 0.15, (source['show'],member,'English language screening',ratio)
            hi = bool(re.search(r'(?:^|[._\[\]\s-])(?:hi|sdh)(?:$|[._\[\]\s-])',member,re.I))
            groups[(source['show'],season,tuple(episodes))].append({'source':source,'member':member,'text':text,'encoding':encoding,
                'repaired':repaired,'hi':hi,'ratio':ratio,'original_sha256':digest(original),**info})
    rows, covered, hashes = [], collections.defaultdict(set), set()
    for (show,season,episodes), variants in sorted(groups.items()):
        picked = min(variants,key=lambda x:(not bool(x['source'].get('episodes')),x['hi'],x['member']))
        for v in variants:
            if v is not picked:
                exclusions.append({'archive':v['source']['archive'],'member':v['member'],'reason':'Alternative subtitle version of selected episode'})
        pairs = {(season,e) for e in episodes}
        assert not covered[show]&pairs, (show,pairs)
        covered[show].update(pairs)
        label=f'S{season:02}E{episodes[0]:02}'+(f'-E{episodes[-1]:02}' if len(episodes)>1 else '')
        out=ROOT/'materials/corpus/tv-subtitles'/show/f'S{season:02}'/(NAMES[show]+'.'+label+'.en.srt')
        out.parent.mkdir(exist_ok=True)
        data=picked['text'].encode('utf-8');sha=digest(data);assert sha not in hashes,(show,label,'duplicate file');hashes.add(sha);out.write_bytes(data)
        times=re.findall(r'(?m)^\s*(\d{1,2}):(\d\d):(\d\d)[,.](\d{3})\s*-->',picked['text'])
        starts=[int(h)*3600000+int(m)*60000+int(s)*1000+int(ms) for h,m,s,ms in times]
        src=picked['source'];row={'show':show,'season':season,'episodes':list(episodes),'titles':[titles[show][(season,e)] for e in episodes],
             'file':str(out.relative_to(ROOT)),'bytes':len(data),'sha256':sha,'cues':len(times),'source_encoding':picked['encoding'],
             'removed_blank_lines_inside_cues':picked['repaired'],'timeline_decreases':sum(b<a for a,b in zip(starts,starts[1:])),
             'english_function_word_ratio':round(picked['ratio'],4),'hearing_impaired':picked['hi'],'archive':src['archive'],
             'archive_sha256':digest((ROOT/'materials'/src['archive']).read_bytes()),'archive_member':picked['member'],
             'original_member_sha256':picked['original_sha256'],'url':src['url'],'source_page':src['page'],'release':src['release']}
        for key in ('reconstruction','text_html','text_html_sha256','timing_source_sha256'):
            if key in picked:row[key]=picked[key]
        if 'reconstruction' in row:
            row['derived_source_label'] = row.pop('archive_member')
            row['recovered_srt_sha256'] = row.pop('original_member_sha256')
        rows.append(row)
    for show in NAMES:
        assert covered[show] == set(titles[show]), f'{show} missing {sorted(set(titles[show])-covered[show])}'
    stats={show:{'files':sum(x['show']==show for x in rows),'covered_episodes':len(covered[show]),
                'seasons':dict(sorted(collections.Counter(s for s,e in covered[show]).items())),
                'cues':sum(x['cues'] for x in rows if x['show']==show)} for show in NAMES}
    write_document(INDEX, json.dumps({'date':'2026-10-08','scope':'Regular episodes; no Christmas/behind-the-scenes specials',
          'language':'English','statistics':stats,'episode_metadata_license':'TVmaze CC BY-SA https://www.tvmaze.com/api#licensing',
          'normalization':'UTF-8/LF and blank-line repair; original sources preserved; one explicitly marked recovered English file',
          'files':rows,'excluded_members':exclusions},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(stats,indent=2))
    print('Total files',len(rows),'cues',sum(x['cues'] for x in rows),'timing flags',sum(bool(x['timeline_decreases']) for x in rows))


if __name__=='__main__':
    build()
