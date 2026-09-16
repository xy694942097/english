# 已下载的词汇资料

> 2026-09-16 起全部下载资源统一存放在项目根目录 `materials/`，按类型分类：`vocabulary/`（词表与词汇语料，含 zhenghaoyang24-voc 例句库）、`dictionaries/`（ECDICT、WordNet、Kaikki、词源单词本 wordbooks）、`papers/`（真题：exams/cet4/cet6/kaoyan）、`corpus/`（OPUS 字幕语料）。哈希清单：`materials/downloads-manifest.json`（原始路径时代的条目路径已同步改写）。本文保留各批资料的来源、许可与质量边界说明。

本次任务日期：2026-09-14。原始文件现保存在 `materials/vocabulary/`，哈希清单为 `materials/downloads-manifest.json`；实际导入来源、统计和备份路径见imports/2026-09-14-vocabulary/report.json。

## 已录入的内容

- 四级词汇：原资料7508行，合并同名词后4544词；关联词组筛选后30478条。
- 六级词汇：原资料5651行，合并同名词后3991词；关联词组筛选后18236条。
- 专八词汇：原资料12881行，合并同名词后12410词；关联词组筛选后39430条。
- NGSL 1.2高频核心词：2809词，使用社区镜像，中英文释义随镜像保留。

不同词表有交集，不能把以上数量直接相加。正式知识库合计53972条：13134个词条、40833个词组义项，另有5个原有语法/句子/情境条目。

当前库中包括旧教材内容。新下载内容新增53717条，未新增学习事件、未变更复习日期。

## 来源及下载方式

考试词汇与关联材料来自 [KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary)，使用full_line_jsonl/sentence/正序下的四级、六级、专八文件。上游从kajweb/dict资料整理，文件可能合并多个词书；它们不是本次逐项核验的最新官方大纲。

