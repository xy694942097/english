# 学习资料总库（materials）

本目录汇集项目从 GitHub 等公开渠道下载的全部原始学习资料，2026-09-16 起按类型分类存放。数据文件不入 git，来源、字节数与 SHA-256 哈希逐条登记在同目录 [downloads-manifest.json](downloads-manifest.json)（files 列表，共 100 条）；来源说明、许可与质量边界的完整版见 [references/README.md](../references/README.md)。本页是浏览索引：左侧目录看到的是文档，文件本体在本机 materials/ 下。

## vocabulary/ — 词表与词汇语料

| 内容 | 说明 |
| --- | --- |
| CET4/CET6/TEM8 `_T.json` 与 `-rich.jsonl` | 四级 4544 词、六级 3991 词、专八 12410 词（KyleBing/english-vocabulary，上游 kajweb/dict）；已于 2026-09-14 导入学习库 |
| NGSL-1.2-community.json | 高频核心词 2809（社区镜像，CC BY-SA 4.0） |
| FCE/PTE-phrases-community.json | 备选词组表，未导入 |
| Qwerty-dictionary-index.ts、Qwerty-LICENSE.txt、KyleBing-format.md、upstream-kajweb-README.md | 来源格式说明与许可文件 |
| zhenghaoyang24-voc/ | voc14w 例句语料 14.1 万句；框架章「语料」标注例句的来源 |

## dictionaries/ — 词典数据

ecdict（ECDICT 全量，英英/中文释义、词频、考试标签）、wordnet（Princeton WordNet 3.0 已解包）、kaikki-wiktionary（Wiktionary English 全量 JSONL，部分下载约 36.5%，未完成不可作已完成来源）、wordbooks/（词源单词本 CET4/CET6/TEM8 三册 PDF+TXT，CC BY-SA 4.0；专八真题无公开开放仓库，词表方向以 TEM8 分册覆盖）。详见 references/dictionaries-2026-09-15.md。

## papers/ — 真题与参考书

- exams/：9 份真题 PDF+txt（四级 2022-06、六级 2018-06、考研英一 2017-2019、英二 2016-2019），真题回收章 09-exam-recall 的首批语料
- cet4/：四级 2024-06、2025-06 各 3 套 PDF+txt（0609x/CET46-Resources）
- cet6/：六级 2016-2026 规整 TXT 62 份（AndrewYuZhenYu/cet6_exam_questions_txt_collection），可直接用于框架挖掘
- kaoyan/：考研英一手译版 5 册（1986-2020，m2kar/KaoYan-English）+ 2020 真题纯卷 + 考研词频表 5530 词（exam-data/NETEMVocabulary，CC BY-NC-SA 4.0 非商用）

边界：模拟题为版权教辅无开放语料，未收录；各真题为考试回忆/社区整理版，不宣称与官方发行版逐字一致；完形填空空格以 ___ 保留。

## corpus/ — 平行语料

opus-opensubtitles/：OPUS OpenSubtitles 英中平行语料（约 1.5GB），口语语域的真实语境备用语料，尚未入库使用。

## 使用边界

papers/ 的文本语料服务于框架挖掘与出题；kaoyan 手译版与 wordbooks 是阅读型参考书；词表已导入部分以学习库为准，本目录是可复核的原始件。收藏/下载规模不代表学习进度，也不构成掌握证据。
