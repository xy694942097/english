#!/usr/bin/env python3
"""人工复筛定版：A 类簇的裁决表。
规则：downgrade=伪框架（词组级/初中已会/骨架弱）；merge=同骨架异名合并；keep=入册。
合并目标与裁决理由以注释记录，可复查可重跑。"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
m = json.loads((BASE / "cascade_frames.json").read_text(encoding="utf-8"))

# ---- 裁决表：frame 名（子串匹配）→ 处置 ----
DOWNGRADE = {
    # 词组级/搭配级——不搭句型，短语档
    "double down": "词组级动词短语",
    "keen to": "形容词搭配，初中后已知",
    "essential to": "介词搭配，初中后已知",
    "be bound to": "情态词组",
    "have trouble/difficulty": "have+n+V-ing 搭配",
    "can/could and should": "并列情态，无骨架",
    "be found / have been shown to": "被动+不定式，语法点",
    "one in [X]": "分母表达，数词结构",
    "differently than": "比较搭配",
    "came/have come to": "come to 渐变，语义弱",
    "the very [N]": "very 强调形容词，词级",
    "all too [Adj/Adv]": "程度副词组",
    "It is (all) too easy to": "too…to 家族，已编07章第2条变体",
    # 初中已会
    "Is [S] not": "否定疑问初中已会",
    "The [second/third/fourth/final] one to avoid": "列举指令变体，语域可疑",
    # 骨架弱
    "[V] that [S V], and that": "that 平行只是并列，无新骨架",
    "[S1], but not [S2], [谓语]": "but not 插入，初中可解",
    "[S V-ed X], but [Y]（but后省略谓语）": "省略承前，熟练度问题",
    "Get [a N], and it’s (the same) as if": "口语祈使+类比，组合",
}
MERGE = {
    # 同骨架异名 → 归并目标（保留目标条，源条 aliases 并入）
    "find oneself / find yourself": "find oneself [V-ing/PP]",  # 双胞胎合并
    "[陈述句], says [来源NP]": "[主句], [S] says/said, [主句续]",  # 引语报道家族
    "[引语], as [身份 NP] puts it": "[主句], [S] says/said, [主句续]",
    "[从句/主语], [人名] told me / found": "[主句], [S] says/said, [主句续]",
    "[主语+谓语前半], [declared": "[主句], [S] says/said, [主句续]",
    "'[引语前半]', [wrote/said]": "[主句], [S] says/said, [主句续]",
    "This/Here is where": "[S] is where [S V]",
    "[前句]. Which is why": "That's why [S V] / Which is why [S V]",
    "This [is/explains] why": "That's why [S V] / Which is why [S V]",
    "One theory is that": "Part of the issue is that",  # 表语从句分项归因家族
    "There is (some) reason/evidence to believe": "There’s (solid/no) evidence that",
    "Contrary to [what S might think": "Contrary to [预期], [主句]",  # 目标需改名
    "[评价], when you consider/look at": "Contrary to [预期], [主句]",
    "[Also/Now] [Adj/V-ed] [时间] is [NP]": "[There will/Now] come(s)",  # 倒装登场家族
    "Rather than [V/V-ing A], [S] [V B]": "Instead of [V-ing], [S V]",
    "As [Adj/much] as [S V], [主句]": "However [Adj]",  # 让步家族
    "in the same way(s) (that)": "the way [S V]",
    "in a way that": "the way [S V]",
    "At a time when": "In a [world/era] where/when",
}

out = []
by_frame = {x["frame"]: x for x in m}
handled = set()
for x in m:
    f = x["frame"]
    if f in handled: continue
    hit_down = next((k for k in DOWNGRADE if k in f), None)
    if hit_down:
        x["status"] = "B"; x["verdict_note"] = DOWNGRADE[hit_down]; out.append(x); continue
    hit_merge = next((k for k in MERGE if k in f), None)
    if hit_merge:
        tgt_name = MERGE[hit_merge]
        tgt = by_frame.get(tgt_name)
        if tgt is None:
            # 目标不存在（需建新目标或目标本身在列表中稍后处理）——暂存，目标出现后并入
            x["_merge_into"] = tgt_name; out.append(x); continue
        # 把本条并入目标
        tgt.setdefault("aliases", []).append(f)
        tgt.setdefault("examples", []).extend(x.get("examples", []))
        tgt["examples"] = tgt["examples"][:8]
        handled.add(f)
        continue
    out.append(x)

# 二次处理：暂存的合并进新目标名（若目标未出现则升级自身为目标改名）
final = []
merged_targets = {x["frame"] for x in out}
for x in out:
    if "_merge_into" in x:
        tgt_name = x.pop("_merge_into")
        tgt = next((y for y in out if y["frame"] == tgt_name), None)
        if tgt is None:
            # 无既存目标：本条改名为目标名
            x["aliases"] = x.get("aliases", []); old = x["frame"]; x["frame"] = tgt_name
            x.setdefault("aliases", []).append(old)
            final.append(x)
        else:
            tgt.setdefault("aliases", []).append(x["frame"])
            tgt.setdefault("examples", []).extend(x.get("examples", []))
            tgt["examples"] = tgt["examples"][:8]
    else:
        final.append(x)

# 去重例句（同 id 只留一次）
for x in final:
    seen, exs = set(), []
    for e in x.get("examples", []):
        if e.get("id") not in seen:
            seen.add(e.get("id")); exs.append(e)
    x["examples"] = exs[:8]

(BASE / "cascade_final.json").write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
c = Counter((x["level"], x["status"]) for x in final)
print("复筛后：", dict(c))
A = [x for x in final if x["status"] == "A"]
for lv in ("cet4", "cet6", "kaoyan"):
    n = sum(1 for x in A if x["level"] == lv)
    print(f"  {lv}: A类 {n}")
print("降级 B:", sum(1 for x in final if x["status"] == "B"))
