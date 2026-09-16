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
    ("07-school-recall.md", "教材回收 · 初高中成对结构", "当年当语法点背的成对结构，升级为预制件"),
    ("09-exam-recall.md", "真题回收 · 四六级考研句式", "9 份真题试卷里反复出现、教材没当框架教的句式骨架"),
    ("10-junior-recall.md", "教材回收 · 初中篇", "从人教版初中五册全文里扫出的高频句式框架，例句全部取自教材原文"),
    ("11-senior-recall.md", "教材回收 · 高中篇", "从人教版 2019 高中教材句子库里扫出的句式框架，例句全部带册别出处"),
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

    header = f"""# 句式框架总集：六大家族与教材回收

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
        "focus": "A-F 六家族 31 框架 + 教材回收 9 框架的单篇合集，适合通读与打印；分章学习仍用独立章。",
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
