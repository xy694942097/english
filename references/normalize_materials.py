#!/usr/bin/env python3
"""materials/ 资料归一化统一入口（2026-09-16，规则见 materials/HANDBOOK.md）。

子命令（均幂等可重跑，派生物不登记 manifest，哈希以原件为准）：
  papers    papers/ 真题 txt → 原件旁同名 .md（含 OCR 版，数据层不进目录）；
            wordbooks 词源书三册全文 txt → wordbooks-md/ 每册一个合集 md；
  readable  materials/readable/ 汇总层：四/六/考研真题合集、考研精翻合集、
            初中教材合集、词源书说明页、索引页；
  all       全部依次执行。

合集化原则（2026-09-16 用户定版）：学习资料是参考资料，大概率不细读，
按考试专题各合 1 个文档，宁少而全不多而碎。json/jsonl/csv 按手册豁免
（结构化数据保原生格式）。
"""
import re
import sys
from pathlib import Path
from document_paths import document_path, write_document

ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"
PAPERS = MATERIALS / "papers"
WB = MATERIALS / "dictionaries" / "wordbooks"
WBMD = MATERIALS / "dictionaries" / "wordbooks-md"
OUT = MATERIALS / "readable"
ENTRY = re.compile(r"^(\d+)\. ([a-zA-Z][a-zA-Z'-]*)\s*$", re.M)
SCRIPT = "references/normalize_materials.py"


# ---------- papers：真题 txt → 原件旁 md；词源书 → wordbooks-md 合集 ----------

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


def convert_paper_txt(txt: Path) -> Path:
    """一份真题 txt → 原件旁同名 md（数据层派生物，不进目录）。"""
    title = exam_md_title(txt.stem)
    body = txt.read_text(encoding="utf-8", errors="replace").strip()
    note = "文本为抽取/整理版，可能有断行；完形填空空格以 ___ 保留。"
    if txt.stem.startswith("kaoyan1-2020"):
        note = "扫描件 OCR 产物（pytesseract，仅 eng 模型）：正文英文可用，中文与排版不可靠。"
    out = txt.with_suffix(".md")
    write_document(out,
        f"# {title}\n\n"
        f"> 来源：materials/papers/{txt.parent.name}/{txt.name}（原件 txt 保留在旁，"
        f"登记哈希见 materials/downloads-manifest.json）。{note}\n\n{body}\n",
        encoding="utf-8")
    return out


def parse_wordbook_entries(book: str) -> list[tuple[int, str, str]]:
    """词源书全文 txt → [(序号, 词目, 正文)]。

    词条以 "N. word" 行分隔；序号在非词目处（如中文行）也可能出现，
    只认「数字. 英文单词」且其后 300 字符内出现 UK/US 音标或 Definitions 段；
    中文行（如「1. 灰烬」）不会命中此模式。
    """
    src = WB / f"etymology-{book}-full.txt"
    text = src.read_text(encoding="utf-8", errors="replace")
    matches = list(ENTRY.finditer(text))
    entries = []
    for i, m in enumerate(matches):
        nxt = re.sub(r"\s+", " ", text[m.end():m.end() + 300])
        if not re.search(r"(UK|US|/|Definitions)", nxt):
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entries.append((int(m[1]), m[2], text[m.start():end].strip()))
    return entries


def convert_wordbook(book: str, label: str) -> Path:
    """一册词源书全文 txt → 单个合集 md（按词目字母排序，2026-09-16 合集化）。"""
    entries = parse_wordbook_entries(book)
    if not entries:
        raise RuntimeError(f"词源书 {book} 未解析出词条")
    entries.sort(key=lambda e: e[1].lower())
    parts = [f"# 词源单词本（{label}）\n\n"
             f"> 来源：materials/dictionaries/wordbooks/etymology-{book}-full.txt"
             f"（pdftotext -layout 提取，原件 PDF 见同目录，哈希见 manifest）。"
             f"共 {len(entries)} 词条，按词目字母排序；词条内保留原书课序编号、音标、释义、"
             f"词根拆解、词源叙述与双语例句。参考资料合集页，内容较长属预期。\n"]
    for num, word, body in entries:
        parts.append(f"\n---\n\n## {word}\n\n{body}\n")
    out = WBMD / f"etymology-{book}.md"
    write_document(out, "".join(parts), encoding="utf-8")
    return out


