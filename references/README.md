# 词汇资料与词表导入

词表下载、选源与归一化的**规则**见 [materials/HANDBOOK.md](../materials/HANDBOOK.md)（2026-09-16 定版，唯一规则处）；资料清单与批次记录见 [materials/README.md](../materials/README.md) 与 [engineering/archive/downloads-batches-2026-09.md](../engineering/archive/downloads-batches-2026-09.md)。本页只保留与**词表导入学习库**直接相关的操作说明和质量边界。

本次任务日期：2026-09-14。

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

复现脚本：import_wordlists.py。先用 --dry-run 核对数量与格式，再用 --database 指向隔离数据库试导入。正式操作会保存备份、比较学习事件前后是否一致、检查SQLite完整性。重复导入测试与页面回归见 engineering/verification/wordlists-import.md（2026-09-16 自 site/verification 迁入）。
