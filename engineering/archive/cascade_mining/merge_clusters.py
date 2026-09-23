#!/usr/bin/env python3
"""跨级合并聚类：14 批 result → 全局框架登记表。
级联规则：同一框架按发现级别归位（四级<六级<考研），低级已提取的高级不重复。
聚类：按骨架相似度程序归并 + 人工核验接口（输出 suggested_merge 供人裁）。"""
import json, re
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent
BD = BASE / "llm_batches"

LEVEL_ORDER = {"cet4": 1, "cet6": 2, "kaoyan": 3}

def norm(f):
    """骨架签名：去槽位标记/方括号/空格，小写，只留死词链。"""
    s = f.lower()
    s = re.sub(r"\[[^\]]*\]", "()", s)   # 槽位→()
    s = re.sub(r"[^a-z().!?'—-]", "", s)
    return s

def key_of(f):
    """聚类键：槽位间最长的连续死词串。"""
    s = norm(f)
    words = re.findall(r"[a-z'.!?—-]+", s)
    words = [w for w in words if w not in ("", ".", "!")]
    return max(words, key=len) if words else norm(f)

raw = []
for rf in sorted(BD.glob("result_*.json"), key=lambda p: int(p.stem.split("_")[1])):
    n = int(rf.stem.split("_")[1])
    batch = json.loads((BD / f"batch_{n:03d}.json").read_text(encoding="utf-8"))
    lv = batch["level"]
    res = json.loads(rf.read_text(encoding="utf-8"))
    for item in res.get("frames", []):
        raw.append({"frame": item["frame"], "gloss": item.get("gloss", ""),
                    "notes": item.get("notes", ""), "related": item.get("related"),
                    "examples": item["examples"], "level": lv, "batch": n,
                    "status": "A"})
    for item in res.get("candidates", []):
        if isinstance(item, str):
            raw.append({"frame": item, "gloss": "", "notes": "单例候选", "related": None,
                        "examples": [], "level": lv, "batch": n, "status": "candidate"})
        else:
            raw.append({"frame": item.get("frame", "?"), "gloss": item.get("gloss", ""),
                        "notes": item.get("notes", ""), "related": item.get("related"),
                        "examples": item.get("examples", []), "level": lv, "batch": n,
                        "status": "candidate"})

# 聚类：按 key 分桶
buckets = defaultdict(list)
for r in raw:
    buckets[key_of(r["frame"])].append(r)

merged = []
for k, group in buckets.items():
    if len(group) == 1:
        merged.append(group[0]); continue
    # 同键多成员：按级别排序，最低级为主位，其余作 aliases
    group.sort(key=lambda r: LEVEL_ORDER.get(r["level"], 9))
    main = dict(group[0])
    main["aliases"] = sorted(set(g["frame"] for g in group[1:]))
    main["levels_seen"] = sorted(set(g["level"] for g in group))
    # 合并例句（去重，限8）
    exs, seen = [], set()
    for g in group:
        for e in g.get("examples", []):
            if e.get("id") not in seen:
                seen.add(e.get("id")); exs.append(e)
    main["examples"] = exs[:8]
    main["status"] = "A" if any(g["status"] == "A" for g in group) else "candidate"
    if len(group) > 1 and main["status"] == "A":
        main["multi_batch"] = sorted(set(g["batch"] for g in group))
    merged.append(main)

# 级联去重对照种子：A 类框架若与种子同帧（签名级），标 seed_hit
seed = {norm(r["frame"]) for r in json.load(open(BASE / "registry_seed.json"))}
for m in merged:
    if norm(m["frame"]) in seed:
        m["seed_hit"] = True

out = BASE / "cascade_frames.json"
out.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")

# 汇总
from collections import Counter
c = Counter(m["level"] for m in merged)
print(f"原始产出：{len(raw)} 条（A {sum(1 for r in raw if r['status']=='A')} / 候选 {sum(1 for r in raw if r['status']=='candidate')}）")
print(f"聚类合并：{len(merged)} 簇")
for lv in ("cet4", "cet6", "kaoyan"):
    ms = [m for m in merged if m["level"] == lv]
    print(f"  {lv}: {len(ms)} 簇（A类 {sum(1 for m in ms if m['status']=='A')}）")
print(f"撞种子（已编/已知，级联剔除）: {sum(1 for m in merged if m.get('seed_hit'))}")
