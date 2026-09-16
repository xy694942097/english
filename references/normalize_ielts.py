#!/usr/bin/env python3
"""雅思资料归一化（2026-09-16，总则「归一化规则」节执行）。

输入：materials/papers/ielts/（原件，manifest 登记，哈希以原件为准）。
产物（派生物，manifest 不登记，本脚本可重跑重建）：
1. 剑4/9/14 + IELTS16体验版（有文字层）→ 原件旁同名 .txt（pdftotext -layout）
   + 原件旁同名 .md（带来源头与质量注记）；
2. vocabulary/IELTS-wordlist-fanhongtao.txt → 原件旁 .md（词表转 md 总则）；
3. materials/readable/papers/ielts/ 可读层：上述 4 册 + 作文案例 3 篇 + 考试介绍 + 词表索引页。

扫描件（剑5/6/7/8/10/11/12/13/15/16/17/18）无文字层，不派生文本，质量边界见
materials/README.md 与 manifest note——留作「人读原件」，不进任何挖掘/导入管线。
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IELTS = ROOT / "materials" / "papers" / "ielts"
JY = IELTS / "剑桥雅思真题"
VOC = ROOT / "materials" / "vocabulary"
READABLE = ROOT / "materials" / "readable" / "papers" / "ielts"

# 文字层完好的册子 → (文件名, md 标题, 质量注记)
TEXT_LAYERED = {
    "剑桥雅思真题4.pdf": ("剑桥雅思真题 4", "文字层完好，无断字/混淆问题。"),
    "剑桥雅思真题9.pdf": ("剑桥雅思真题 9", "文字层完好；含沪江水印等中文字符约 9 千（噪音，可过滤）。"),
    "剑桥雅思真题14.pdf": ("剑桥雅思真题 14", "文字层为 OCR 嵌入层：约 36 处 i/l 混淆（invoIves 类），"
                                     "完整句约 1900 条可用，用于挖掘时按需校对。"),
    "IELTS16_体验版.pdf": ("IELTS16 官方体验版", "官方免费样张，文字层完好。"),
}


def pdftotext_layout(pdf: Path, out: Path) -> int:
    """pdftotext -layout 抽取全文，返回字符数。"""
    r = subprocess.run(["pdftotext", "-layout", str(pdf), str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"pdftotext failed on {pdf}: {r.stderr}")
    return out.stat().st_size


def paper_md(txt: Path, title: str, note: str) -> Path:
    """原件旁 md：来源头 + 质量注记 + 正文。"""
    body = txt.read_text(encoding="utf-8", errors="replace").strip()
    out = txt.with_suffix(".md")
    out.write_text(
        f"# {title}\n\n"
        f"> 来源：materials/papers/ielts/剑桥雅思真题/{txt.parent.name}/{txt.stem}.pdf"
        f"（原件 PDF 保留在旁，登记哈希见 materials/downloads-manifest.json）。"
        f"pdftotext -layout 派生物，可由 references/normalize_ielts.py 重跑重建。{note}"
        f"社区整理版，不宣称与官方发行版逐字一致；听力部分音频未收录。\n\n{body}\n",
        encoding="utf-8")
    return out


def readable_copy(md: Path, title: str, note: str) -> Path:
    """原件旁 md → readable/papers/ielts/ 可读层（加头，链接原位置）。"""
    body = md.read_text(encoding="utf-8").strip()
    # 去掉原件旁 md 已有的标题头，换成可读层标题
    body = re.sub(r"^# .+?\n+> .*?\n\n", "", body, count=1, flags=re.S)
    out = READABLE / md.name
    out.write_text(f"# {title}\n\n> {note}\n\n{body}\n", encoding="utf-8")
    return out


def main() -> None:
    READABLE.mkdir(parents=True, exist_ok=True)
    report = []

    # 1) 有文字层的册子：派生 txt + 原件旁 md + 可读层
    for pdf_name, (title, note) in TEXT_LAYERED.items():
        pdf = JY / pdf_name
        if not pdf.exists():
            report.append(f"MISSING {pdf_name}")
            continue
        txt = pdf.with_suffix(".txt")
        n = pdftotext_layout(pdf, txt)
        md = paper_md(txt, title, note)
        rmd = readable_copy(md, title, note)
        report.append(f"TXT+MD {pdf_name}: txt {n}B → {md.name}, readable {rmd.name}")

    # 2) 作文案例 3 篇 + 考试介绍：md 原件 → 可读层（加来源头）
    intro = {
        "IELTS 整体介绍&考试内容.md": "雅思考试整体介绍与考试内容（社区编写，zeeklog/IELTS）",
        "Readme.md": "IELTS 资料仓库说明（目录索引）",
        "Readme.EN.md": "IELTS 资料仓库说明（英文）",
    }
    for name, title in intro.items():
        src = IELTS / name
        if not src.exists():
            report.append(f"MISSING {name}")
            continue
        body = src.read_text(encoding="utf-8", errors="replace").strip()
        body = re.sub(r"^# .+?\n+", "", body, count=1)
        out = READABLE / name
        out.write_text(f"# {title}\n\n> 来源：materials/papers/ielts/{name}"
                       f"（zeeklog/IELTS，哈希见 manifest）。\n\n{body}\n", encoding="utf-8")
        report.append(f"MD {name} → readable")

    for f in sorted((IELTS / "作文案例").glob("*.md")):
        body = f.read_text(encoding="utf-8", errors="replace").strip()
        body = re.sub(r"^# .+?\n+", "", body, count=1)
        out = READABLE / f.name
        out.write_text(f"# 雅思图表作文范文：{f.stem}\n\n> 来源：materials/papers/ielts/作文案例/"
                       f"{f.name}（zeeklog/IELTS，剑桥19 类图表题范文，哈希见 manifest）。\n\n{body}\n",
                       encoding="utf-8")
        report.append(f"MD 作文案例/{f.name} → readable")

    # 3) fanhongtao 词表 txt → 原件旁 md（词表转 md，索引页进 readable）
    wtxt = VOC / "IELTS-wordlist-fanhongtao.txt"
    if wtxt.exists():
        body = wtxt.read_text(encoding="utf-8", errors="replace").strip()
        wmd = wtxt.with_suffix(".md")
        wmd.write_text(
            "# 雅思词汇词根+联想记忆法（乱序便携版）单词表\n\n"
            "> 来源：materials/vocabulary/IELTS-wordlist-fanhongtao.txt（fanhongtao/IELTS，"
            "作者手抄录入 3722 行，含音标与中文释义；哈希见 manifest）。"
            "原件 txt 的派生物，normalize_ielts.py 可重跑重建。仅本地个人学习使用。\n\n"
            "```text\n" + body + "\n```\n", encoding="utf-8")
        report.append(f"TXT+MD 词表: {wmd.name}（{wmd.stat().st_size}B）")
        # readable 索引页：词表本体大（~250KB），readable 只放说明页
        idx = READABLE / "IELTS词表索引.md"
        idx.write_text(
            "# 雅思词表（归一化说明）\n\n"
            "> 本页是索引说明，词表本体见左侧目录对应文件。\n\n"
            "| 词表 | 规模 | 位置 | 状态 |\n| --- | --- | --- | --- |\n"
            "| IELTS-rich.jsonl | 7002 词（音标/中译/词组/双语例句） | materials/vocabulary/ | "
            "jsonl 结构化豁免转 md；与 CET rich 同构，可直接走导入管线 |\n"
            "| IELTS-wordlist-fanhongtao | 3722 行（音标+中文释义） | materials/vocabulary/ | "
            "原件 txt + 原件旁 md（代码块包裹保排版） |\n", encoding="utf-8")
        report.append("MD 词表索引页 → readable")

    # 4) 汇总：哪些册子是扫描件（未派生）
    scans = [p.name for p in sorted(JY.glob("*.pdf"))
             if p.name not in TEXT_LAYERED]
    report.append(f"扫描件（未派生文本，阅读件）：{len(scans)} 册 → {', '.join(scans)}")

    print("\n".join(report))


if __name__ == "__main__":
    main()
