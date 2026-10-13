# 学习资料总库（materials）

## 2026-10-08 · TED 100 篇英文原文 TXT

按用户要求仅保留带基本信息的 TXT：100 篇、236,186 个空白分词，位于 `corpus/ted/english/`。各篇开头含中英文标题、讲者、年份、时长、TED ID 与官方来源链接；正文按官方段落合并字幕断行，文字不改写。旧 JSON、SRT、VTT 已清理，来源与 TXT 哈希保留在 manifest；[选材目录](<../course/原文与参考资料/原文、教材与影视/TED 英语选材目录：100 个演讲与对谈.md>) 与 [TXT 清单](<../course/原文与参考资料/原文、教材与影视/TED 英语选材目录：100 个演讲与对谈.md>) 可查文件。084 官方时长差异在文首备注，尚未逐条听校。

## 2026-10-08 · GovInfo 总统演讲扩充：五位总统、19 篇

新增 15 篇，现在共 **19 篇、55,069 个空白分词、1,286 个本地段落**。覆盖克林顿 3 篇、小布什 3 篇、奥巴马 4 篇、特朗普 4 篇、拜登 5 篇；包含就职、告别、国情咨文、危机应对、纪念与每周讲话。原件统一来自 GovInfo，HTML 与带中英文姓名／日期／标题／官方编号／出处的 TXT 位于 `corpus/presidential-speeches/govinfo/`，在 [可读原文合集](../course/原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md) 按总统和日期查看完整索引。

代表内容：克林顿 1993／1997 就职与 2001 告别；小布什 2001／2005 就职与九一一当晚讲话；奥巴马 2009／2013 就职、2015 塞尔玛纪念、2017 告别演讲前的每周讲话（不是 1 月 10 日告别演讲本身）；特朗普 2017／2025 就职、2020 拉什莫尔山庆典、2025 国会讲话；拜登 2021 就职、2023 民主讲话、2024 国情咨文与大选后讲话、2025 告别。

新增 15 件原文已登记下载直链、字节与 SHA-256。生成脚本兼容旧版 PPP 的预格式文本，去除页码标记并合并排版断行；没有采用 PDF/OCR，也不自动纠正官方实录中的字词。新下载属于待选学习素材，尚未逐篇提取 chunks；已有 [20 条精选](<../course/Chunks 收集/总统演讲 Chunks：坚持原则、澄清判断与回应挫折.md>) 仍来自首批四篇，未增加用户掌握记录。

## 2026-10-08 · GovInfo 总统演讲首批

