#!/usr/bin/env python3
"""分级句池构建：四级/六级/考研(真题+精翻) → 带id分级别信息句池。
防幻觉设计：全部程序抽取，每句带 id 与 loc，供后续逐字校验。
过滤：指令/选项/中文/填空/题号/页眉。池句条件：≥8词、大写率<0.4、含尾标点。"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # english/
OUT = Path(__file__).resolve().parent / "pools"
OUT.mkdir(exist_ok=True)

DROP = re.compile(r"^(Directions|Questions?\s*\d|Part\s+[IVW]+|Section\s+[A-D]|Translation|Writing|Listening|Reading|答案|解析|注[:：]|【|英语[（(].*试题|.*第\d+页.*)", re.I)
OPT = re.compile(r"\b[A-D]\)|（?[A-D]）|^[A-D][).．]\s|^\d{1,3}[\.\、]\s*[A-D]\)?")
QMARK = re.compile(r"^Q\d+|\bQ\d+\b|___+|\.{4,}")
ZH = re.compile(r"[\u4e00-\u9fff]")
MD = re.compile(r"^(#|>|\||-|\s*$|\+\+|---)")

def clean_line(l):
    l = l.strip()
    if not l: return None
    if DROP.match(l): return None
    if OPT.search(l): return None
    if QMARK.search(l): return None
    zh = len(ZH.findall(l))
    if zh / max(len(l), 1) > 0.15: return None
    if MD.match(l): return None
    return l

def split_sentences(text):
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([a-z]) -([a-z])", r"\1-\2", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", text)
    return parts

def ok_sentence(s):
    s = re.sub(r"^\d{1,3}[\.、]\s*", "", s)
    w = s.split()
    if len(w) < 8 or len(w) > 60: return False
    up = sum(1 for c in s if c.isupper())
    if up / max(len(s), 1) > 0.4: return False
    if ZH.search(s): return False
    if not re.search(r"[.!?][\"')]?$", s): return False
    if re.match(r"^[A-D][).\s]", s): return False
    # 完形空号残留：词+悬挂 1-2 位数字（非年份/非百分比）
    if re.search(r"\b[a-zA-Z]+\s\d{1,2}\b", s) and not re.search(r"\b(19|20)\d{2}\b|%", s): return False
    return s

def parse_jingfan(path):
    """精翻md：英文在 [!quote] 原文 引用块内，剥 ==高亮== 与（定位：…）标记。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    quotes, cur, in_q = [], [], False
    for l in lines:
        if l.startswith("> [!quote]"):
            if cur: quotes.append(" ".join(cur))
            cur, in_q = [], True
            continue
        if in_q and l.startswith(">"):
            body = l.lstrip(">").strip()
            if body: cur.append(body)
        elif in_q and not l.startswith(">"):
            if cur: quotes.append(" ".join(cur))
            cur, in_q = [], False
    if cur: quotes.append(" ".join(cur))
    clean = []
    for q in quotes:
        q = re.sub(r"==|（?定位[:：][^）]*）?", " ", q)
        q = re.sub(r"\s+", " ", q).strip()
        if q: clean.append(q)
    return clean

def build(level, files):
    seen, pool = set(), []
    for f in files:
        loc = f.stem
        paras, cur = [], []
        if f.suffix == ".md":
            paras = parse_jingfan(f)
        else:
            for raw in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                if clean_line(raw) is None:
                    if cur: paras.append(" ".join(cur)); cur = []
                    continue
                cur.append(raw.strip())
            if cur: paras.append(" ".join(cur))
        for p in paras:
            for s in split_sentences(p):
                s0 = s.strip(" \u201c\u201d\"'")
                s1 = ok_sentence(s0)
                if s1 and s1 not in seen:
                    seen.add(s1)
                    pool.append({"id": f"{level}-{loc}-{len(pool):04d}", "s": s1, "loc": loc})
    return pool

LEVELS = {
    "cet4": sorted((ROOT / "materials/papers/cet4").glob("*.txt")) + [ROOT / "materials/papers/exams/cet4-2022-06.txt"],
    "cet6": sorted((ROOT / "materials/papers/cet6").glob("*.txt")) + [ROOT / "materials/papers/exams/cet6-2018-06.txt"],
    "kaoyan": sorted((ROOT / "materials/papers/exams").glob("kaoyan-*.txt")) + sorted((ROOT / "materials/papers/exams").glob("kaoyan1-2020.txt")) + sorted((ROOT / "materials/papers/kaoyan-jingfan").glob("*.md")),
}

for level, files in LEVELS.items():
    pool = build(level, [f for f in files if f.exists()])
    (OUT / f"{level}.json").write_text(json.dumps(pool, ensure_ascii=False, indent=0), encoding="utf-8")
    locs = {}
    for d in pool: locs[d["loc"]] = locs.get(d["loc"], 0) + 1
    print(f"{level}: {len(pool)} 句 / {len(locs)} 份材料")
