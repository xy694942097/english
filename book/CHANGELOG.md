# 编纂记录

## 2026-09-16 · 雅思资料归一化（normalize_ielts.py）

按总则「文字层完好的 PDF 收下不算完成，必须当场派生并抽查」执行：新脚本 references/normalize_ielts.py（可重跑幂等已验证）——①15 册剑桥真题逐册文字层分级（pdftotext 全文抽取 + 完整英文句计数 + 混淆词检测）：剑4（1,005 句/无瑕疵）、剑9（1,599 句/沪江水印中文噪音 9.3 千字）、剑14（1,943 句/OCR 嵌入层 36 处 i/l 混淆如 invoIves）、IELTS16 体验版（113 句）四件文字层完好，派生 txt+原件旁 md+可读层页；剑5-8、10-13、15-18 共 12 册为扫描件（含「扫描全能王」水印、个别只有沪江推广水印），如实登记「人读原件，不进挖掘/导入管线」，不做 OCR 硬转。②fanhongtao 词表 txt 转原件旁 md（代码块包裹保排版）。③可读层 11 页入 materials/readable/papers/ielts/（4 册真题+3 作文范文+考试介绍 3 件+词表索引页），运行中服务 catalog 实时发现验证通过，服务端 8 项回归全过。manifest 哈希以原件为准，153 条全量复验通过，派生物不登记。

## 2026-09-16 · 雅思资料批次（+24 件，为后续编纂备料）

按用户指令搜集雅思资料入库，manifest 现 153 条全量 SHA-256 复验通过。词表两件：IELTS-rich.jsonl 7002 词（KyleBing/english-vocabulary sentence 版，与 CET rich 同构可直接进导入管线）、IELTS-wordlist-fanhongtao.txt 3722 行（新东方乱序版手抄词表）。真题与参考 22 件（zeeklog/IELTS）：剑桥雅思真题 4-18 全 15 册 PDF + IELTS16 官方体验版 + 考试介绍 3 件 + 剑桥19 图表作文范文 3 篇；听力音频 238 个未收录（用户明确）。选源级别如实登记：真题 PDF 属「文字层完好的 PDF」，用于挖掘前须先派生 txt 并抽查。同批修复：22 条考研精翻 manifest 路径双重前缀（materials/materials/→materials/，哈希复验通过）。materials/README.md 更新（共 153 条）。

## 2026-09-16 · 文本类资料全量 Markdown 化

按用户定版（纯文本全转 md，json/csv/jsonl 豁免）：新脚本 references/normalize_text_to_md.py——①papers/ 全部 78 个真题 txt（含 OCR 版）转原件旁同名 md，带来源头与质量边界注记；②词源书三册全文按词目首字母分册转 materials/dictionaries/wordbooks-md/（77 册，四级 4283/六级 2109/专八 3594 共 9986 词条，词条判定经音标行核验、中文行误匹配已修，单册 ≤440KB）。catalog 白名单更新为层级精确匹配（顶层/readable/textbooks/wordbooks-md 三级），test_server 夹具与断言扩充（词源分册可见、papers 原件 md 与第三方 README 屏蔽），8 项全过；浏览器验证词源分册渲染正常（264 词条+目录）。总则与 AGENTS.md 同步更新。json/jsonl/csv（词表/词频表/句子索引/ECDICT）按有损降维理由豁免，查询走学习库与脚本。

## 2026-09-16 · 下载与归一化总则定版

按用户要求把本轮沉淀的规则写入文档，后续下载不再临场决策：references/README.md 顶部新增「下载与归一化总则」——下载原则（优先公开仓库/官方平台、gh api 探仓+raw 直链、manifest 唯一登记处、许可记录、优先文本原生格式、质量差换源不硬转、边界如实披露）、目录分类（按形态与用途五类）、归一化规则（数据层原件不改写/派生物放原件旁哈希以原件为准/可读层走 build_materials_readable.py 生成/catalog 放行范围与测试同步/批量前先抽查质量）。AGENTS.md 目录体系补 materials/ 条目、排除扫描说明更新（materials 只扫顶层 md 与 readable/ 子树），「记录与边界」节新增执行摘要条目。同时补记：初高中教材语料已于本轮前段入库（materials/textbooks/：初中人教 5 册全文 md、高中句子倒排索引 30110 句 MIT、人教高中词汇表 2569 词）。