下载 4 篇官方 HTML 原文：拜登 2024-11-07 大选后讲话、2023-09-28 民主与麦凯恩讲话、奥巴马 2009-01-20 就职演说、特朗普 2017-01-20 就职演说。原件位于 `corpus/presidential-speeches/govinfo/`，逐件字节与 SHA-256 已登记 manifest；优先原生 HTML，未采用 PDF/OCR。派生 TXT 和 [可读原文合集](../course/原文与参考资料/原文、教材与影视/总统演讲原文合集：GovInfo.md)由 `references/build_presidential_speeches.py` 重建，保留停顿、观众反应和官方修正；211 个本地段落、9,685 个空白分词。通读后 [精选 20 个 chunks](<../course/Chunks 收集/总统演讲 Chunks：坚持原则、澄清判断与回应挫折.md>)，原句逐字校验，并加入 Chunks 收集箱。政治陈述作为语言素材，不作事实背书；第三方引文的权利边界见 [GovInfo 政策](https://www.govinfo.gov/about/policies)。

资料网站及具体操作见 [资料来源](../course/编纂与维护/资料来源.md)：包含 SubtitleCat 的英文字幕搜索、下载与质量检查方法，以及 OpenSubtitles、Addic7ed 的电影／剧集入口。

本目录汇集项目从 GitHub 等公开渠道下载的全部原始学习资料，2026-09-16 起按类型分类存放。数据文件不入 git，来源、字节数与 SHA-256 哈希逐条登记在同目录 [downloads-manifest.json](downloads-manifest.json) 的 files 列表；部分历史原件已归档或删除。**下载、选源与归一化规则唯一出处是 [HANDBOOK.md](HANDBOOK.md)**（2026-09-16 定版），本页只是资料清单与批次记录：左侧目录看到的是文档，文件本体在本机 materials/ 下。

> **2026-09-24 收录范围收窄**：站点收敛为纯查看器后，与学习库/词典库配套的原始数据移至 `~/workspace/english-archive/`——`vocabulary/`（词表）与 `dictionaries/`（ecdict/wordnet/wordbooks）已移出（wordbooks-md 词源书合集的可读层随 dictionaries 移走；恢复见 [wordlists-guide.md](wordlists-guide.md)）；剑桥雅思真题 PDF（351M）移至 `english-archive/ielts-pdfs/`；opus 语料的 zip 压缩包与 ids 对齐文件已删（与解压文本重复）。本目录现存：readable/ 合集（站点在用）、papers/ 文本真题、textbooks/ 教材、corpus/ 平行语料（.en/.zh）。下文各节为移出前的历史记录，保留原貌。

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

## corpus/ — 平行语料与影视字幕

2026-10-08 六部剧批次：新增《绝命毒师》5 季 62 集、《风骚律师》6 季 63 集、《生活大爆炸》12 季 279 集、《马男波杰克》6 季 76 集正片、《百年酒馆》10 集、`This Is Us` 6 季 106 集的英文字幕，合计 **596 份 UTF-8 SRT、314,564 条时间码字幕**。逐季补漏、替换非 SRT 候选、普通／SDH 去重；《百年酒馆》S01E04 是网页英文原文与同页已有时间轴对应的恢复版，需视频复核。保存位置、来源、检查及重建方式见 [六部剧下载清单](../course/原文与参考资料/原文、教材与影视/六部剧英文字幕：绝命毒师、风骚律师等.md)。

2026-10-08 口语学习推荐六部批次：新增《The Intern》《The Good Place》《Superstore》《Ted Lasso》《Shrinking》《About Time》的英文字幕，按已播范围与剧集标题核对后，整理为 **242 份 SRT、148,283 条时间码字幕**。电视剧按季保存于 `tv-subtitles/<作品>/`，电影位于 `movie-subtitles/<作品>/`；保留 20 个原始 ZIP、四份目录快照与出处索引。普通／SDH 版本去重，补《爆笑超市》奥运篇，明确处理两部剧的双集首播编号；完整覆盖、文件路径与重建方式见 [六部作品下载清单](../course/原文与参考资料/原文、教材与影视/六部口语学习作品：英文字幕下载清单.md)。

tv-subtitles/modern-family/：2026-10-08 下载《摩登家庭》11 季英文字幕，按正片集目录覆盖 **250 集**。整理为 **249 份 UTF-8 SRT**，S11E17–E18 为一份双集大结局字幕；12 个原始 ZIP 和目录快照保留，可追溯成员名、版本与哈希。第三季首个候选包缺 E24 且 E04 格式异常，已换用完整替代包。逐季覆盖和处理边界见 [摩登家庭字幕清单](<../course/原文与参考资料/原文、教材与影视/摩登家庭英文字幕：11 季覆盖清单.md>)，逐文件信息见 [字幕索引](../references/subtitles/modern-family-index.json)。尚未按用户视频核同步或逐句听校；下载不代表学习掌握。

opus-opensubtitles/：OPUS OpenSubtitles 英中平行语料（约 1.5GB），口语语域的真实语境备用语料，尚未入库使用。

standup-subtitles/george-carlin/：2026-10-08 从 SubtitleCat 下载的 4 份**英文原始 SRT**，供口语 chunks 选材和带时间码回查。按原件保存，不转成站点文章，也不并入已有的通用影视平行语料：

| 演出 | 本地文件 | 字幕条数 | 覆盖至 |
|---|---|---:|---:|
| Again! (1978) | `again-1978.en.srt` | 1,515 | 1:19:41 |
| Doin' It Again (1990) | `doin-it-again-1990.en.srt` | 1,389 | 0:58:23 |
| Back in Town (1996) | `back-in-town-1996.en.srt` | 953 | 1:01:34 |
| It's Bad for Ya (2008) | `its-bad-for-ya-2008.en.srt` | 1,288 | 1:07:52 |

四份均为社区上传字幕，页上未见明确许可；仅本地个人学习使用，不再分发。已核对连续编号、时间码、UTF-8 可读性与两两文本重叠（8 词连续片段交集不超过较短文件的 0.16%）。字幕可能有听写错误，引用到正式教材前仍需对照原演出；来源页、下载直链和 SHA-256 见 manifest。

movie-subtitles/before-trilogy/：2026-10-08 从 SubtitleCat 下载爱在三部曲的 3 份英文 SRT，原始字节保持不变，用于对白阅读、口语 chunks 选材及时间码回查：

| 电影 | 本地文件 | 字幕条数 | 覆盖至 |
|---|---|---:|---:|
| 爱在黎明破晓前 / Before Sunrise (1995) | `before-sunrise-1995.en.srt` | 1,453 | 1:42:00 |
| 爱在日落黄昏时 / Before Sunset (2004) | `before-sunset-2004.en.srt` | 2,278 | 1:18:39 |
| 爱在午夜降临前 / Before Midnight (2013) | `before-midnight-2013.en.srt` | 1,905 | 1:44:18 |

三份文件均能完整解析为字幕块，时间码起点不倒退，UTF-8 解码无损坏。《Before Sunrise》含首尾推广字幕，末条推广重复使用编号 1452；《Before Sunset》从编号 0 开始，首条时间码小时为一位数字；后两部含 SDH 式声音／音乐说明及字幕组署名。这些噪音已记入 manifest 的 quality_notes，提取对白时应排除；没有对照用户的视频版本做同步校验。社区资料未发现明确开放许可，仅本地个人学习，不再分发。

## 使用边界

papers/ 的文本语料服务于句式骨架挖掘与出题；kaoyan 手译版与 wordbooks 是阅读型参考书；词表已导入部分以学习库为准，本目录是可复核的原始件。收藏/下载规模不代表学习进度，也不构成掌握证据。

2026-09-16 雅思批次（+24 件）：词表两件（IELTS-rich 7002 词、fanhongtao 3722 行）+ 剑桥真题 4-18 PDF + 作文案例文本。同批修复：22 条考研精翻条目的 manifest 路径双重前缀（materials/materials/→materials/）。

2026-09-16 雅思归一化（normalize_materials.py ielts，可重跑幂等）：15 册真题逐册文字层分级（完整英文句计数 + 混淆词检测），4 册派生 txt+md，12 册扫描件如实标注不派生；fan 词表转 md；可读层 11 页（catalog 已验证可见，服务端 8 项回归全过）。哈希以原件为准，派生物不登记。
