# 学习资料总库（materials）

本目录汇集项目从 GitHub 等公开渠道下载的全部原始学习资料，2026-09-16 起按类型分类存放。数据文件不入 git，来源、字节数与 SHA-256 哈希逐条登记在同目录 [downloads-manifest.json](downloads-manifest.json)（files 列表，共 153 条）。**下载、选源与归一化规则唯一出处是 [HANDBOOK.md](HANDBOOK.md)**（2026-09-16 定版），本页只是资料清单与批次记录：左侧目录看到的是文档，文件本体在本机 materials/ 下。

## vocabulary/ — 词表与词汇语料

| 内容 | 说明 |
| --- | --- |
| CET4/CET6/TEM8 `_T.json` 与 `-rich.jsonl` | 四级 4544 词、六级 3991 词、专八 12410 词（KyleBing/english-vocabulary，上游 kajweb/dict）；已于 2026-09-14 导入学习库 |
| NGSL-1.2-community.json | 高频核心词 2809（社区镜像，CC BY-SA 4.0） |
| FCE/PTE-phrases-community.json | 备选词组表，未导入 |
| Qwerty-dictionary-index.ts、Qwerty-LICENSE.txt、KyleBing-format.md、upstream-kajweb-README.md | 来源格式说明与许可文件 |
| zhenghaoyang24-voc/ | voc14w 例句语料 14.1 万句；句式骨架章「语料」标注例句的来源 |
| IELTS-rich.jsonl | 雅思词表 7002 词（KyleBing/english-vocabulary，上游 kajweb/dict 雅思词书；rich 格式与 CET4/CET6/TEM8 同构，含音标/中译/词组/双语例句），未导入 |
| IELTS-wordlist-fanhongtao.txt | 《雅思词汇词根+联想记忆法（乱序便携版）》手抄词表 3722 行（fanhongtao/IELTS，含音标与中文释义），未导入 |

## dictionaries/ — 词典数据

ecdict（ECDICT 全量，英英/中文释义、词频、考试标签；2026-09-21 瘦身已删 repo/.git 与未用的 stardict.7z）、wordnet（Princeton WordNet 3.0 已解包）、wordbooks/（词源单词本 CET4/CET6/TEM8 三册 PDF+TXT，CC BY-SA 4.0；专八真题无公开开放仓库，词表方向以 TEM8 分册覆盖）。kaikki-wiktionary 已删（部分下载残件 1.1GB，详见 references/dictionaries-2026-09-15.md）。

## papers/ — 真题与参考书

- exams/：9 份真题 PDF+txt（四级 2022-06、六级 2018-06、考研英一 2017-2019、英二 2016-2019）+ 2020 英一 OCR 版 txt（扫描件经 pytesseract 识别，头部中文识别不可靠，正文英文质量可用）
- cet4/：四级 2024-06、2025-06 各 3 套 PDF+txt（0609x/CET46-Resources）
- cet6/：六级 2016-2026 规整 TXT 62 份（AndrewYuZhenYu/cet6_exam_questions_txt_collection），可直接用于句式骨架挖掘
- kaoyan/：考研英一手译版 5 册（1986-2020，m2kar/KaoYan-English，中文层无 ToUnicode 映射不可机读，留作原件阅读）+ 考研词频表 5530 词（exam-data/NETEMVocabulary，CC BY-NC-SA 4.0 非商用）
- kaoyan-jingfan/：考研英一 2005-2026 阅读精翻 22 份 markdown（Destinnnnn/kaoyan-english-1-2005-2026）——逐句原文+精译+词汇搭配+长难句拆解，手译版的机读替代层
- ielts/：雅思资料 22 件（zeeklog/IELTS）——剑桥雅思真题 4-18 全 15 册 PDF + IELTS16 官方体验版 + 考试介绍 3 件 + 剑桥19 图表作文范文 3 篇；听力音频（mp3/m4a 共 238 个）按需再取未收录。真题 PDF 为社区整理版，不宣称与官方发行版逐字一致。**已归一化（2026-09-16）**：文字层分级实测——剑4/9/14/IELTS16体验版 4 件文字层完好（pdftotext -layout 派生 txt+md，完整英文句合计 4,660 条；剑9 含沪江水印中文噪音、剑14 为 OCR 嵌入层约 36 处 i/l 混淆），剑5-8/10-13/15-18 共 12 册为扫描件不可机读，登记为「人读原件，不进挖掘/导入管线」；词表 fanhongtao txt 转原件旁 md；真题/资料合集入 materials/readable/papers/（雅思真题合集 + 雅思资料合集）