def cmd_papers() -> None:
    n_papers = 0
    for sub in ["exams", "cet4", "cet6"]:
        for txt in sorted((PAPERS / sub).glob("*.txt")):
            convert_paper_txt(txt)
            n_papers += 1
    for book, label in [("cet4", "四级"), ("cet6", "六级"), ("tem8", "专八")]:
        out = convert_wordbook(book, label)
        print(f"wordbooks {book}: {label} 合集 {out.stat().st_size // 1024}KB")
    print(f"[papers] txt→md: {n_papers} | 词源书合集: 3")


# ---------- readable：materials/readable/ 汇总层（合集化） ----------

def humanize(name: str) -> str:
    """exams/cet4-2022-06-1 → 四级 2022-06；kaoyan1-2020 → 考研英一 2020（OCR）"""
    m = re.match(r"kaoyan1-(\d{4})$", name)
    if m:
        return f"考研英语一真题 {m[1]}（OCR）"
    m = re.match(r"cet4-(\d{4})-(\d{2})(?:-(\d))?$", name)
    if m:
        sit = f"{m[1]}年{int(m[2])}月"
        return f"四级真题 {sit} 第{m[3]}套" if m[3] else f"四级真题 {sit} 第1套"
    m = re.match(r"cet6-(\d{4})-(\d{2})$", name)
    if m:
        return f"六级真题 {m[1]}年{int(m[2])}月 第1套"
    m = re.match(r"kaoyan-([12])-(\d{4})$", name)
    if m:
        return f"考研英语{'一' if m[1] == '1' else '二'}真题 {m[2]}"
    return name


def cet6_set_title(stem: str) -> str:
    m = re.match(r"(\d{4})-(\d{2})[_-](\d+)$", stem)
    if m:
        return f"{m[1]}年{int(m[2])}月 第{int(m[3])}套"
    return stem


def exam_body(txt: Path) -> str:
    return txt.read_text(encoding="utf-8", errors="replace").strip()


def collect_cet4() -> list[tuple[str, str]]:
    """[(小节标题, 正文)]，新→旧。"""
    secs: dict[str, dict[str, str]] = {}
    t = PAPERS / "exams" / "cet4-2022-06-1.txt"
    if t.exists():
        secs.setdefault("2022年6月", {})["第1套"] = exam_body(t)
    for txt in sorted((PAPERS / "cet4").glob("*.txt")):
        p = txt.stem.split("-")  # cet4-2024-06-1
        secs.setdefault(f"{p[1]}年{int(p[2])}月", {})[f"第{int(p[3])}套"] = exam_body(txt)
    out = []
    for sit in sorted(secs, reverse=True):
        for n in sorted(secs[sit]):
            out.append((f"{sit} {n}", secs[sit][n]))
    return out


def collect_cet6() -> list[tuple[str, str]]:
    """[(小节标题, 正文)]，新→旧。"""
    secs: dict[str, dict[str, str]] = {}
    t = PAPERS / "exams" / "cet6-2018-06.txt"
    if t.exists():
        secs.setdefault("2018年6月", {})["第1套"] = exam_body(t)
    for txt in sorted((PAPERS / "cet6").glob("*.txt")):
        secs.setdefault(txt.stem[:4], {})[cet6_set_title(txt.stem)] = exam_body(txt)
    out = []
    for year in sorted(secs, reverse=True):
        for title in sorted(secs[year]):
            out.append((title, secs[year][title]))
    return out


