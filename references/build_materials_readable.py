#!/usr/bin/env python3
"""把 materials/papers/ 下的真题文本转成前端可读的 Markdown 层。

输出到 materials/readable/（派生物，可随时重跑重建，不入 git）。
数据原件不动：PDF/JSON 等保持原样，本脚本只消费 .txt 文本。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "materials" / "papers"
OUT = ROOT / "materials" / "readable"


def cet6_title(sets_lines: list[str]) -> str:
    return "六级真题文本（按年合并）"


def humanize(name: str) -> str:
    """exams/cet4-2022-06 → 四级 2022-06；kaoyan1-2020 → 考研英一 2020（OCR）"""
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


def slug(t: str) -> str:
    return re.sub(r"[\s/]+", "-", t)


def convert_exam_txt(txt: Path, dest_dir: Path) -> Path:
    name = txt.stem
    title = humanize(name)
    body = txt.read_text(encoding="utf-8", errors="replace").strip()
    out = dest_dir / f"{slug(title)}.md"
    out.write_text(f"# {title}\n\n> 来源：materials/papers/{txt.parent.name}/{txt.name}，"
                   f"原件与 SHA-256 见 materials/downloads-manifest.json。文本为抽取/整理版，"
                   f"可能有断行残留；完形填空空格以 ___ 保留。\n\n{body}\n", encoding="utf-8")
    return out


def convert_cet6_year(txts: list[Path], year: str, dest_dir: Path) -> Path:
    parts = [f"# {year} 年六级真题文本\n\n> 来源：materials/papers/cet6/（AndrewYuZhenYu/"
             f"cet6_exam_questions_txt_collection），全年各套合并。文本为整理版，可能有断行；"
             f"完形填空空格以 ___ 保留。\n"]
    for txt in sorted(txts):
        parts.append(f"\n---\n\n## {cet6_set_title(txt.stem)}\n\n"
                     + txt.read_text(encoding="utf-8", errors="replace").strip() + "\n")
    out = dest_dir / f"cet6-{year}.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def convert_cet4_sitting(txts: list[Path], sitting: str) -> Path:
    y, m = sitting.split("-")
    parts = [f"# 四级真题 {y}年{int(m)}月（全3套）\n\n> 来源：materials/papers/cet4/，"
             f"pypdf 抽取文本合并。可能有断行残留；原件 PDF 与哈希见 manifest。\n"]
    for txt in sorted(txts):
        n = txt.stem[-1]
        parts.append(f"\n---\n\n## 第{int(n)}套\n\n"
                     + txt.read_text(encoding="utf-8", errors="replace").strip() + "\n")
    out = OUT / "papers" / f"cet4-{sitting}.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def main() -> None:
    for sub in ["papers/exams", "papers/cet6", "papers/kaoyan-jingfan", "dictionaries"]:
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    generated: list[tuple[str, str, int]] = []  # (相对路径, 标题, 字符数)

    # exams：一份一个 md
    for txt in sorted((PAPERS / "exams").glob("*.txt")):
        out = convert_exam_txt(txt, OUT / "papers" / "exams")
        rel = out.relative_to(ROOT)
        generated.append((str(rel), out.stem.split(".md")[0], out.stat().st_size))

    # cet4：一次考试一个 md（3 套合并）
    by_sitting: dict[str, list[Path]] = {}
    for txt in sorted((PAPERS / "cet4").glob("*.txt")):
        parts = txt.stem.split("-")  # cet4-2024-06-1
        by_sitting.setdefault(f"{parts[1]}-{parts[2]}", []).append(txt)
    for sitting, txts in sorted(by_sitting.items()):
        out = convert_cet4_sitting(txts, sitting)
        generated.append((str(out.relative_to(ROOT)), f"四级 {sitting}（全3套）", out.stat().st_size))

    # cet6：一年一个 md（全年各套合并）
    by_year: dict[str, list[Path]] = {}
    for txt in sorted((PAPERS / "cet6").glob("*.txt")):
        by_year.setdefault(txt.stem[:4], []).append(txt)
    for year, txts in sorted(by_year.items()):
        out = convert_cet6_year(txts, year, OUT / "papers" / "cet6")
        generated.append((str(out.relative_to(ROOT)), f"六级 {year}", out.stat().st_size))

    # kaoyan-jingfan：精翻 md 已经是 md，去 frontmatter 后入可读层（链接到原文件）
    for src in sorted((PAPERS / "kaoyan-jingfan").glob("*.md")):
        year = re.search(r"(\d{4})", src.stem)[1]
        body = re.sub(r"^---\n.*?\n---\n", "", src.read_text(encoding="utf-8").strip(), flags=re.S)
        out = OUT / "papers" / "kaoyan-jingfan" / f"kaoyan1-jingfan-{year}.md"
        out.write_text(f"# 考研英语一 {year} 年阅读精翻\n\n> 来源：materials/papers/kaoyan-jingfan/"
                       f"kaoyan1-jingfan-{year}.md（Destinnnnn/kaoyan-english-1-2005-2026）。逐句原文+精译+"
                       f"词汇搭配+长难句拆解；含 Obsidian callout 语法，网页渲染为引用块。\n\n{body}\n",
                       encoding="utf-8")
        generated.append((str(out.relative_to(ROOT)), f"考研英一 {year} 精翻", out.stat().st_size))

    # 词源书说明页：指向 wordbooks-md 分册（normalize_text_to_md.py 生成，前端直接可见）
    (OUT / "dictionaries").mkdir(parents=True, exist_ok=True)
    lines = ["# 词源单词本（Markdown 分册）\n\n",
             "词源书三册（四级/六级/专八）全文已归一化为 Markdown：按词目首字母分册存于 "
             "materials/dictionaries/wordbooks-md/<册>/<册>-<字母>.md（脚本 references/normalize_text_to_md.py 生成，"
             "可重跑重建），每册带目录，词条含音标、释义、词根拆解、词源叙述、双语例句，左侧目录「学习资料」组直接可见。"
             "数据层原件：etymology-*.pdf（哈希见 manifest）与 pdftotext 全文 etymology-*-full.txt 保留在 wordbooks/；"
             "官方精简 txt 只是裸词表。json/csv 等结构化资料按总则豁免不转 md。\n\n",
             "| 册 | 分册数 | 词条数 |\n| --- | --- | --- |\n"]
    for b, label in [("cet4", "四级"), ("cet6", "六级"), ("tem8", "专八")]:
        d = ROOT / "materials" / "dictionaries" / "wordbooks-md" / b
        if d.exists():
            import subprocess
            n = sum(int(x.split(':')[1]) for x in subprocess.run(
                ['grep', '-rc', '^## [a-z]', str(d)], capture_output=True, text=True).stdout.strip().split('\n') if ':' in x)
            lines.append(f"| {label} | {len(list(d.glob('*.md')))} | {n} |\n")
    (OUT / "dictionaries" / "wordbooks-full.md").write_text("".join(lines), encoding="utf-8")
    generated.append(("materials/readable/dictionaries/wordbooks-full.md", "词源书说明", 0))

    # 索引页
    lines = ["# 真题文本阅读层\n\n",
             "materials/ 下载资料的可读 md 层（自动生成，脚本 references/build_materials_readable.py，"
             "可重跑重建）。数据原件（PDF/JSON/txt）与哈希见 materials/downloads-manifest.json；"
             "本层哈希以原件为准。\n\n",
             "边界：考研手译版 5 册的中文层无法可靠提取（无 ToUnicode 映射），留作原件阅读，"
             "机读层由 2005-2026 阅读精翻（kaoyan-jingfan，22 份）替代；考研词频表走学习库查询。\n\n"]
    for rel, title, size in generated:
        lines.append(f"- {title}（{size // 1024}KB）\n")
    (OUT / "README.md").write_text("".join(lines), encoding="utf-8")

    print(f"generated {len(generated)} paper pages + index at materials/readable/")


if __name__ == "__main__":
    main()
