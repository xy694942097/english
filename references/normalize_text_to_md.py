#!/usr/bin/env python3
"""文本类资料归一化为 Markdown（2026-09-16，总则第 4 条执行）。

两类转换（原件 txt 全部保留，md 是派生物，manifest 不登记派生物）：
1. papers/ 全部真题 txt → 原件旁同名 .md（含 OCR 版）；
2. dictionaries/wordbooks/etymology-*-full.txt → wordbooks-md/ 按首字母分册（控制单文件体积）。

json/jsonl/csv 按总则豁免（结构化数据保原生格式），只保留既有说明页。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "materials" / "papers"
WB = ROOT / "materials" / "dictionaries" / "wordbooks"
WBMD = ROOT / "materials" / "dictionaries" / "wordbooks-md"

CET6_TITLE = re.compile(r"(\d{4})[年\s.-]*(\d{1,2})[月\s.-]*第?\s*(\d)\s*套|(\d{4})-(\d{2})[_-](\d+)")


def exam_md_title(name: str) -> str:
    m = re.match(r"cet4-(\d{4})-(\d{2})-(\d)$", name)
    if m:
        return f"四级真题 {m[1]}年{int(m[2])}月第{m[3]}套"
    m = re.match(r"cet6-(\d{4})-(\d{2})$", name)
    if m:
        return f"六级真题 {m[1]}年{int(m[2])}月第1套"
    m = re.match(r"kaoyan-([12])-(\d{4})$", name)
    if m:
        return f"考研英语{'一' if m[1] == '1' else '二'}真题 {m[2]}"
    m = re.match(r"kaoyan1-(\d{4})$", name)
    if m:
        return f"考研英语一真题 {m[1]}（OCR）"
    return name


def convert_paper_txt(txt: Path) -> Path | None:
    """一份真题 txt → 原件旁同名 md。"""
    title = exam_md_title(txt.stem)
    body = txt.read_text(encoding="utf-8", errors="replace").strip()
    note = "文本为抽取/整理版，可能有断行；完形填空空格以 ___ 保留。"
    if txt.stem.startswith("kaoyan1-2020"):
        note = "扫描件 OCR 产物（pytesseract，仅 eng 模型）：正文英文可用，中文与排版不可靠。"
    out = txt.with_suffix(".md")
    out.write_text(
        f"# {title}\n\n"
        f"> 来源：materials/papers/{txt.parent.name}/{txt.name}（原件 txt 保留在旁，"
        f"登记哈希见 materials/downloads-manifest.json）。{note}\n\n{body}\n",
        encoding="utf-8")
    return out


ENTRY = re.compile(r"^(\d+)\. ([a-zA-Z][a-zA-Z'-]*)\s*$", re.M)


def convert_wordbook(book: str, label: str) -> list[Path]:
    """一册词源书全文 txt → 按词目首字母分册 md。

    词条以 "N. word" 行分隔；每个分册加目录索引，Entries 小节用 ### 锚点。
    850 万字符拆 26 册后单册约 100-400KB，前端可接受。
    """
    src = WB / f"etymology-{book}-full.txt"
    text = src.read_text(encoding="utf-8", errors="replace")
    matches = list(ENTRY.finditer(text))
    if not matches:
        return []
    # 序号在非词目处（如中文行）也可能出现，只认「数字. 英文单词」且下一行是 UK/US 音标或 Definitions
    entries = []
    for i, m in enumerate(matches):
        nxt = re.sub(r"\s+", " ", text[m.end():m.end() + 300])
        # 音标行可能隔空白行：300 字符内出现 UK/US/音标斜杠或 Definitions 段即认定为词目；
        # 中文行（如词源叙述里的「1. 灰烬」）不会命中此模式
        if not re.search(r"(UK|US|/|Definitions)", nxt):
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entries.append((int(m[1]), m[2], text[m.start():end].strip()))
    (WBMD / book).mkdir(parents=True, exist_ok=True)
    written = []
    by_letter: dict[str, list] = {}
    for num, word, body in entries:
        by_letter.setdefault(word[0].lower(), []).append((num, word, body))
    for letter in sorted(by_letter):
        es = by_letter[letter]
        toc = "\n".join(f"- {w}（{num}）" for num, w, _ in es)
        parts = [f"# 词源单词本 {label} · {letter.upper()}\n\n"
                 f"> 来源：materials/dictionaries/wordbooks/etymology-{book}-full.txt"
                 f"（pdftotext -layout 提取，原件 PDF 见同目录，哈希见 manifest）。"
                 f"本册 {len(es)} 词。\n\n## 目录\n\n{toc}\n"]
        for num, word, body in es:
            parts.append(f"\n---\n\n## {word}\n\n{body}\n")
        out = WBMD / book / f"{book}-{letter}.md"
        out.write_text("".join(parts), encoding="utf-8")
        written.append(out)
    return written


def main() -> None:
    n_papers = 0
    for sub in ["exams", "cet4", "cet6"]:
        for txt in sorted((PAPERS / sub).glob("*.txt")):
            convert_paper_txt(txt)
            n_papers += 1
    n_wb = 0
    for book, label in [("cet4", "四级"), ("cet6", "六级"), ("tem8", "专八")]:
        outs = convert_wordbook(book, label)
        n_wb += len(outs)
        sizes = [o.stat().st_size // 1024 for o in outs]
        print(f"wordbooks {book}: {len(outs)} 分册, {min(sizes)}-{max(sizes)}KB/册")
    print(f"papers txt→md: {n_papers} | wordbook 分册: {n_wb}")


if __name__ == "__main__":
    main()
