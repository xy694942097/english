# 下载批次记录归档（2026-09-14 ~ 09-16）

> 本页是历史批次的事实记录（来源明细、许可、边界说明），归档自 references/README.md（2026-09-16 收敛规则时迁出）。现行规则见 materials/HANDBOOK.md；资料清单见 materials/README.md；流水账见 engineering/agents/book-editorial/CHANGELOG.md。

## 真题语料（2026-09-16）

materials/papers/exams/ 下有 9 份四六级/考研历年真题 PDF 及对应 .txt 抽取（pypdf，约 22 万字符），用于句式框架真题回收（08-frames/09-exam-recall.md）：四级 2022-06 第 1 套、六级 2018-06 卷一、考研英语一 2017/2018/2019、考研英语二 2016/2017/2018/2019。

下载源（GitHub 公开仓库，raw 文件直连）：[youngflysky/KaoYanZhenTi-PDF](https://github.com/youngflysky/KaoYanZhenTi-PDF)（英一、六级）、[zwd1216/yingyuer](https://github.com/zwd1216/yingyuer)（英二）、[DieDiDi/CET4-6-past-exam-paper](https://github.com/DieDiDi/CET4-6-past-exam-paper)（四级）。每份文件的字节数、SHA-256、来源与原始下载 URL 见 materials/downloads-manifest.json（files 列表中 file 为 papers/exams/*.pdf 的条目，downloaded 2026-09-16），下载时已按 API 报告大小核对文件完整性。

边界：模拟题未收录（公开可批量下载的多为历年真题，模拟题基本是版权教辅，未找到可合法下载的开放语料）。PDF 抽取文本可能存在断行与公式残留，用作框架归纳语料前已人工核对每条例句；不作为排版誊写依据。这些真题为考试回忆/整理版，不宣称与官方发行版逐字一致。

## 考试参考资料库（2026-09-16）

papers/、dictionaries/wordbooks/ 下共 81 个文件，全部登记于 materials/downloads-manifest.json（files 列表，downloaded 2026-09-16），全量 SHA-256 已校验通过。原始路径曾为 references/downloads/ 下的平铺子目录，2026-09-16 迁入 materials/ 分类结构。

**papers/exams/**（上文，9 份真题）之外新增：

- **papers/cet4/**：四级 2024-06、2025-06 各 3 套真题 PDF（紧凑版，每份 300-400KB），来自 [0609x/CET46-Resources](https://github.com/0609x/CET46-Resources)；已随文件抽取同名 .txt（pypdf，每份 1.9-2.5 万字符），供后续框架挖掘。txt 是派生物，哈希以 PDF 为准。
- **papers/cet6/**：六级 2016-2026 历年真题纯文本 62 份（约 1MB），来自 [AndrewYuZhenYu/cet6_exam_questions_txt_collection](https://github.com/AndrewYuZhenYu/cet6_exam_questions_txt_collection)。已经是规整 TXT，可直接用于词频统计与框架归纳。
- **papers/kaoyan/**：考研英语一手译版 5 册（1986-2020 分段 PDF，约 4.8MB，阅读参考用）+ 2020 年英一真题纯卷，来自 [m2kar/KaoYan-English](https://github.com/m2kar/KaoYan-English)；考研大纲词汇词频排序表 netem-vocab-freq.json（5530 词，含释义/分类），来自 [exam-data/NETEMVocabulary](https://github.com/exam-data/NETEMVocabulary)，数据许可 CC BY-NC-SA 4.0（非商业用途）。
- **dictionaries/wordbooks/**：词源单词本 CET4/CET6/TEM8 三册（PDF+TXT 词条表），来自 [openetymology/OpenEtymology](https://github.com/openetymology/OpenEtymology)，词书文件许可 CC BY-SA 4.0。专八方向的可用开放资料：TEM8 分册覆盖专八词表（词源、词根拆解）；专八历年真题无公开开放仓库，未收录。

用途边界：papers/cet4、papers/cet6 文本与 papers/exams 同为框架挖掘与出题素材；papers/kaoyan 手译版与 dictionaries/wordbooks 是阅读型参考书，不进入学习库、不计入词汇导入统计。各仓库均为考试回忆/社区整理版，不宣称与官方发行版逐字一致。

## 其他语料目录

- `materials/vocabulary/zhenghaoyang24-voc/`：voc14w 例句语料（github.com/zhenghaoyang24/english-vocabulary），框架章「语料」标注例句的来源。
- `materials/corpus/opus-opensubtitles/`：OPUS OpenSubtitles 英中平行语料（约 1.5GB），备用的真实语境语料，尚未入库使用。
- `materials/dictionaries/`：ECDICT、WordNet、Kaikki/Wiktionary 数据，见 references/dictionaries-2026-09-15.md。

## 初高中教材语料（2026-09-16）

`materials/textbooks/` 下新增两批，共 7 个文件登记于 materials/downloads-manifest.json（downloaded 2026-09-16，SHA-256 已校验）：

- **初中人教版/**（5 册 Markdown 全文，约 1.2MB）：人教版《Go for it!》七年级上/下、八年级上/下、九年级全一册，来自 [chncaesar/ChinaTextbook-Text](https://github.com/chncaesar/ChinaTextbook-Text)（仓库无 LICENSE 声明，仅本地个人学习使用，不再分发）。PDF 提取文本：正文真实完整（五册合计约 7500 行成段英文课文），但含目录/版权页噪音，常见 PDF 断行（如 "Y ou"、"att ention"、"fl oor"），做精确匹配前需归一化。
- **高中人教版2019/**：
  - `textbook_index_data.zip` + 解压物 `index-extracted/textbook_sentence_index.json`（29MB）：高中教材句子倒排索引，来自 [ZhangYixuan-in-BUPT/textbook-sentence-index](https://github.com/ZhangYixuan-in-BUPT/textbook-sentence-index)（MIT License）。覆盖人教/沪教/译林/外研四版本 × 必修一至选择性必修四共 7 册层级，实测去重后 30,110 句（人教版 8,523 句），每句带版本/册别/单元/单元主题出处。zip 为登记原始物，解压物是派生物。
  - `pep-senior-vocab.json`：人教 2019 版高中英语七册词汇总表（2,569 词条，含册别/单元/词性/中文释义），来自 [lfcypo/pep-senior-eng-vocab-json](https://github.com/lfcypo/pep-senior-eng-vocab-json)（无 LICENSE，仅本地使用）。

用途：初中课文全文与高中句子库是「教材框架回收」的原始语料——07 章当初以课标项目表为纲补写、未逐册扫描教材的缺口，现在可以真正逐册扫了；高中句子库的倒排结构可直接按框架关键词检索教材原句。两库均为社区 OCR/整理版，不宣称与官方教材逐字一致。

## 词汇批次（2026-09-14，词表导入）

原始文件现保存在 `materials/vocabulary/`，哈希清单为 `materials/downloads-manifest.json`；实际导入来源、统计和备份路径见 imports/2026-09-14-vocabulary/report.json。来源与许可明细保留在 references/README.md「来源及下载方式」节。
