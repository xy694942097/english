#!/usr/bin/env python3
"""将 book/08-frames/ 的 01-07 章合并为单篇总集文档（排版保持紧凑学习卡风格）。

用法: python3 build_frames_collection.py
输出: book/08-frames/08-frames-collection.md（同时挂进 course.json 导航）
"""

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "book" / "08-frames"

CHAPTERS = [
    ("01-degree-comparison.md", "家族A · 程度与比较", "表达“超出预期”“与其说A不如说B”这类评价"),
    ("02-emphasis-focus.md", "家族B · 强调与聚焦", "读长句时抓住作者到底在强调什么（诊断句原生家族）"),
    ("03-concession-contrast.md", "家族C · 让步与对照", "让步—转折的语气力度，反驳不止 although"),
    ("04-stance-commentary.md", "家族D · 评述与立场", "句子之外的作者态度信号"),
    ("05-narrative-logic.md", "家族E · 叙事与逻辑推进", "复盘、postmortem 的因果推进骨架"),
    ("06-condition-subjunctive.md", "家族F · 条件与虚拟", "技术文档与正式邮件的省 if 结构"),
    ("07-school-recall.md", "教材回收 · 初高中句式骨架", "初中五册+高中人教句库扫描与课标项目回收的合成章，例句带册别出处"),
    ("09-exam-recall.md", "真题回收 · 四六级考研句式", "9 份真题试卷里反复出现、教材没当句式骨架教的句式骨架"),
    ("12-readthrough-recall.md", "教材回收 · 通读篇", "LLM 逐句通读挖出的无钩子词结构型句式骨架，regex 扫不出来的那批"),
    ("13-cet4-readthrough.md", "真题通读 · 四级篇", "四级 7 份真题逐句通读：29 个句式骨架 + 短语档（anything but、Gone are the days、at best、Who says、just because doesn't mean 等）"),
    ("14-cet6-readthrough.md", "真题通读 · 六级篇", "六级 48 份真题逐句通读：66 个句式骨架 + 短语档（evidence that、Of 前置分母、双破折号插入、find oneself、It's simply not true that、anything but、However [Adj] 让步、Thus was born、known as 命名同位等）"),
    ("15-kaoyan-readthrough.md", "真题通读 · 考研篇", "考研真题+精翻逐句通读：60 个句式骨架 + 短语档（never to、not enough to say、It's not as if、being what it is、has it that、can't afford not to、It is all very well…but 等）"),
    ("16-oral-dialogue-actions.md", "小说通读 · 口语对话动作", "《Normal People》全书通读：23 个口语对话句式骨架（It's not like/Not that/How was I supposed to know/not really 等），攻防与体面的表达动作"),
    ("17-narrative-cognition-actions.md", "小说通读 · 叙事与认知动作", "《Normal People》全书通读：18 个叙事句式骨架（only to 反转、Later would 回望、without ever 归零、To his relief 注脚等），讲故事的发动机"),
    ("18-self-picked.md", "自选篇 · 手动收录", "日常阅读/影视/对话中撞见即收的活页章：less about…and more about 重新定焦等，不设 7 条红线"),
]


def demote(body: str) -> str:
    """章内标题降一级：# -> ##，## -> ###，依此类推（只处理 # 标题行，不动代码块内内容）。"""
    out, in_code = [], False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if not in_code and re.match(r"^#{1,5} ", line):
            out.append("#" + line)
        else:
            out.append(line)
    return "\n".join(out)


def main():
    today = date.today().isoformat()
    toc_lines = []
    parts = []
    for filename, title, solves in CHAPTERS:
        path = FRAMES / filename
        if not path.is_file():
            raise SystemExit(f"缺少章节文件: {path}")
        body = path.read_text(encoding="utf-8").strip()
        # 去掉章内的一级标题（总集里由分节标题替代）
        body = re.sub(r"^# .*\n+", "", body, count=1)
        sections = re.findall(r"^## (.+)$", demote(body), re.M)
        anchor = title
        toc_lines.append(f"[{title}](#{anchor.replace(' ', '-').replace('·', '').replace('（', '').replace('）', '')}) — {solves}")
        part = f"\n---\n\n# {title}\n\n{demote(body)}\n"
        parts.append(part)

    header = f"""# 句式骨架总集：六大家族与教材回收

> 单篇合集，供通读与打印。分章学习仍推荐用各家族独立章（含课程导航与练习折叠）。合成日期：{today}。标注约定全文一致：例句后标（语料）为词典例句库真实例句，标（自造）为教学自造。

## 总目录

{chr(10).join(toc_lines)}
"""
    output = FRAMES / "08-frames-collection.md"
    output.write_text(header + "\n".join(parts), encoding="utf-8")

    # 挂进课程导航（家族F之后、样张之前）
    course_path = ROOT / "book" / "course.json"
    course = json.loads(course_path.read_text(encoding="utf-8"))
    entry = {
        "path": "book/08-frames/08-frames-collection.md",
        "title": "总集：六大家族与教材回收（单篇通读版）",
        "focus": "A-F 六家族 31 句式骨架 + 教材回收 9 句式骨架的单篇合集，适合通读与打印；分章学习仍用独立章。",
        "level": "通读",
    }
    for topic in course["topics"]:
        if topic["id"] == "frames":
            if not any(l["path"] == entry["path"] for l in topic["lessons"]):
                idx = next((i for i, l in enumerate(topic["lessons"]) if "[样张]" in l["title"]), len(topic["lessons"]))
                topic["lessons"].insert(idx, entry)
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成 {output} 并挂入课程导航")


if __name__ == "__main__":
    main()