## 2026-09-16 · materials 归一化：可读层 + PDF 数据层

数据层与可读层分两线归一。可读层：新脚本 references/build_materials_readable.py 把 papers/ 全部真题文本转成 materials/readable/ 下 46 页 md（真题 22 页、考研英一阅读精翻 22 页、词源书说明、索引页），catalog 放行 readable/ 子目录，「学习资料」组在前端可见；test_server 用例同步，8 项全过。数据层：下载考研英一 2005-2026 阅读精翻 22 份 md（Destinnnnn/kaoyan-english-1-2005-2026，逐句原文+精译+搭配+长难句拆解，已登记 manifest，现 122 条）；2020 英一扫描卷经 pytesseract OCR（8 页 2.6 万字符，英文正文可用、中文头部不可靠）；词源书三册经 pdftotext -layout 提取全文（etymology-*-full.txt，共约 850 万字符，含词源叙述与双语例句——官方精简 txt 只是裸词表）。诚实边界：手译版 5 册中文层无 ToUnicode 映射不可机读，留作原件阅读，机读层由精翻替代；PDF skill 的 OCR 层仅英文模型可用（lang=eng）。

## 2026-09-16 · materials 接入左侧目录

materials/ 从 catalog 排除名单移出：server.py 新增分组规则（section=reference、group=学习资料），只发现顶层 md、屏蔽子目录第三方 README（ecdict 仓库说明等）；新建 materials/README.md 作为浏览索引（四类目录内容、来源、许可与使用边界）；.gitignore 白名单放行该 README；前端 app.js 参考资料节改为嵌套子分组渲染，「学习资料」单独可见。新增 test_server 用例（materials 索引发现+第三方 README 排除），8 项回归全过；4174 已重启，浏览器验证侧边栏与页面渲染正常。

## 2026-09-16 · 资源目录重组：materials/

