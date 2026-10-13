"""Render the curated ten-talk TED learning data; no extraction or automatic sense merging."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'references/ted/pilot-10.json'


def render(data, track):
    title = 'TED：Chunks 积累' if track == 'chunks' else 'TED：词汇与搭配积累'
    total = sum(len(t[track]) for t in data['talks'])
    kind = '词块' if track == 'chunks' else '词汇义项'
    lines = [f'# {title}', '',
             f'首批选取10篇TED英文原文，保留{total}个{kind}候选。按原文段落定位，不提供虚构时间码；同词新义或独立接法保留，未标学习者掌握。', '',
             '本批覆盖拖延、沟通、创造力、脆弱与关系、幸福、幽默叙事、AI、对话和毅力。原文与选择目录见[100篇TED目录](<../原文与参考资料/原文、教材与影视/TED 英语选材目录：100 个演讲与对谈.md>)。', '']
    for talk in data['talks']:
        source = talk['source']
        number = source['number']
        lines += [f"## TED {number} · {source['title_zh']}", '',
                  f"{source['speaker']} · {source['year']} · {source['title']}", '']
        for i, item in enumerate(talk[track], 1):
            label = item['chunk'] if track == 'chunks' else item['word']
            meaning = item['meaning']
            if track == 'chunks' and item.get('register'):
                meaning += f"（{item['register']}）"
            elif track == 'vocabulary':
                meaning = item['pos'] + ' ' + meaning
            location = f"P{item['paragraph']:03d}"
            if item.get('end_paragraph', item['paragraph']) != item['paragraph']:
                location += f"–P{item['end_paragraph']:03d}"
            lines += [f'### {i}. {label}', '', f'**意思：** {meaning}', '',
                      '> ' + item['quote'].replace('\n', ' '), '',
                      f"**来源：** [{source['speaker']} · TED {number} · {location}]({source['official_url']})", '']
            if item.get('note'):
                lines += [f"**补充：** {item['note']}", '']
    return '\n'.join(lines).rstrip() + '\n'


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    for track, relative in [('chunks', 'course/Chunks 收集/TED：Chunks 积累.md'),
                            ('vocabulary', 'course/词汇/TED：词汇与搭配积累.md')]:
        path = ROOT / relative
        path.write_text(render(data, track), encoding='utf-8')
        print(relative, sum(len(t[track]) for t in data['talks']))


if __name__ == '__main__':
    main()
