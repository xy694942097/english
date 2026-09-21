# 当前学习状态

更新：2026-09-16。

## 工程根本目标（2026-09-16 用户明确）

这个工程不是给所有人用的，仅仅给用户自己用。目的是**真正"学会"英语**，而不是仅仅学几个词汇、几个词组。为此可能需要花很多时间分析：什么是"学会"英语、学不会英语的原因有哪些，或许还需要测试问卷/系统来分析使用者欠缺的能力、不擅长什么、如何补齐。所以这个工程不只是学习系统。

（背景备注：截至目前工程建造投入很大，但真实学习记录为零——events/progress 均为空。后续工作应回到真实学习行为与能力诊断本身，而不是继续横向加功能。）

- 自选篇建立（2026-09-18，用户指令）：18-self-picked.md 手动收录活页章上线——日常撞见即收、不设 7 条红线、来源标（自选）不要求反查；首个条目 less about…and more about（重新定焦）。三脚本 CHAPTERS 补齐（含并行会话的 16/17 小说通读章），管线一致，回归全过，前端 17 章可见。
- 四级篇返工（2026-09-18，评审后整改第一批）：13-cet4-readthrough 按定版标准重做——旧 9 条重裁留 2 砍 6 存疑 1，重挖 27 候选取 5 入章（anything to go by / anything but / few 隐性最高级 / It's not that 归因纠正 / You might think 设靶预判），每条补语域/频次/产出侧三件套，例句逐字出真题。27 条 candidate 存 references/mining/cet4-restandard.frames.json 待族章分流。管线重跑一致，8 项回归全过。待办：09/12 章同标准重裁、07 章降级裁决。
- 四级章补编（2026-09-21，用户指令）：四级「少」系 09-18 返工有意收紧+大量候选存档未编。本次候选全裁决：13 章 7→29 骨架 + 26 条短语档，35 例句逐字校验 0 不一致；00-guide/course.json 旧计数修正；09-18 返工未提交工作一并入库。
- 六级章补编（2026-09-21，用户指令「6级的开始」）：116 条存档候选全裁决，14 章 19→66 骨架 + 15 短语（68 例句逐字校验 0 不一致）；cascade_final 六级 candidate 清零（47A/5B/64skip）。
- 考研章补编（2026-09-21，用户指令「继续」）：89 条存档候选全裁决，15 章 21→60 骨架 + 10 短语（含 It is all very well…but、I'd be lying if I said、It is a [adj] N that 反语让步等）；A 类未编 4 条复审（1 入章 3 判已编族/语法层，Now comes word that 例并入 ##12 变体注）；cascade_final 考研 candidate 清零（A:61/B:10/skip:46）。真题通读线（四/六/考研）存档候选全部清零，三真题章合计 155 骨架。
- 结构重排（2026-09-21，用户指令「同时动」，目标「简单」）：book 四个单章目录归拢（02-chunks→01-reading、07-word-topics→03-四六级词汇、06-sentences→05-patterns、04-词表资料→materials/wordlists-guide.md），course.json 6→5 专题零单章；侧边栏「参考资料」撤销（工程记录入工程侧「导入与挖掘记录」），学习资料=materials+历史课堂，CURRENT 移入进度与诊断；00-guide 补小说通读/自选篇索引+三条系列线说明；frames 冒烟 h1 断言 15→16 旧账修复。全部回归过、浏览器实测过。
- 仓库瘦身（2026-09-21，用户指令「精简瘦身」）：逐项核实引用后删——kaikki 部分下载残件 1.1G（零脚本消费、残件不可用）、ecdict repo/.git 72M（哈希已记录）、stardict.7z 49M（与 csv 重叠、零引用）、空嵌套 references/references/ 与 __pycache__×2。materials 3.3G→2.1G。保留核实：opus 1.5G（回填待用）、全部可复现导入/归一脚本、llm_batches 裁决证据链。文档同步（下载记录页/materials README/CHANGELOG），19+1 测试全过、管线重跑一致、站点实测更新后页面已生效。
- 术语定版（2026-09-17，用户指令）：全项目「框架/句式框架」更名「句式骨架」——course.json、08-frames 全章、AGENTS、HANDBOOK、methodology（含什么是框架.md→什么是句式骨架.md）、frames-plan、三个生成脚本、frame-miner skill 均已改；侧边栏组名同步；生成管线重跑一致，8 项回归全过，前端零残留。frame-miner/08-frames/frames.json 等技术标识符保留原名。
- 学习资料合集化（2026-09-16，用户指令）：可读层从 142 条碎页收敛到 14 条合集——词源书 77 分册→每册一合集（按词目字母排序）、四/六/考研真题各一合集、考研精翻 22 份合一、雅思真题/资料各合一、初中教材 5 册合一（textbooks 原件退出目录）。normalize_materials.py 重写合集化输出（幂等已验），白名单/夹具同步，8 项回归全过，浏览器实测大页渲染正常（2MB 词源页 4316 词条）。原则入 HANDBOOK 第五节：参考资料宁少而全不多而碎。
- 工程简化（2026-09-16，用户指令三项全选）：规则收敛——materials/HANDBOOK.md 成为下载/选源/归一化规则唯一出处（旧「总则」+「选源规则」合并，AGENTS 三处收敛为单条指向，批次记录归档 engineering/archive/downloads-batches-2026-09.md）；脚本三合一——references/normalize_materials.py（papers/ielts/readable/all 子命令，幂等已验 300 生成物快照比对，顺带修 ielts 来源头路径重复 bug）；杂物清理——空目录 reading/review 删除、textbook_mining 6.7MB→2.2MB（只留两个句子池参考实现）、site/verification 迁入 engineering/verification/。全部测试通过，浏览器验证 HANDBOOK 渲染正常。
- 教材回收三章合成（2026-09-16，用户指令）：07+10+11 合成单章 07-school-recall「教材回收：初高中句式框架」（三节 23 框架：初中篇扫描 9 + 课标回收 3 + 高中篇扫描 11，四组重叠框架以教材原文例句优先去重），10/11 章删除；三管线脚本 CHAPTERS 同步，build_chapter_previews.py 插入点升级兼容 ### 分节标题，总集 12→10 章，冒烟断言同步；00-guide 索引区扩为 23 框架全表，12 章两处「高中篇」引用改指合成章；全部测试通过。
- 分级通读三章（2026-09-17，用户指令）：中学/四/六/考研/雅思全量级联再提取——三级句池程序构建（四596/六3169/考2089句，精翻走引用块解析），152条种子登记表下发每批，20批LLM逐句通读，540例句回池逐字校验（替换19处后0不一致），程序聚类+人工裁决定版A类74条；低级已提取的高级不收，三章零重复；专八无开放语料由雅思83簇顶替（已披露）。编纂13/14/15三章（9+14+10句式骨架），管线/导航/00-guide同步，总集13章，全部测试过。中间物references/cascade_mining/。
- 阶段：重新定义工程目标：从“学习工具箱”转向“会”的定义、能力诊断与补齐闭环。
- 理论调研基线：engineering/methodology/2026-09-16-sla-research.md（二语习得理论与中国应试型学习者画像；关键结论：现有系统只做了四股均衡中的“语言聚焦学习”一股，缺意义聚焦输入、流利度发展与产出）。
- 已讨论：be resigned to，以及多组熟词生义和搭配。
- 历史 Lesson 001 已提供讲解和练习；练习尚无用户提交，不标记掌握。
- 诊断结论（2026-09-16 首批实测，见 progress/202609161941_诊断_能力基线第一批.md）：词汇广度约 4,000-4,500 词族（6k 段失守）；词汇深度不完整；句法主干提取 10/10 但两层嵌套+省略结构是盲区；瓶颈排序：词汇（广度+深度）> 嵌套句法 > 流利度 > 产出。剩余两项（阅读测速、写作样本）待测。
- 下一步候选：①按调研文档第九节实现轻量能力诊断（词汇广度/深度、句法加工、阅读速度、写作样本）；②把每日真实英文技术文档阅读接入为意义聚焦输入并计时测速。两者都应让测量本身就是一次真实学习行为。专题课程保留但降为主线之一。
- 首批诊断已完成两项（词汇广度/句法加工），接下来优先做：一次真实技术文档阅读计时（同时完成流利度测试与 strand 1 启动）与 150 词写作样本。
- 防偏提醒：避免重演“建造代替学习”，同样要避免“分析代替学习”——诊断项必须本周内被真实执行一次。
- 学习方法主线（2026-09-16，用户高度认可）：**框架学习法**——框架是比语法分析高一层的句级预制件（so...that 的同类）。四步法：Notice→Unpack→Imitate→Collect。已开专题 book/08-frames/（方法章+六大家族索引约30框架+家族A详细章），course.json 默认入口已指向家族A。新框架只从真实卡点/语料登记，不批量造。
- 框架边界共识（2026-09-16）：六大家族只是组织方式不是定义域；not only...but also 等初高中成对结构就是框架，应回收登记；长期用例句语料库（VOA/新闻/文学/台词）归纳框架为常态扩编方式——本地 examples 表 3.2万条但语域单一不足以归纳框架，外部语料下载为候选待办；另计划"没有框架的句子"特殊章（先讨论后落笔）。
- 前端排版已修（2026-09-16）：markdown 渲染器支持 GFM 表格+多行引用合并，引用样式从19px文学体改为紧凑学习样式；回归测试 site/test_markdown.cjs（10项）。
- 排版样张已定版并清理（2026-09-16）：风格 A「紧凑学习卡」胜出，规则固化在 book/TEMPLATE.md 与 AGENTS.md；四个样张文件与导航链接已删除（定版信息已入模板，样张使命完成）。
- 内容建设（2026-09-16，本会话）：①家族A已按新风格重写（例句大半换成 voc14w 语料真实例句，标注（语料）/（自造））；②新写家族B《强调与聚焦》：What假分裂/It was分裂句/Only倒装/rather than主语从句/do强调，基于诊断句 Q2/Q4/Q7/Q10；③**家族C/D/E/F 全部编纂完成**（03让步对照/04评述立场/05叙事推进/06条件虚拟），至此索引中 31 个框架全部有专章；每章均含语料真实例句+结构拆解+迁移练习与参考答案；④ course.json 七篇全挂进导航，前端已验证可见。已知发现：not least vs last but not least 是易混对，已在家族E章内对比。待办：教材回收批次、“没有框架的句子”章讨论、删除临时样张导航链接。

