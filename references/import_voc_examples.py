#!/usr/bin/env python3
"""Import zhenghaoyang24/english-vocabulary example sentences into the combined dictionary.

数据来源: https://github.com/zhenghaoyang24/english-vocabulary (tb_voc_examples.json + tb_vocabulary.json)
约定: 例句按 headword(单词拼写) 关联入库, source_collection='voc14w', 记录导入报告。
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "materials" / "vocabulary" / "zhenghaoyang24-voc"
DEFAULT_DB = ROOT / "data" / "combined_dictionary.sqlite3"
REPORT_DIR = ROOT / "references" / "imports" / "2026-09-16-voc-examples"


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--limit", type=int, default=0, help="调试用：只导入前 N 条")
    args = ap.parse_args()

    examples_path = DOWNLOADS / "tb_voc_examples.json"
    vocab_path = DOWNLOADS / "tb_vocabulary.json"
    for p in (examples_path, vocab_path):
        if not p.is_file():
            sys.exit(f"缺少数据文件: {p}（先按 references/README.md 下载）")

    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    wordmap = {v["wordid"]: v.get("spelling", "").strip().lower() for v in vocab}

    examples = json.loads(examples_path.read_text(encoding="utf-8"))
    if args.limit:
        examples = examples[: args.limit]

    db = sqlite3.connect(args.db)
    cur = db.cursor()
    inserted = skipped_no_word = duplicates = 0
    batch = []
    seen = set()
    for row in examples:
        spelling = wordmap.get(row.get("wordid"))
        english = (row.get("en") or "").strip()
        chinese = (row.get("cn") or "").strip()
        if not spelling or not english:
            skipped_no_word += 1
            continue
        key = (spelling, english, chinese)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        batch.append((spelling, english, chinese, "voc14w", "voc_examples heat=%s" % row.get("heat", 0)))
        if len(batch) >= 5000:
            cur.executemany(
                "INSERT OR IGNORE INTO examples(headword,english,chinese,source_collection,source) VALUES(?,?,?,?,?)",
                batch,
            )
            inserted += cur.rowcount
            batch = []
    if batch:
        cur.executemany(
            "INSERT OR IGNORE INTO examples(headword,english,chinese,source_collection,source) VALUES(?,?,?,?,?)",
            batch,
        )
        inserted += cur.rowcount
    db.commit()

    total = cur.execute("SELECT COUNT(*) FROM examples WHERE source_collection='voc14w'").fetchone()[0]
    db.close()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "built_at": now(),
        "source": "https://github.com/zhenghaoyang24/english-vocabulary (master)",
        "files": {"examples": examples_path.name, "vocab": vocab_path.name},
        "source_examples": len(examples),
        "inserted": inserted,
        "already_in_db_total": total,
        "skipped_no_word": skipped_no_word,
        "duplicates_in_file": duplicates,
    }
    (REPORT_DIR / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
