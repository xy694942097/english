"""Normalize downloaded GovInfo HTML; verify curated quotations; build reading view."""
import json
import re
from html.parser import HTMLParser
from html import unescape
from pathlib import Path
from document_paths import write_document

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'references/presidential-speeches'
RAW = ROOT / 'materials/corpus/presidential-speeches/govinfo'
OUT = ROOT / 'course/原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md'


def source_url(src):
    return src.get('url', f"https://www.govinfo.gov/content/pkg/{src['id']}/html/{src['id']}.htm")


def read_rows(src):
    text = (RAW / f"{src['id']}.htm").read_text(encoding='utf-8')
    if 'Page Not Found' in text:
        raise ValueError(f"Error page: {src['id']}")
    if src.get('format') == 'pre':
        # Older PPP text uses indentation for paragraphs and markers inside them.
        plain = unescape(re.sub(r'<[^>]+>', '', text.split('<pre>', 1)[1].split('</pre>', 1)[0]))
        plain = re.sub(r'\n*\[\[Page [^\]]+\]\]\n*', '\n', plain)
        rows, buffer = [], []
        for line in plain.splitlines():
            if (line.startswith('    ') or re.match(r'^Note:', line, re.I)) and buffer:
                rows.append(' '.join(buffer))
                buffer = []
            if line.strip():
                buffer.append(line.strip())
        if buffer:
            rows.append(' '.join(buffer))
    else:
        parser = Paragraphs()
        parser.feed(text)
        rows = parser.rows
    start = next(i for i, row in enumerate(rows) if row.startswith(src['start']))
    end = next((i for i in range(start, len(rows)) if re.match(r'^N\s*OTE\s*:', rows[i], re.I)), len(rows))
    result = [r for r in rows[start:end] if not re.fullmatch(r'\d+', r)]
    if not result or any(r.startswith(('Categories:', 'Subjects:', 'DCPD Number:')) for r in result):
        raise ValueError(f"Invalid speech boundary: {src['id']}")
    return result


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.body = False
        self.tag = None
        self.buffer = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body = True
        if self.body and tag in ('p', 'h1', 'h2', 'h3'):
            self.tag, self.buffer = tag, []
        if self.tag and tag == 'br':
            self.buffer.append(' ')

    def handle_data(self, value):
        if self.tag:
            self.buffer.append(value)

    def handle_endtag(self, tag):
        if tag == self.tag:
            value = re.sub(r'\s+', ' ', ''.join(self.buffer)).strip()
            if value:
                self.rows.append(value)
            self.tag = None



def render_chunks(sources, selection):
    """Render curated chunks by speech; discovery/dedup remain editorial work."""
    from collections import defaultdict
    groups = defaultdict(list)
    for chunk in selection['chunks']:
        groups[chunk['source_id']].append(chunk)
    speakers = ['Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump', 'Joe Biden']
    ordered = sorted(sources, key=lambda src: (speakers.index(src['speaker']), src['date']))
    lines = ['# 总统演讲：Chunks 积累', '',
             f"取自五位总统的 {len(groups)} 篇官方实录，按演讲分组。记录可迁移的搭配、话语套语和整句表达；正式与演讲语气标在意思中，不把出现次数当作日常高频或掌握证据。", '',
             '原文见 [总统演讲原文合集](../原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md)。以下是候选积累；段号对应本地可读层，原句逐字保留。', '']
    for src in ordered:
        if src['id'] not in groups:
            continue
        lines += [f"## {src['date']} · {src['label']}", '']
        for i, chunk in enumerate(sorted(groups[src['id']], key=lambda x: x['paragraph']), 1):
            location = f"P{chunk['paragraph']:03d}"
            if chunk.get('end_paragraph', chunk['paragraph']) != chunk['paragraph']:
                location += f"–P{chunk['end_paragraph']:03d}"
            register = chunk.get('register', '')
            lines += [f"### {i}. {chunk['chunk']}", '',
                      f"**意思：** {chunk['meaning']}" + (f"（{register}）" if register else ''), '',
                      '> ' + chunk['quote'].replace('\n', ' '), '',
                      f"**来源：** [{src['speaker']} · {location}]({source_url(src)})", '']
            if chunk.get('note'):
                lines += [f"**补充：** {chunk['note']}", '']
            if chunk.get('transfer'):
                lines += [f"> {chunk['transfer']}（教学自造）", '']
    return '\n'.join(lines).rstrip() + '\n'


def main():
    sources = json.loads((META / 'sources.json').read_text())
    speeches = {}
    lines = ['# 总统演讲原文合集：GovInfo', '',
             '官方 HTML 的本地可读层；解码 HTML 实体、合并排版空白，并去除旧版 PPP 的页码标记，保留口误、重复和观众反应。段号是本地段落编号，不是官方 PDF 页码。', '',
             '来源和原件哈希见 `materials/downloads-manifest.json`；可重跑 `python3 references/build_presidential_speeches.py`。', '']
    lines += ['## 演讲索引', '', '| 总统 | 日期 | 演讲 | 官方编号 |', '|---|---|---|---|']
    ordered = sorted(sources, key=lambda s: (['Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump', 'Joe Biden'].index(s['speaker']), s['date']))
    for src in ordered:
        lines.append(f"| {src['label'].split('：', 1)[0]} | {src['date']} | [{src['label']}]({source_url(src)}) | {src['id']} |")
    lines += ['', '索引中的日期为演讲／播出日期，可能与档案卷册年份或实录发布日期不同。每周讲话若预录，录制日另见 TXT 页首。原文可用于学习表达，尚未逐篇提取 chunks。', '']
    for src in ordered:
        rows = read_rows(src)
        speeches[src['id']] = rows
        url = source_url(src)
        header = [
            '[资料信息 / Source information]',
            f"总统 / President: {src['speaker']}（{src['label'].split('：', 1)[0]}）",
            f"演讲日期 / Speech date: {src['date']}",
            *([f"录制日期 / Recorded date: {src['recorded_date']}"] if src.get('recorded_date') else []),
            f"演讲名称: {src['label']}",
            f"官方标题 / Official title: {src['title']}",
            f"文档编号 / Document ID: {src['id']}",
            f"官方原文 / Source: {url}",
            '说明：以上为本项目添加的资料信息；以下正文来自官方 HTML，保留口误、重复与观众反应。',
            '',
            '[演讲正文 / Speech text]',
            '',
        ]
        write_document(RAW / f"{src['id']}.txt", '\n'.join(header) + '\n\n'.join(rows) + '\n', encoding='utf-8')
        lines += [f"## {src['date']} · {src['label']}", '', f"{src['speaker']} · [{src['title']}]({url}) · {src['id']}", '']
        lines += [f'**P{i:03d}.** {row}\n' for i, row in enumerate(rows, 1)]
        print(src['id'], len(rows), 'paragraphs', len(' '.join(rows).split()), 'words')
    chunks_path = META / 'chunks.json'
    if chunks_path.exists():
        selection = json.loads(chunks_path.read_text())
        chunks = selection['chunks']
        for chunk in chunks:
            paragraph = ' '.join(speeches[chunk['source_id']][chunk['paragraph'] - 1:chunk.get('end_paragraph', chunk['paragraph'])])
            if chunk['quote'] not in paragraph:
                raise ValueError(f"Quotation mismatch: {chunk['chunk']}")
        print('verified', len(chunks), 'verbatim quotations')
        report = render_chunks(sources, selection)
        (ROOT / 'course/Chunks 收集/总统演讲：Chunks 积累.md').write_text(report, encoding='utf-8')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_document(OUT, '\n'.join(lines).rstrip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