def collect_kaoyan_exams() -> list[tuple[str, str]]:
    """考研真题 [(标题, 正文)]，英一新→旧、英二新→旧。"""
    out = []
    for pfx, label in [("kaoyan-1-", "考研英语一真题"), ("kaoyan-2-", "考研英语二真题")]:
        items = sorted((PAPERS / "exams").glob(f"{pfx}*.txt"),
                       key=lambda p: p.stem, reverse=True)
        for txt in items:
            year = re.search(r"(\d{4})", txt.stem)[1]
            out.append((f"{label} {year}", exam_body(txt)))
    ocr = PAPERS / "exams" / "kaoyan1-2020.txt"
    if ocr.exists():
        out.append(("考研英语一真题 2020（OCR）", exam_body(ocr)))
    return out


def merged_exam_doc(path: Path, title: str, source_note: str, sections: list[tuple[str, str]],
                    extra_note: str = "") -> Path:
    parts = [f"# {title}\n\n> {source_note}{extra_note}"
             f"文本为抽取/整理版，可能有断行残留；完形填空空格以 ___ 保留。"
             f"由 references/normalize_materials.py 重跑重建。\n"]
    for sec_title, body in sections:
        parts.append(f"\n---\n\n## {sec_title}\n\n{body}\n")
    write_document(path, "".join(parts), encoding="utf-8")
    return path