按用户指令新建项目根目录 materials/，将 references/downloads/ 全部下载资源（约 1.4GB）按类型分类迁入：vocabulary/（词表 JSON/JSONL、NGSL、FCE/PTE 词组、Qwerty 索引、zhenghaoyang24-voc 例句语料）、dictionaries/（ECDICT、WordNet、Kaikki、词源单词本 wordbooks）、papers/（exams、cet4、cet6、kaoyan 真题与手译）、corpus/（OPUS OpenSubtitles 英中平行语料，此前未登记）。manifest 迁为 materials/downloads-manifest.json，100 条 file 路径全部改写并逐条复验 SHA-256 通过。引用同步更新：.gitignore（materials/* 入库白名单仅 manifest）、site/server.py catalog 排除目录、import_wordlists.py / import_voc_examples.py / build_combined_dictionary.py 脚本路径、references/README.md、dictionaries-2026-09-15.md、08-frames/09-exam-recall.md、00-guide.md、site/verification/wordlists-import.md、engineering/design/frames-plan-v1.md；08-frames-collection.md 已重建。历史记录（imports 报告、当日 CHANGELOG 条目）保留原路径作为当时事实。

## 2026-09-16 · 考试参考资料库（四六级/考研/专八）

按用户指令从 GitHub 公开仓库补充下载 81 个参考文件至 references/downloads/ 四个新目录：cet4/（2024-06、2025-06 各 3 套真题 PDF+txt 抽取，0609x/CET46-Resources）、cet6/（2016-2026 真题规整 TXT 62 份，AndrewYuZhenYu/cet6_exam_questions_txt_collection）、kaoyan/（英一手译版 5 册+2020 真题，m2kar/KaoYan-English；考研词频表 5530 词，exam-data/NETEMVocabulary，CC BY-NC-SA 4.0）、wordbooks/（词源单词本 CET4/CET6/TEM8 三册 PDF+TXT，openetymology/OpenEtymology，CC BY-SA 4.0）。全部登记 downloads-manifest.json（files 列表现 100 条）并全量 SHA-256 校验通过。边界：专八真题无公开开放仓库，仅以 TEM8 词源分册覆盖词表方向；手译版与词书为阅读参考，不进学习库。详见 references/README.md「考试参考资料库」节。

## 2026-09-16 · 真题回收：四六级考研句式框架

接入第三条扩编来源（真题语料）：从 GitHub 公开仓库下载 9 份历年真题 PDF（四级 2022-06、六级 2018-06、考研英语一 2017/2018/2019、考研英语二 2016/2017/2018/2019，约 22 万字符文本），原件与 .txt 抽取存 references/downloads/exams/，SHA-256 与下载 URL 登记于 references/downloads-manifest.json。对新章 08-frames/09-exam-recall.md 用正则初筛约 60 个候选模式、人工核对语境后登记 7 个框架：as long as 条件句、rather than 平行、end up 补语三型、it turns out、when it comes to、be likely to、even if/even though。每框架附 2-3 条真题原句（标注试卷出处）+ 结构拆解 + 常见误读，章尾 4 题新语境练习（答案标注自造）。边界披露：模拟题未收录（公开渠道多为版权教辅，无开放语料）；完形填空空格以 ___ 标出不作填补；频次结论仅限 9 卷样本。已登记 00-guide 索引（真题回收节，扩编规则改为三条来源）、接入 course.json 句式框架专题（10 课）。回归：site/test_server 7 项、site/test_learning 7 项全过，catalog 与浏览器渲染已验证。

## 2026-09-16 · 教材回收：初高中句式框架

依课标语法项目表（义教 2022 + 高中 2017/2020 带星分级）回收 7 个初高中框架入索引：not only…but also（含倒装）、so/such…that、too…to、either/or 与 neither/nor、the more…the more、no sooner…than 与 hardly…when、would rather…than。新章 08-frames/07-school-recall.md，按风格A编写；除标注（自造）的仿写示例外，例句均取自 voc14w 语料并标注（语料）。来源边界：未逐册扫描教材文本，以课标项目为纲，链接见章首披露。已接入 course.json 句式框架专题。

## 2026-09-15 · 专题课程

根据用户关于“知识没有重点”的纠正，将教学主线改为五类知识专题。复用7个已写章节，新增4章，共11章进入主线；其余材料保留作延伸和查阅。

新增nothing but/anything but/all but、not until、陌生句形、take专题。每章以情境进入，解释结构与区别，附迁移练习和折叠答案；重点用法来源见正文。

课程导航存放book/course.json，支持显式指定语法知识点类型。没有学习者新答题，不改变既有学习或复习记录。

## 2026-09-14 · B0002

按用户“扩充四、六级词汇、例句、词组，尽量详细”的请求，新增 8 个主题章和 2 个查阅入口。共48个独立核心词、144个编号英汉例句、192项主搭配说明、8段章首语境、32道迁移练习与相应解析；词族、附加结构和索引重复不计入核心词数。

新增章节：熟悉动词、证据与结论、因果、介词结构、变化与持续、程度与效果、评估与论证、抽象义深化。涵盖原候选 qualify、entertain、register、inform。

关键难点义项参考 Collins 与 Oxford 实际查阅页面，链接与核查范围保存在词条及学习路线页。全部教学例句自造，没有标成真题；未宣称完成官方词表覆盖或逐词频次统计。

Book 现有12个教学章，另有导览、背景和索引等页面。没有新增学习者答题，不改变掌握等级。

## 2026-09-14 · B0001

建立可恢复的学习档案与方法论，编入 4 个教学章：语境阅读方法、resigned、证据与分歧、进展与效果。材料包含 11 个重点表达；内容准备完成不代表学习者掌握。

保留早期 vocabulary/Lesson 001 为历史课堂材料，不用其已讲例句作独立摸底。
