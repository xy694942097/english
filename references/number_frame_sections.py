#!/usr/bin/env python3
"""给框架章节的框架节标题加序号（## X. 框架名），按 TEMPLATE.md 规范。

规则：每章内 ## 节标题，除"迁移练习"“参考答案”等非框架节外，从 1 连续编号。
用法: python3 number_frame_sections.py  # 处理 01-07 章
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "book" / "08-frames"
CHAPTERS = [
    "01-degree-comparison.md", "02-emphasis-focus.md", "03-concession-contrast.md",
    "04-stance-commentary.md", "05-narrative-logic.md", "06-condition-subjunctive.md",
    "07-school-recall.md", "09-exam-recall.md",
    "10-junior-recall.md", "11-senior-recall.md",
]
SKIP = ("迁移练习", "参考答案", "新语境练习", "练习", "总目录", "本章预览")

for name in CHAPTERS:
    path = FRAMES / name
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    out, in_code, n = [], False, 0
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        m = re.match(r"^## (.+)$", line) if not in_code else None
        if m:
            title = m.group(1).strip()
            # 幂等：已编号标题先去掉旧编号，避免叠加
            title = re.sub(r"^\d+\.\s+", "", title)
            if any(k in title for k in SKIP):
                out.append(line)
                continue
            n += 1
            out.append(f"## {n}. {title}")
        else:
            out.append(line)
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"{name}: 编号 {n} 个框架节")