def cmd_readable() -> None:
    (OUT / "papers").mkdir(parents=True, exist_ok=True)
    (OUT / "textbooks").mkdir(parents=True, exist_ok=True)
    (OUT / "dictionaries").mkdir(parents=True, exist_ok=True)
    generated: list[tuple[str, str, int]] = []  # (相对路径, 标题, 字节数)

    # 真题合集（四/六/考研）
    specs = [
        (document_path('materials/readable/papers/四级真题合集.md'), "四级真题合集",
         "来源：materials/papers/exams/ 与 materials/papers/cet4/（DieDiDi、0609x 仓库），",
         collect_cet4(), ""),
        (document_path('materials/readable/papers/六级真题合集.md'), "六级真题合集",
         "来源：materials/papers/exams/ 与 materials/papers/cet6/（AndrewYuZhenYu 仓库），全年各套合并，",
         collect_cet6(), ""),
        (document_path('materials/readable/papers/考研真题合集.md'), "考研真题合集",
         "来源：materials/papers/exams/（youngflysky、zwd1216 仓库），",
         collect_kaoyan_exams(), "2020 年卷为扫描件 OCR（仅 eng 模型），中文与排版不可靠。"),
    ]
    for path, title, note, sections, extra in specs:
        out = merged_exam_doc(path, title, note, sections, extra)
        generated.append((str(out.relative_to(ROOT)), title, out.stat().st_size))

    # 考研精翻合集（22 份合一，新→旧）
    jingfan = []
    for src in sorted((PAPERS / "kaoyan-jingfan").glob("*.md"), reverse=True):
        year = re.search(r"(\d{4})", src.stem)[1]
        body = re.sub(r"^---\n.*?\n---\n", "", src.read_text(encoding="utf-8").strip(), flags=re.S)
        jingfan.append((f"考研英语一 {year} 年阅读精翻", body))
    out = document_path('materials/readable/papers/考研精翻合集.md')
    merged_exam_doc(
        out, "考研精翻合集",
        "来源：materials/papers/kaoyan-jingfan/（Destinnnnn/kaoyan-english-1-2005-2026）。"
        "逐句原文+精译+词汇搭配+长难句拆解；含 Obsidian callout 语法，网页渲染为引用块。"
        "替代中文层不可机读的手译版 5 册（无 ToUnicode 映射，留作原件阅读）。",
        jingfan)
    generated.append((str(out.relative_to(ROOT)), "考研精翻合集", out.stat().st_size))

    # 初中教材合集（5 册全文合一）
    tb = MATERIALS / "textbooks" / "初中人教版"
    order = ["七年级上册", "七年级下册", "八年级上册", "八年级下册", "九年级全一册"]
    parts = ["# 初中英语教材合集\n\n"
             "> 来源：materials/textbooks/初中人教版/（chncaesar/ChinaTextbook-Text，"
             "无 LICENSE 仅本地学习用，原件保留在旁，哈希见 manifest）。人教版《Go for it!》"
             "五册全文合一；正文真实完整，含目录/版权页噪音与常见 PDF 断行（\"Y ou\"/\"att ention\"），"
             f"精确匹配前需归一化。高中语料为结构化 JSON（句子索引 30,110 句 + 词汇表 2,569 词），"
             f"按 HANDBOOK 豁免转 md，走学习库/脚本查询。由 references/normalize_materials.py 重跑重建。\n"]
    n_tb = 0
    for pre in order:
        f = tb / f"英语{pre}.md"
        if not f.exists():
            continue
        n_tb += 1
        body = re.sub(r"^# .+?\n+", "", f.read_text(encoding="utf-8", errors="replace").strip(), count=1)
        parts.append(f"\n---\n\n## 人教版《Go for it!》{pre}\n\n{body}\n")
    out = document_path('materials/readable/textbooks/初中英语教材合集.md')
    write_document(out, "".join(parts), encoding="utf-8")
    generated.append((str(out.relative_to(ROOT)), f"初中英语教材合集（{n_tb} 册）", out.stat().st_size))

    # 词源书说明页：指向 3 个合集（papers 子命令生成，前端直接可见）
    lines = ["# 词源单词本（合集）\n\n",
             "词源书三册（四级/六级/专八）全文已归一化为 Markdown 合集：每册一个文档，"
             f"存于 materials/dictionaries/wordbooks-md/etymology-*.md（脚本 {SCRIPT} 生成，"
             "可重跑重建），按词目字母排序，词条含音标、释义、词根拆解、词源叙述、双语例句，"
             "左侧目录「学习资料」组直接可见。数据层原件：etymology-*.pdf（哈希见 manifest）与 "
             "pdftotext 全文 etymology-*-full.txt 保留在 wordbooks/；官方精简 txt 只是裸词表。"
             "json/csv 等结构化资料按 HANDBOOK 豁免不转 md。\n\n",
             "| 册 | 文档 | 词条数 | 体量 |\n| --- | --- | --- | --- |\n"]
    for b, label in [("cet4", "四级"), ("cet6", "六级"), ("tem8", "专八")]:
        f = WBMD / f"etymology-{b}.md"
        if f.exists():
            n = len(parse_wordbook_entries(b))
            lines.append(f"| {label} | {f.name} | {n} | {f.stat().st_size // 1024}KB |\n")
    write_document(OUT / "dictionaries" / "wordbooks-full.md", "".join(lines), encoding="utf-8")
    generated.append(("materials/readable/dictionaries/wordbooks-full.md", "词源书说明", 0))

    # 索引页
    lines = ["# 学习资料阅读层\n\n",
             f"materials/ 下载资料的可读 md 合集层（自动生成，脚本 {SCRIPT}，"
             "可重跑重建；2026-09-16 合集化：按考试专题各合一，宁少而全）。"
             "数据原件（PDF/JSON/txt）与哈希见 materials/downloads-manifest.json；"
             "本层哈希以原件为准。\n\n",
             "边界：考研手译版 5 册的中文层无法可靠提取（无 ToUnicode 映射），留作原件阅读，"
             "机读层由 2005-2026 阅读精翻合集替代。\n\n"]
    for rel, title, size in generated:
        lines.append(f"- {title}（{size // 1024}KB）\n")
    write_document(OUT / "README.md", "".join(lines), encoding="utf-8")

    print(f"[readable] generated {len(generated)} 合集 pages + index at materials/readable/")


COMMANDS = {"papers": cmd_papers, "readable": cmd_readable}


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help") or args[0] not in COMMANDS and args[0] != "all":
        print(__doc__)
        sys.exit(0 if args and args[0] in ("-h", "--help") else 1)
    if args[0] == "all":
        cmd_papers()
        cmd_readable()
    else:
        COMMANDS[args[0]]()


if __name__ == "__main__":
    main()
