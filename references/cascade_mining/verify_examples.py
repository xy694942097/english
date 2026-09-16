#!/usr/bin/env python3
"""例句逐字校验：result_NNN 例句与 batch_NNN 同 id 的 s 精确比对。
零容忍：不一致的例句替换为原句（保留框架，例句以池为准）。"""
import json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent
BD = BASE / "llm_batches"

fixed = 0
total = 0
for rf in sorted(BD.glob("result_*.json")):
    n = rf.stem.split("_")[1]
    bf = BD / f"batch_{n}.json"
    if not bf.exists():
        print(f"{rf.name}: 无对应批次，跳过"); continue
    res = json.loads(rf.read_text(encoding="utf-8"))
    batch = json.loads(bf.read_text(encoding="utf-8"))
    pool = {d["id"]: d["s"] for d in batch["sentences"]}
    mismatches = []
    for sec in ("frames", "candidates"):
        for item in res.get(sec, []):
            for ex in item.get("examples", []):
                total += 1
                if ex["id"] in pool:
                    if ex["text"] != pool[ex["id"]]:
                        mismatches.append((ex["id"], sec, item.get("frame", "?")))
                        ex["text"] = pool[ex["id"]]  # 以池为准，逐字替换
                        fixed += 1
                else:
                    print(f"  ! {rf.name} 例句 id 不在批次池: {ex['id']}")
    if mismatches:
        print(f"{rf.name}: {len(mismatches)} 例不一致，已逐字替换 {[m[0] for m in mismatches]}")
    rf.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"\n校验完成：共 {total} 例句，替换 {fixed} 处（全部以池内原句为准）")