- 精确检索补强（2026-09-16，用户质疑质量后）：改用带单词边界的正则扫全库（17.4万例句），替换粗暴 LIKE。新挖语料例句：as it were（梭罗）、nothing less than/nothing if not、were it not 从句内倒装变体（汤姆·潘恩）。新沉淀三个陷阱教学点并已入章：much as≠as much as（全库39条命中全是数量用法）、if you will 命中全是字面义“如果你愿意”、had it not been 唯一命中是真疑问句。纯自造框架（词典库语域极限，补齐需轨道二真实语料）：much as 让步、be that as it may、so to speak、not least because。方法论教训：内容完成度声明必须附语料覆盖率数据。

- 框架总集（2026-09-16）：单篇通读版 book/08-frames/08-frames-collection.md（约1030行，六家族31框架+教材回收9框架，含目录锚点、全文标注约定统一）；合成脚本 references/build_frames_collection.py（章节增删后可重跑再生成）；渲染冒烟测试 site/test_frames_collection.cjs；已挂入课程导航"通读"级。分章学习仍用独立章（练习折叠在网页端只有独立章有）。教材回收章（07-school-recall，9框架）由另一会话完成并入总集。
- 框架节序号规范（2026-09-16，用户要求）：TEMPLATE.md 新增"## N. 框架名"格式（章内连续编号，练习/答案节不编号）；已应用全部章节并重新合成总集（8 章节、56 个编号框架节）。导航收敛：保留方法章/总集/教材回收/真题回收四项入口，家族A-F 分章文件保留为合成原料（不挂导航，合成脚本引用）；course.json start 改为总集。09 真题回收章（另一会话产出，9 份真题语料）已编号并入总集。
- 章首预览表规范（2026-09-16，用户要求）：TEMPLATE.md 新增通用规则——一章含多个知识点时章首必须放预览表（序号/名称/一句话语义），作用"先给地图再给地形+章末自查清单"；适用于所有 content。已为 8 个分章自动生成（references/build_chapter_previews.py，从节内语义行提取，幂等可重跑），总集重新合成（19 张表）。
- 教材回收覆盖度澄清（2026-09-16）：materials/ 并无初高中教材文本，07 章依据是课标语法项目表（未逐册扫描教材）；仅收"成对结构"故只有 7 个框架属正常。真正的未挖金矿是 materials/papers/ 的 70+ 份真题文本（六级 62 份规整 TXT 未用），是框架扩编的现成语料。修复 07/09 章编号叠加 bug（number_frame_sections.py 幂等化）。台词语料（930万句对，materials/corpus/opus-opensubtitles/）已下载登记，4 个纯自造框架在其中均找到真实例句，回填待做。
- 教材语料补齐（2026-09-16）：下载初中人教版 5 册课文全文（chncaesar/ChinaTextbook-Text）与高中教材句子倒排索引（ZhangYixuan-in-BUPT，MIT，四版本×7册、去重 30,110 句，人教版 8,523 句带单元出处）+ 人教 2019 高中七册词汇表（2,569 词）。存 materials/textbooks/，7 文件登记 manifest。07 章缺的教材原文现在有了，待逐册扫描做真正的教材框架回收（成对结构之外的倒装/强调/省略等也在此语料中）。
- 教材框架重挖（2026-09-16）：语料就绪后全量重扫——初中五册提取 5,588 完整句（词典驱动修复 PDF 断字），高中人教版 8,523 句，两轮正则扫描（粗扫发现误报后收紧：感叹限定句末!、倒装限定句首^等）。新增两章：10-junior-recall（初中 9 框架：so…that、too…to、used to、by the time、why not、get+过去分词、感叹句、more and more/the more、not only）与 11-senior-recall（高中 11 框架：so that、It is V-ed that、It is adj that、as if、句首分词状语、no matter、when it comes to、no longer、even if/though、It takes、what if），例句全部为教材真实命中并人工筛除 OCR 噪音（挖掘中间物存 references/textbook_mining/）。07 章来源行更新（不再"未逐册扫描"）。管线：number/previews/collection 三脚本 CHAPTERS 清单补新章（幂等验证无叠加），总集扩至 11 个 h1、21 表、148 引用块，冒烟测试断言 9→11。全部测试通过（test_server 8、test_learning 7、test_markdown 10、frames 冒烟；playwright 系浏览器测试因缺依赖跳过，与本次改动无关）。
- 下载选源规则定版（2026-09-16）：PDF 不是好的机器语料源（断字/乱序/扫描件不可机读，手译本与 2020 OCR 件为实证）。四级优先序：结构化带元数据 > 规整纯文本/Markdown > 文字层 PDF（须当场派生 txt/md 并抽查，登记以 PDF 哈希为准）> 扫描型 PDF（默认不收，仅阅读件）。通用：先明确用途再下载、下载即登记 manifest、无 LICENSE 仅本地用、优先带出处元数据的源。写入 materials/README.md，AGENTS.md 加引用条目。
- 框架挖掘方法定版（2026-09-16）：用户指出 regex 挖不出多少——正确分工是"发现框架靠 LLM 逐句通读、回收例句靠 regex 反查"。试点验证：300 句通读产出 25 个非预设新框架（同位语插入、指示回指、主谓间插入语、承前省略并列等 regex 盲区结构型框架）+18 单句候选，89 例句双重逐字校验 0 不一致。四步流程（成文语料池→LLM 批量通读→合并聚类→regex 反查）写入 methodology/2026-09-16-frame-mining.md，AGENTS.md 加"框架挖掘"硬条目，00-guide 扩编规则节挂链接。待办：教材池 10,949 句全量通读（37 批，分波并行）、六级 62 份 TXT 同法、字幕语料。
- 框架通读全量挖掘完成（2026-09-16）：与用户先定"什么值得挖"（三判据：骨架/误读/语域；A类进框架/B类语法点留拆解素材/C类指令伪影丢弃，试点25个里A类仅约7个）。重建通读池：4,649 句（10,949 信息句三轮过滤掉指令/模板/标题/断字，batch_001 试点旧池被覆盖、result_001 作废——判据定版前产物）。16 批 × 300 句分波并行 LLM 通读，产出 85 框架 + 217 单句候选，聚类去重 67 个独立框架，418 例句独立逐字复核 0 不一致（试点 89 例按内容比对发现 38 条已出池——正是新过滤有效的证据）。regex 反查全语料为各框架回收例句分布（修正 6 条词形 bug 后 backfill_hits.json）。编纂 12-readthrough-recall.md（12 个最高价值 A 类框架：one of the 最高级、What 假拟分裂、Could you tell me、疑问词+to do、with 复合结构、have/get+O+V-ed 使役、which 回指整句、句尾 V-ing 结果、Some others 对举、Not all 部分否定、For one thing/For another、was doing...when 突发叙事），例句全部教材真实命中。管线三脚本纳入新章，总集 12 章/22 表/171 引用块，冒烟断言 11→12，全部测试通过。框架总数：40（家族+回收）+ 20（教材两章）+ 12（通读篇）= 72，聚类中间物还有 55 个候选待后续按判据精选扩编。
- git 已初始化（2026-09-16）：english/ 为独立仓库，首提 8b975f9（81 文件，.git 仅 592K）。大文件排除：data/*.sqlite3、data/backups/、references/downloads/、sessions/web/（可通过 references 脚本重建）。后续改动随做随 commit。
- 框架建设计划：engineering/design/frames-plan-v1.md（四阶段：排版定版→手工识别器→语料接入→教材回收，含规模红线：索引≤100框架/专章≤7框架/语料十万句级；每章绑定真实学习行为）。
- 语料轨道一已完成（2026-09-16）：voc14w 14.1万例句已导入词典库（examples 总数 17.4万），站点查词可带回多语境例句；轨道二（Tatoeba/影视字幕子集，用于框架归纳）待用户授权下载；中文书籍先验推荐旋元佑《语法俱乐部》等已登记 guide 第七节。
- AGENTS.md 新增硬规则（2026-09-16）：对话中决定的项目改动必须当轮落档，只对话不落档视为未完成。
- 网页对话原始记录：sessions/web/*.json。恢复时读取相关会话，不把模型自评当作学习证据。
- 全仓库文档前端可见（2026-09-16）：catalog 改为全仓库 .md 自动发现，排除 site/data/sessions/.git/node_modules/downloads/imports 等工程目录；engineering/methodology/engineering/design/progress 诊断报告/references 导入记录/AGENTS.md 等知识文档与 agent 文档按「调研与方法／工程文档／进度与诊断／参考资料／项目说明」分组，显示在侧边栏「学习档案与扩展阅读」内。学习库不受影响（sync 只处理 book/，items 仍 53985、events 仍 0）。回归：site/test_server.py 新增全仓库发现用例。
- 侧边栏折叠（2026-09-16）：专题目录与扩展阅读分组改为 details 折叠组（带章节计数与箭头），当前阅读章所在专题/分组自动展开，其余默认收起。
- 侧边栏分区定版（2026-09-16）：右上角「专题课程」改名「主页」；侧边栏拆为两节——「专题目录」只放 course.json 的 6 个专题（用户概念：一本一本书），下移新增「文档资源」节收纳学习档案/工程文档/进度与诊断/参考资料/历史课堂/Book 其他章节，课程与文档彻底分离。
- 教材回收首批（2026-09-16）：新章 book/08-frames/07-school-recall.md「教材回收：初高中句式框架」——从课标语法项目表（义教2022+高中2017/2020，整理稿链接见章内）回收 7 框架：not only…but also（含倒装）、so/such…that、too…to、either/or 与 neither/nor、the more…the more、no sooner…than 与 hardly…when、would rather…than。例句除 4 条（自造）仿写示例外均取自 voc14w 语料并逐条标注；边界披露：未逐册扫描教材文本，以课标为纲。已登记 00-guide 索引（教材回收节）、接入 course.json 句式框架专题、更新 CHANGELOG/BACKLOG（第二批候选已列）。catalog 发现与页面渲染已验证（表格/代码块/引用块/答案折叠）。
- 文本类资料全量 md 化（2026-09-16，用户定版：纯文本全转、json/csv/jsonl 豁免）：normalize_text_to_md.py——papers 78 txt→原件旁 md；词源书三册按首字母分册 wordbooks-md/（77 册 9986 词条）；catalog 白名单层级精确（顶层/readable/textbooks/dictionaries/wordbooks-md），materials 前端可见 130 篇；test_server 夹具扩充 8 项全过，浏览器验证词源分册渲染（264 词条+目录）。总则/AGENTS 已同步。
- 下载与归一化总则定版（2026-09-16）：references/README.md 顶部新增「下载与归一化总则」（下载五原则/目录五分类/数据层-可读层分离规则），AGENTS.md 目录体系补 materials/ 条目与排除扫描更新、「记录与边界」补执行摘要——后续资料下载照总则执行，不再临场决策。另：初高中教材语料已入库 materials/textbooks/（初中人教 5 册全文 md、高中句子倒排索引 30110 句、人教高中词汇表 2569 词），07 章当年「未逐册扫描教材」的缺口已可补。
- materials 归一化（2026-09-16）：可读层 materials/readable/（46 页 md：真题+精翻+词源说明+索引，脚本 references/build_materials_readable.py 可重跑）进前端「学习资料」组；数据层补齐——下载考研英一 2005-2026 阅读精翻 22 份 md（Destinnnnn 仓库，manifest 现 122 条）、2020 扫描卷 OCR（pytesseract eng，2.6 万字符，中文头部不可靠已注明）、词源书三册 pdftotext 全文（-full.txt 约 850 万字符）。边界：手译版中文层不可机读（无 ToUnicode），机读层由精翻替代；OCR 无中文语言包。catalog 现含 materials 47 篇可见。
- materials 侧边栏接入（2026-09-16）：materials/README.md（浏览索引）进左侧「参考资料」下的「学习资料」子分组；catalog 只发现 materials 顶层 md，第三方 README 屏蔽；前端参考资料节改嵌套渲染；test_server 新增用例 8 项全过，4174 已重启并浏览器验证。
- 资源目录重组（2026-09-16）：references/downloads/ 整体迁入项目根目录 materials/ 并按类型分类——vocabulary/（词表+voc14w 例句库）、dictionaries/（ECDICT/WordNet/Kaikki/词源单词本）、papers/（exams/cet4/cet6/kaoyan 真题与手译）、corpus/（OPUS OpenSubtitles 1.5GB，此前未登记已补记）。manifest 现为 materials/downloads-manifest.json，100 条路径改写后全量复验 SHA-256 通过；.gitignore 改为 materials/* + 白名单 manifest；server.py catalog 排除 materials；三个 references 脚本与全部活文档引用已更新；08-frames-collection 重建。历史导入报告与当日 CHANGELOG 条目保留原路径作为历史事实。
- 考试参考资料库（2026-09-16）：按用户指令从 GitHub 补充下载 81 个四六级/考研/专八参考文件至 references/downloads/ 新四目录——cet4/（2024-06、2025-06 各 3 套真题 PDF+txt）、cet6/（2016-2026 规整 TXT 62 份，可直用于框架挖掘）、kaoyan/（英一手译版 5 册 1986-2020+2020 真题+考研词频表 5530 词）、wordbooks/（词源单词本 CET4/CET6/TEM8 三册）。manifest（files 列表）现 100 条，全量 SHA-256 校验通过；sources：0609x/CET46-Resources、AndrewYuZhenYu/cet6_exam_questions_txt_collection、m2kar/KaoYan-English、exam-data/NETEMVocabulary（CC BY-NC-SA 4.0）、openetymology/OpenEtymology（CC BY-SA 4.0）。边界：专八真题无开放仓库，以 TEM8 词源分册覆盖词表方向；手译版与词书为阅读参考不进学习库。注意：downloads-manifest.json 实为 {created_at, files:[...]} 列表结构，非顶层键。
- 真题回收首批（2026-09-16）：按用户指令从 GitHub 公开仓库下载四六级/考研历年真题 9 份 PDF（四级 2022-06、六级 2018-06、英一 2017/2018/2019、英二 2016-2019）至 references/downloads/exams/，pypdf 抽取文本约 22 万字符，SHA-256 全部登记 downloads-manifest.json。正则初筛约 60 候选模式、人工核对后新章 book/08-frames/09-exam-recall.md 登记 7 框架（as long as / rather than / end up / it turns out / when it comes to / be likely to / even if/even though），每条附真题原句与出处；已登记 00-guide 索引（扩编规则改为三条来源）与 course.json（句式框架 10 课）。边界：模拟题未收录（版权教辅无开放语料），完形空格以 ___ 保留；频次结论限 9 卷样本。回归 test_server/test_learning 各 7 项全过，浏览器渲染已验证（9 个 h2、17 条引用块）。剩余候选（Suppose、in other words、it is likely that、be expected to、as such、happen to）已留证据入 BACKLOG。
- 非 book 文档整理（2026-09-16）：盘点全部非教材文档后，新建 engineering/archive/（组「历史归档」）并 git mv 5 份失去现实效力的文档——implementation-v1（计划全部完成）、learning-workbench（标注已实现）、topics-v1（被 course.json 取代）、top-down-method（自标被 METHOD.md 替代）、product-retrospective-09-15（历史复盘）。engineering/agents/ 补 README.md 说明目录职责并删除 .gitkeep。AGENTS.md「目录体系」节新增归档整理原则：失去效力即移入 archive/，只进不出。
- 目录体系重构（2026-09-16，用户定版）：新建根目录 engineering/ 工程文档总目录（git mv design、methodology 进入，新建 agents/ 子目录待用），左侧对应顶层资源「工程文档」（子组：Agent 文档/设计/调研与方法）；progress/ 确认为学习进度与诊断（非工程建设进度），保持根目录对应「进度与诊断」；侧边栏改为顶层资源平铺（学习档案/工程文档/进度与诊断/参考资料/历史课堂/Book 其他章节），废除单一「学习档案与扩展阅读」；book 根目录 README/TEMPLATE/BACKLOG/CHANGELOG 不再形成「Book 导览」组——README 为书入口（隐藏，专题页底部「关于本书」可达），TEMPLATE/BACKLOG/CHANGELOG 归「工程文档→Agent 文档」。全仓 md 路径引用已同步更新；规则写入 AGENTS.md「目录体系」节；回归 site/test_server.py 7 项全过。

## 掌握记录

目前没有足够独立与延迟复测证据，不设置完成百分比。

## 学习记录入口更新

第一版工作台已上线本机4174端口。具体学习标记、原答、自评及到期日期以 data/learning.sqlite3 的events/progress为准，网页“知识库／今日复习”可查看。系统初始记录为空，工程测试在独立目录进行，不计入个人学习状态。
