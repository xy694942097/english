#!/usr/bin/env python3
"""为句式骨架分章生成章首预览表（按 TEMPLATE.md 规范）。

表来源：每章 "## N. 句式骨架名" 节标题 + 节内第一处 "**语义：**…**" 定义句。
幂等：已有 "## 本章预览" 节则先删除再重建。表放在章首说明段之后、第一个句式骨架节之前。

用法: python3 build_chapter_previews.py
"""

import re
from pathlib import Path
from document_paths import document_path

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "book" / "08-frames"
CHAPTERS = [
    "01-degree-comparison.md", "02-emphasis-focus.md", "03-concession-contrast.md",
    "04-stance-commentary.md", "05-narrative-logic.md", "06-condition-subjunctive.md",
    "07-school-recall.md", "09-exam-recall.md", "12-readthrough-recall.md",
    "13-cet4-readthrough.md", "14-cet6-readthrough.md", "15-kaoyan-readthrough.md",
    "16-oral-dialogue-actions.md", "17-narrative-cognition-actions.md", "18-self-picked.md",
]


def extract_semantics(body: str) -> dict:
    """返回 {序号: (句式骨架名, 一句话语义)}。"""
    result = {}
    lines = body.split("\n")
    in_code = False
    current = None
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            current = int(m.group(1))
            result[current] = (m.group(2).strip(), "")
            continue
        if current is not None and result[current][1] == "":
            sm = re.search(r"\*\*语义：(.+?)\*\*", line)
            if sm:
                text = sm.group(1).strip().rstrip("。**")
                result[current] = (result[current][0], text)
    return result


for name in CHAPTERS:
    path = document_path("book/08-frames/" + name)
    text = path.read_text(encoding="utf-8")

    # 幂等：删除已存在的预览节（表头列名兼容 框架/句式骨架 两种措辞）
    text = re.sub(r"\n## 本章预览\n\n\| 编号 \| (?:框架|句式骨架) \| 一句话语义 \|\n\|---\|---\|---\|\n(?:\| \d+ \|.*\n)+\n", "\n", text)
    text = re.sub(r"\n## 本章预览\n[\s\S]*?(?=\n## )", "\n", text)

    entries = extract_semantics(text)
    if not entries:
        print(f"{name}: 无编号句式骨架节，跳过")
        continue

    rows = ["| 编号 | 句式骨架 | 一句话语义 |", "|---|---|---|"]
    for n in sorted(entries):
        title, sem = entries[n]
        rows.append(f"| {n} | {title} | {sem or '（见节内）'} |")
    preview = "## 本章预览\n\n" + "\n".join(rows) + "\n"

    # 插入位置：第一个 "### " 分节标题或 "## N. " 句式骨架节（取更靠前者）之前
    m = re.search(r"^(?:### .+|## \d+\. )", text, re.M)
    if not m:
        print(f"{name}: 找不到插入点，跳过")
        continue
    text = text[: m.start()] + preview + "\n" + text[m.start():]
    path.write_text(text, encoding="utf-8")
    print(f"{name}: 预览表 {len(entries)} 行")