## textbooks/ — 初高中教材

- 初中人教版/：5 册 Markdown 全文（约 1.2MB，chncaesar/ChinaTextbook-Text，无 LICENSE 仅本地学习用）——人教《Go for it!》七上/七下/八上/八下/九年级全一册；正文真实完整（五册合计约 7500 行成段英文课文），含目录/版权页噪音与常见 PDF 断行（"Y ou"/"att ention"），精确匹配前需归一化。合集阅读版见 readable/textbooks/初中英语教材合集.md（原件不入目录）。
- 高中人教版2019/：textbook_sentence_index.json（29MB 解压物，ZhangYixuan-in-BUPT/textbook-sentence-index，MIT）——人教/沪教/译林/外研四版本 × 7 册层级句子倒排索引，去重后 30,110 句（人教 8,523 句），每句带版本/册别/单元出处；pep-senior-vocab.json（2,569 词条，lfcypo/pep-senior-eng-vocab-json，无 LICENSE 仅本地用）。教材句式骨架回收（07 章）的原始语料。

## readable/ 与 wordbooks-md/ — 可读层（前端可见）

生成物（可重跑重建，不手改）：`readable/` 由 normalize_materials.py 生成——四/六/考研真题合集、考研精翻合集、雅思真题/资料合集、初中教材合集、词源书说明与索引页；`dictionaries/wordbooks-md/` 由同一脚本生成——词源书三册各一合集（etymology-cet4/cet6/tem8.md，共 9986 词条，按词目字母排序）。papers/ 真题 txt 与 textbooks/ 教材原件另有原件旁同名 md（数据层派生物，不入目录避免与合集重复）。合集页与词源书合集在左侧目录「学习资料」分组可见；数据层原件（-full.txt、PDF、官方精简 txt）存 wordbooks/。json/csv/jsonl 结构化数据按 [HANDBOOK](HANDBOOK.md) 豁免不转 md。

边界：模拟题为版权教辅无开放语料，未收录；各真题为考试回忆/社区整理版，不宣称与官方发行版逐字一致；完形填空空格以 ___ 保留。

## corpus/ — 平行语料

opus-opensubtitles/：OPUS OpenSubtitles 英中平行语料（约 1.5GB），口语语域的真实语境备用语料，尚未入库使用。

## 使用边界

papers/ 的文本语料服务于句式骨架挖掘与出题；kaoyan 手译版与 wordbooks 是阅读型参考书；词表已导入部分以学习库为准，本目录是可复核的原始件。收藏/下载规模不代表学习进度，也不构成掌握证据。

2026-09-16 雅思批次（+24 件）：词表两件（IELTS-rich 7002 词、fanhongtao 3722 行）+ 剑桥真题 4-18 PDF + 作文案例文本。同批修复：22 条考研精翻条目的 manifest 路径双重前缀（materials/materials/→materials/）。

2026-09-16 雅思归一化（normalize_materials.py ielts，可重跑幂等）：15 册真题逐册文字层分级（完整英文句计数 + 混淆词检测），4 册派生 txt+md，12 册扫描件如实标注不派生；fan 词表转 md；可读层 11 页（catalog 已验证可见，服务端 8 项回归全过）。哈希以原件为准，派生物不登记。
