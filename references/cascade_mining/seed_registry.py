#!/usr/bin/env python3
"""全局框架登记表种子：已编章节框架 + 雅思A类簇 + 本对话人工候选。
用途：级联挖掘去重基准——低级已提取的，高级不再提取。"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = Path(__file__).resolve().parent / "registry_seed.json"

registry = []

# 1) 已编章节：## N. 框架名
CHAPTERS = {
    "book/08-frames/01-degree-comparison.md": ("中学", "01"),
    "book/08-frames/02-emphasis-focus.md": ("中学", "02"),
    "book/08-frames/03-concession-contrast.md": ("中学", "03"),
    "book/08-frames/04-stance-commentary.md": ("中学", "04"),
    "book/08-frames/05-narrative-logic.md": ("中学", "05"),
    "book/08-frames/06-condition-subjunctive.md": ("中学", "06"),
    "book/08-frames/07-school-recall.md": ("中学", "07"),
    "book/08-frames/09-exam-recall.md": ("四级六级考研", "09"),
    "book/08-frames/12-readthrough-recall.md": ("中学", "12"),
}
for path, (lv, ch) in CHAPTERS.items():
    for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## \d+\. (.+)$", line.strip())
        if m:
            name = re.sub(r"（.*?）", "", m.group(1)).strip()
            registry.append({"frame": name, "level": lv, "src": f"已编{ch}章"})

# 2) 雅思 A 类簇
cl = json.load(open(ROOT / "references/ielts_mining/frames_clustered.json"))
for c in (cl if isinstance(cl, list) else cl.get("clusters", cl.get("frames", []))):
    lvl = c.get("level", "")
    if lvl.startswith("A"):
        registry.append({"frame": c.get("frame") or c.get("name"), "level": "雅思", "src": "雅思挖掘A类"})

# 3) 本对话人工候选（frame-miner 对拆产出）
manual = [
    ("there's no such thing as [N]", "四级"), ("Gone are the days of/when", "四级"),
    ("If [S] is to [V]", "四级"), ("lead [sb] to believe that", "四级"),
    ("rather than + V-ing + 祈使句（与其A不如B）", "四级"),
    ("Take [N].（拿…来说）", "六级"), ("To the [情感N] of [sb]", "六级"),
    ("You hear that [S V]（立靶-引语版）", "六级"),
    ("But is there a cost to X instead of Y?（立靶-设问版）", "六级"),
    ("[A组] than those who did(n't)（对照回指）", "六级"),
    ("[A] was once [B]. Now [C]", "六级"),
    ("not so much [A] as [B]", "考研"), ("Just as [A], so [B]", "考研"),
    ("What [NP], what [NP], would not [V]?", "考研"),
    ("By the time [完成体], [may have done]", "考研"),
    ("[N], or [同位语], [谓语]", "考研"),
    ("hold [sb] accountable for", "短语"), ("at the expense of", "短语"),
    ("be under investigation for", "短语"), ("put a premium on", "短语"),
    ("the makeup of", "短语"), ("to the disadvantage of", "短语"),
    ("convert [A] to/into [B]", "短语"), ("the cost to [V-ing]", "短语"),
    ("hang onto", "短语"),
]
for f, lv in manual:
    registry.append({"frame": f, "level": lv, "src": "对话对拆"})

OUT.write_text(json.dumps(registry, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"登记表种子：{len(registry)} 条")
print(f"  其中雅思A类 {sum(1 for r in registry if r['src']=='雅思挖掘A类')} 条")
