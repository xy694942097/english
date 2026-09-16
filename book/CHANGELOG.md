# 编纂记录

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