高频词来自 [NGSL 1.2社区镜像提交](https://github.com/RealKai42/qwerty-learner/pull/1069)，固定引用0b29037中的NGSL_1.2.json；[NGSL官方项目](https://www.newgeneralservicelist.com/new-general-service-list)用于核对列表名称、2809规模与原表许可。官网CSV下载本轮未成功，因此尚未做镜像与官方CSV逐项比对；没有验证镜像行顺序就是词频排序，不能把前1000行称为前1000高频词。

终端直连部分下载站不稳定，实际通过jsDelivr的GitHub文件镜像完成下载。原始地址、镜像下载地址、下载日期和SHA-256保存在导入报告中。

原NGSL词表标注CC BY-SA 4.0，作者为Browne、Culligan、Phillips。代码仓库的GPL许可与上游教材数据的权利范围不能混为一谈；保留下载许可和出处，不宣称获得所有来源的再分发授权。本次未作线上发布。

## 处理规则与质量边界

1. 词头按现有规范合并；同名词在不同词表的额外释义与例句保存在各自来源中，不覆盖原有Book讲解和学习记录。
2. 词组按规范化英文与中文含义区分；不同含义仍可独立保存。
3. 关联词组只选2–6词、至多1词不在NGSL集合的条目。这是阅读难度粗筛，不是词频统计，不保证自然度或考试必考程度。
4. 每个词表的每个词最多保留3个去重完整例句及8个关联搭配；明显以省略号开头的片段例句不导入。该步骤不等于逐句语言审校。
5. 示例校订：internship原资料出现“实习医师”，已按Oxford将主释义改为实习、实习期、实习职位；原记录和校订说明同时保留。其他错误可能仍存在，应结合阅读语境核对。
6. 词组资料一般没有独立例句，不拿母词例句假装该词组例句。可以请老师按需生成并标明自造。
7. 在三个考试来源中共保留32221条例句记录，跨词表仍有重复；不声称这是去重后的独立例句数。

## 另已下载但未采用

Qwerty的CET4_T、CET6_T、TEM8_T简版，以及FCE/PTE非官方短语表用于比较与备选，未再次并入正式库，以免重复和混淆考试分类。ECDICT整库下载本轮未成功，未将其计入已导入来源。

## 本地词典补充

2026-09-15 已下载 ECDICT 和 Princeton WordNet 3.0，记录见 dictionaries-2026-09-15.md。ECDICT 提供英英/中文释义、音标、词频、考试标签、词形变化、词根词缀与近义辨析材料；WordNet 提供英英释义、同义词集合、反义词关系和部分例句。Kaikki / Wiktionary English 全量 JSONL 已部分下载，因当前网络 TLS/Range 不稳定暂未完成，不能作为已完成来源使用。

合并脚本：build_combined_dictionary.py。默认读取 ECDICT、WordNet、当前学习库中的例句/词组，生成 `data/combined_dictionary.sqlite3`，并把构建报告写到 `references/imports/2026-09-15-dictionary/report.json`。该脚本只生成独立词典索引，不修改 `data/learning.sqlite3` 中的学习记录和复习进度。

```bash
python3 references/build_combined_dictionary.py
```

## 使用与复现

网页进入知识库，用“词表分类”选择四级、六级、专八、NGSL或关联词组。条目页底部可展开各来源资料。收藏规模不是背诵任务量，关联词组尤其适合查阅和按需选择。

复现脚本：import_wordlists.py。先用 --dry-run 核对数量与格式，再用 --database 指向隔离数据库试导入。正式操作会保存备份、比较学习事件前后是否一致、检查SQLite完整性。重复导入测试与页面回归见site/verification/wordlists-import.md。

## 真题语料（2026-09-16）

materials/papers/exams/ 下有 9 份四六级/考研历年真题 PDF 及对应 .txt 抽取（pypdf，约 22 万字符），用于句式框架真题回收（08-frames/09-exam-recall.md）：四级 2022-06 第 1 套、六级 2018-06 卷一、考研英语一 2017/2018/2019、考研英语二 2016/2017/2018/2019。

下载源（GitHub 公开仓库，raw 文件直连）：[youngflysky/KaoYanZhenTi-PDF](https://github.com/youngflysky/KaoYanZhenTi-PDF)（英一、六级）、[zwd1216/yingyuer](https://github.com/zwd1216/yingyuer)（英二）、[DieDiDi/CET4-6-past-exam-paper](https://github.com/DieDiDi/CET4-6-past-exam-paper)（四级）。每份文件的字节数、SHA-256、来源与原始下载 URL 见 materials/downloads-manifest.json（files 列表中 file 为 papers/exams/*.pdf 的条目，downloaded 2026-09-16），下载时已按 API 报告大小核对文件完整性。

边界：模拟题未收录（公开可批量下载的多为历年真题，模拟题基本是版权教辅，未找到可合法下载的开放语料）。PDF 抽取文本可能存在断行与公式残留，用作框架归纳语料前已人工核对每条例句；不作为排版誊写依据。这些真题为考试回忆/整理版，不宣称与官方发行版逐字一致。

## 考试参考资料库（2026-09-16）

papers/、dictionaries/wordbooks/ 下共 81 个文件，全部登记于 materials/downloads-manifest.json（files 列表，downloaded 2026-09-16），全量 SHA-256 已校验通过。原始路径曾为 references/downloads/ 下的平铺子目录，2026-09-16 迁入 materials/ 分类结构。

**papers/exams/**（本节上文，9 份真题）之外新增：

- **papers/cet4/**：四级 2024-06、2025-06 各 3 套真题 PDF（紧凑版，每份 300-400KB），来自 [0609x/CET46-Resources](https://github.com/0609x/CET46-Resources)；已随文件抽取同名 .txt（pypdf，每份 1.9-2.5 万字符），供后续框架挖掘。txt 是派生物，哈希以 PDF 为准。
- **papers/cet6/**：六级 2016-2026 历年真题纯文本 62 份（约 1MB），来自 [AndrewYuZhenYu/cet6_exam_questions_txt_collection](https://github.com/AndrewYuZhenYu/cet6_exam_questions_txt_collection)。已经是规整 TXT，可直接用于词频统计与框架归纳。
- **papers/kaoyan/**：考研英语一手译版 5 册（1986-2020 分段 PDF，约 4.8MB，阅读参考用）+ 2020 年英一真题纯卷，来自 [m2kar/KaoYan-English](https://github.com/m2kar/KaoYan-English)；考研大纲词汇词频排序表 netem-vocab-freq.json（5530 词，含释义/分类），来自 [exam-data/NETEMVocabulary](https://github.com/exam-data/NETEMVocabulary)，数据许可 CC BY-NC-SA 4.0（非商业用途）。
- **dictionaries/wordbooks/**：词源单词本 CET4/CET6/TEM8 三册（PDF+TXT 词条表），来自 [openetymology/OpenEtymology](https://github.com/openetymology/OpenEtymology)，词书文件许可 CC BY-SA 4.0。专八方向的可用开放资料：TEM8 分册覆盖专八词表（词源、词根拆解）；专八历年真题无公开开放仓库，未收录。

用途边界：papers/cet4、papers/cet6 文本与 papers/exams 同为框架挖掘与出题素材；papers/kaoyan 手译版与 dictionaries/wordbooks 是阅读型参考书，不进入学习库、不计入词汇导入统计。各仓库均为考试回忆/社区整理版，不宣称与官方发行版逐字一致。

## 其他语料目录

- `materials/vocabulary/zhenghaoyang24-voc/`：voc14w 例句语料（github.com/zhenghaoyang24/english-vocabulary），框架章「语料」标注例句的来源。
- `materials/corpus/opus-opensubtitles/`：OPUS OpenSubtitles 英中平行语料（约 1.5GB），备用的真实语境语料，尚未入库使用。
- `materials/dictionaries/`：ECDICT、WordNet、Kaikki/Wiktionary 数据，见 dictionaries-2026-09-15.md。
