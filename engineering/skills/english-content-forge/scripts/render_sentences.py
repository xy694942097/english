#!/usr/bin/env python3
"""render_sentences.py — 句集数据 → 两种 markdown 视图 + 一致性自检

用法:
    python render_sentences.py data.jsonl -o outdir/

输入: JSONL, 每行六个字段:
    id, category, en, cn, hard_phrases, pattern_note

输出:
    <stem>-v1.md  交错版 (句子紧跟解析锚点链接)
    <stem>-v2.md  分组版 (句子区/解析区分两大 Part)

自检 (任一失败则不产出文件, exit 1):
    - 字段齐全且非空
    - id 连续、不重复
    - 两视图句数 == 数据行数 (结构上必然, 但仍显式断言)
    - en 长度 >= 15 字符 (防残句)
    - en 去重
"""
import json
import sys
import argparse
from pathlib import Path

REQUIRED = ("id", "category", "en", "cn", "hard_phrases", "pattern_note")


def load_and_validate(jsonl_path: Path) -> list[dict]:
    rows = []
    errors = []
    seen_ids = set()
    seen_en = {}
    with open(jsonl_path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"行 {lineno}: JSON 解析失败 {e}")
                continue
            for k in REQUIRED:
                v = row.get(k)
                if v is None or (isinstance(v, str) and not v.strip()):
                    errors.append(f"行 {lineno} (id={row.get('id')}): 字段 {k} 缺失或为空")
            rid = row.get("id")
            if rid in seen_ids:
                errors.append(f"行 {lineno}: id {rid} 重复")
            seen_ids.add(rid)
            en = (row.get("en") or "").strip()
            if len(en) < 15:
                errors.append(f"行 {lineno} (id={rid}): en 过短 ({len(en)} 字符), 疑似残句: {en!r}")
            if en and en.lower() in seen_en:
                errors.append(f"行 {lineno} (id={rid}): en 与 id={seen_en[en.lower()]} 重复")
            if en:
                seen_en[en.lower()] = rid
            rows.append(row)

    ids = [r.get("id") for r in rows if r.get("id") is not None]
    if ids and sorted(ids) != list(range(min(ids), min(ids) + len(ids))):
        expected = sorted(ids)
        missing = set(range(min(ids), min(ids) + len(ids))) - set(ids)
        errors.append(f"id 不连续, 缺失: {sorted(missing)}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        raise SystemExit(f"自检未通过 ({len(errors)} 处), 未渲染任何文件")
    return rows


def render_v1(rows: list[dict]) -> str:
    parts = ["### Part 1 - Sentences\n"]
    for r in rows:
        parts.append(
            f"#### {r['id']}. [{r['category']}]\n\n"
            f'<a id="s{r["id"]}"></a>\n\n'
            f'> *"{r['en']}"*\n'
            f'> [[解析 →](#a{r["id"]})]\n'
        )
    parts.append("\n### Part 2 - Analysis\n")
    for r in rows:
        parts.append(
            f"#### Analysis {r['id']}\n\n"
            f'<a id="a{r["id"]}"></a>\n'
            f'[[← 回到句子](#s{r["id"]})]\n\n'
            f"- **难词/短语**：{r['hard_phrases']}\n"
            f"- **句式分析**：{r['pattern_note']}\n"
            f"- **中文意思**：{r['cn']}\n"
        )
    return "\n".join(parts)


def render_v2(rows: list[dict]) -> str:
    cats: dict[str, list[dict]] = {}
    for r in rows:
        cats.setdefault(r["category"], []).append(r)
    ordered = sorted(cats.items(), key=lambda kv: min(x["id"] for x in kv[1]))

    parts = ["### Part 1 - 句子\n"]
    for cat, items in ordered:
        lines = [f"#### {cat}句子\n"]
        for r in items:
            lines.append(f'**{r["id"]}.** *"{r["en"]}"*\n')
        parts.append("\n".join(lines))

    parts.append("\n### Part 2 - 解析\n")
    for cat, items in ordered:
        lines = [f"#### {cat}解析\n"]
        for r in items:
            lines.append(
                f"**{r['id']}.** {r['cn']}\n"
                f"- 难词/短语：{r['hard_phrases']}\n"
                f"- 句式分析：{r['pattern_note']}\n"
            )
        parts.append("\n".join(lines))
    return "\n\n---\n\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data", type=Path, help="data.jsonl 路径")
    ap.add_argument("-o", "--outdir", type=Path, default=Path("."), help="输出目录")
    args = ap.parse_args()

    rows = load_and_validate(args.data)
    stem = args.data.stem
    args.outdir.mkdir(parents=True, exist_ok=True)

    v1 = render_v1(rows)
    v2 = render_v2(rows)

    # 视图级断言: 两种排版中的句子数必须都等于数据行数
    n = len(rows)
    assert v1.count("[解析 →]") == n, "v1 解析链接数与数据不符"
    assert v1.count("[[← 回到句子]") == n, "v1 回链数与数据不符"
    assert v2.count('*"') >= n, "v2 句子数不足"

    (args.outdir / f"{stem}-v1.md").write_text(v1, encoding="utf-8")
    (args.outdir / f"{stem}-v2.md").write_text(v2, encoding="utf-8")

    cats = {}
    for r in rows:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    dist = ", ".join(f"{c}×{k}" for c, k in sorted(cats.items(), key=lambda kv: -kv[1]))
    print(f"OK: {n} 句 | 分布: {dist}")
    print(f"OK: 两视图句数一致 ({n} == {n})")
    print(f"产出: {args.outdir / (stem + '-v1.md')}")
    print(f"产出: {args.outdir / (stem + '-v2.md')}")


if __name__ == "__main__":
    main()
