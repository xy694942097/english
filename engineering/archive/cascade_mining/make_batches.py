#!/usr/bin/env python3
"""切批：分级别 300 句一批，写入 llm_batches/。级联提示词附已有清单。"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
BATCH = 300

order = ["cet4", "cet6", "kaoyan"]  # 级联顺序：低级在前
pools = {}
for lv in order:
    pools[lv] = json.load(open(BASE / f"pools/{lv}.json"))

seed = json.load(open(BASE / "registry_seed.json"))
seed_names = sorted(set(r["frame"] for r in seed if not r["frame"].startswith("[")) | set(r["frame"] for r in seed))

n = 0
for lv in order:
    for i in range(0, len(pools[lv]), BATCH):
        n += 1
        batch = pools[lv][i:i+BATCH]
        out = {"batch": f"{n:03d}", "level": lv, "range": [i, i+len(batch)],
               "known_frames": seed_names,
               "sentences": batch}
        (BASE / "llm_batches" / f"batch_{n:03d}.json").write_text(
            json.dumps(out, ensure_ascii=False), encoding="utf-8")
        print(f"batch_{n:03d}: {lv} [{i}:{i+len(batch)}]")
print(f"共 {n} 批")
