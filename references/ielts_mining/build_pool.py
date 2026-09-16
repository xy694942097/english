#!/usr/bin/env python3
"""雅思语料池构建（2026-09-16，挖掘方法学第 1 步）。

输入：剑4/9/14 派生 txt（materials/papers/ielts/剑桥雅思真题/*.txt，normalize_materials.py ielts 产物）。
输出：references/ielts_mining/ielts_sentences.json —— [{id, src, s}]，排序后 300 句一批。

过滤（语域判据前置执行，方法学第 0/1 步）：
- 剑9 沪江水印中文行、全部 PDF 页眉残留；
- 指令/题目模板行（Questions N-M、Complete the...、Choose...、Write NO MORE THAN、
  SECTION/READING/LISTENING 大写标题等）；
- 含填空残片（___、孤立数字空位）的句子；
- <8 词句子（对话轮次框架密度低，方法学规定）。

诚实披露：剑14 为 OCR 嵌入层（约 36 处 i/l 混淆，invoIves 类），例句逐字复制时保留原样；
剑9 少量中文水印行已整行剔除，英文正文未改动。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "materials" / "papers" / "ielts" / "剑桥雅思真题"
OUT = ROOT / "references" / "ielts_mining"
BOOKS = {"剑桥雅思真题4.txt": "剑4", "剑桥雅思真题9.txt": "剑9", "剑桥雅思真题14.txt": "剑14"}

# 指令/题目/标题行（行首匹配或整行模式）
DROP_LINE = re.compile(
    r"^\s*(Questions?\s+\d|Section\s+\d|SECTION\s+\d|Test\s+\d|READING|LISTENING|WRITING|SPEAKING"
    r"|Complete the|Choose\s|Write\s+(NO MORE|ONE|TWO|THREE|the|your|correct)|Match\s|Label\s|Which\s+(paragraph|TWO|two|of the)"
    r"|Do the following|The following|Part\s+\d|Academic Reading|General Training|Instructions?|End of Test|Turn over|\*?\s*$)"
)
# 题干常见模板（句中出现即弃）
STEM = re.compile(
    r"do(es)? the following|Choose NO MORE THAN|Choose ONE WORD|Choose TWO|Choose THREE|"
    r"matching information|Match each|the correct letter|next to Questions|"
    r"Complete the (notes|table|summary|sentences?|flow-chart|diagram|form|notes below)"
)
# 行内含中文（剑9 水印；正文应为纯英文）
ZH = re.compile(r"[\u4e00-\u9fff]")
# 填空残片
BLANK = re.compile(r"_{2,}|\b\d+\s*___")
# 纯数字/编号行
NUMONLY = re.compile(r"^\s*[\d\s.]+\s*$")


def load_book(path: Path, tag: str) -> list[str]:
    """读 txt，过滤行，返回保留的原始行。"""
    kept = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if ZH.search(ln) or BLANK.search(ln):
            continue
        if DROP_LINE.match(ln) or NUMONLY.match(ln) or STEM.search(ln):
            continue
        s = ln.strip()
        if len(s) < 3:
            continue
        kept.append(s)
    return kept


SENT_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def to_sentences(lines: list[str], tag: str, start_id: int) -> tuple[list[dict], int]:
    """行拼段（layout 断行）→ 句号切分 → ≥8 词信息句。"""
    paras, buf = [], []
    for ln in lines:
        buf.append(ln)
        if re.search(r"[.!?\"']\s*$", ln) or len(ln) < 20:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    out = []
    for para in paras:
        para = re.sub(r"\s+", " ", para).strip()
        for s in SENT_END.split(para):
            s = s.strip()
            # 清理行内孤立的题目编号残留（"3 Some scientists..." 开头数字）
            s = re.sub(r"^\d{1,3}\s+(?=[A-Z])", "", s)
            if STEM.search(s):
                continue
            words = re.findall(r"[A-Za-z][A-Za-z'-]*", s)
            if len(words) < 8:
                continue
            # 大写比例过高 → 题目/标题残余
            letters = [c for c in s if c.isalpha()]
            if letters and sum(c.isupper() for c in letters) / len(letters) > 0.45:
                continue
            # OCR 乱码密集行（非常见字符）
            if sum(not (c.isalnum() or c in " ,.'\";:()!?-_—-" + "’‘“”") for c in s) > len(s) * 0.08:
                continue
            out.append({"id": f"I{start_id:05d}", "src": tag, "s": s})
            start_id += 1
    return out, start_id


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pool, n = [], 1
    for fname, tag in BOOKS.items():
        lines = load_book(SRC / fname, tag)
        sents, n = to_sentences(lines, tag, n)
        pool.extend(sents)
        print(f"{tag}: 过滤后行 {len(lines)}，信息句 {len(sents)}")
    pool.sort(key=lambda x: (x["src"], x["id"]))
    (OUT / "ielts_sentences.json").write_text(
        json.dumps(pool, ensure_ascii=False, indent=1), encoding="utf-8")
    batches = [pool[i:i + 300] for i in range(0, len(pool), 300)]
    bd = OUT / "llm_batches"
    bd.mkdir(exist_ok=True)
    for i, b in enumerate(batches, 1):
        (bd / f"batch_{i:03d}.json").write_text(
            json.dumps(b, ensure_ascii=False), encoding="utf-8")
    print(f"总信息句 {len(pool)}，切 {len(batches)} 批 → {bd}")


if __name__ == "__main__":
    main()
