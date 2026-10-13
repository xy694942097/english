# English 项目约定

适用范围仅为 english。用户当前明确要求优先。

## 目录体系（2026-10-13：教程统一放在 course/）

`course/` 是教程与前端阅读文档的统一根目录；下属分组和子目录与前端同名。新增学习文档直接放入 `course/` 对应目录，项目根目录只保留工程、原始数据与配置。

- **course/词汇/**：当前保留《生词与熟词新义》一个学习入口；单词义项、接法和高一层的词汇辨析在此积累，不为单词新建章节。
- **course/表达练习/**：表达讲解和情境任务。
- **course/Chunks 收集/**：包含《精选 Chunks》、候选收集箱及按作品整理的原句积累。精选条目与候选原句分层，默认录入路径见下文。
- **course/原文与参考资料/**：可读原文、教材、影视资料入口与表达语法查阅；同名前端子标签对应同名子目录，审校状态写在文档中。
- **course/我的学习/**：背景、方法、诊断与当前状态。
- **course/编纂与维护/**：编纂约定、Chunks 收集与排版、中译英训练与编题、资料来源四篇；TED 维护并入资料来源；前端作为独立折叠入口。
- **nav.json**：只登记展示顺序与可见性，分组／子标签必须与实际父目录同名，不跨目录重新分类。
- **materials/**：后台下载数据与来源 manifest，原文数据的目录、许可、哈希规则见 materials/HANDBOOK.md；面向读者的阅读文档放“course/原文与参考资料/”。
- **references/**、**engineering/**、**site/**、**progress/**：生成工具、工程记录、查看器和后台练习证据；不映射成学习顶层目录。原26篇独立学习章节全文及校验清单在 engineering/archive/learning-chapters-2026-10-13，旧版未展示教材仍在 engineering/archive/legacy-book；编纂说明在 engineering/agents/book-editorial。
- **.agents/skills/translation-coach/**：中译英训练的实际 Skill 源包；“编纂与维护/中译英训练与编题.md”为可读总览，执行时以源包为准。

旧路径到新路径的映射保存在 engineering/design/document-paths-2026-10-11.json，用于旧网页深链兼容与生成工具定位；它不是第二套分类。后续新增文档直接使用新目录。

## 恢复

先读 course/我的学习/学习者背景.md、course/我的学习/学习方法与教学思想.md、course/我的学习/当前学习状态.md，再读当前章节。不要重复背景问卷，不从旧考试分数推断当前等级。

## 教学

遵守 course/我的学习/学习方法与教学思想.md。用户当前在搭建系统时，不擅自推进测验。听力暂缓，长难句是候选章节而非已证实短板。保留用户纠正，区分事实、假设、已讲解与掌握。

用户要求中译英练习、中文与自然英文素材采集、表达课程计划或翻译评改时，使用 `.agents/skills/translation-coach/SKILL.md`；整句表达与交际意图优先，单词、词组和句式骨架按卡点嵌入。计划与来源规则见该 Skill 内的 `PLAN.md` 和 `references/sources-and-coverage.md`。

用户要求从已提取的 chunks 编写中译英题库／练习文档时，使用 `.agents/skills/chunk-translation-drills/SKILL.md`；题目与参考 Chunk 分区，参考区默认折叠，不提供完整英文答案。出题原则的后续修订写入该 Skill，用户实际作答反馈仍由 translation-coach 处理。

用户提出的 chunks 上位概念与快速识别目标见 `course/我的学习/把 chunks 作为快速理解与表达的学习单位.md`。采集候选是第一步，可以广收并暂记待核；编入正式教材或作为正确用法教学时才应用更严格的查证与迁移门槛。记录来源和语域，不把搜集数量当理解速度或掌握证据。

在本项目中用户说“帮我录入”且没有指定其他去处时，按 `course/编纂与维护/Chunks 收集与排版.md` 将其给出的单项、多行或文本候选录入 `course/Chunks 收集/Chunks 收集箱.md` 的相应分类，采用 Better Call Saul 式纵向条目（编号 Chunk、意思、例句引用块、来源），以 `.agents/skills/chunk-collection/SKILL.md` 为规则源。只在收集箱内查重，Book 或其他文章里已有讲解不构成跳过理由；收集箱内同义、同功能且无独立学习价值的近重复跳过，不因片段更长就重收。先保留原句与来源；缺失例句写“待补例句”，查重时不覆盖旧例证。录入后报告新增、补充及跳过项。仅录为候选，不自动编入 Book、做学习测验或标掌握；用户指定别的目标时服从其指令。

## 编纂 Book

站点顶层仍按“词汇／Chunks 收集／表达练习／原文与参考资料／我的学习”五个用途组组织，维护工具单列在 maintenance。知识主轴是 Chunks 与生词；一个表达或一个生词直接进入现有精选页／词汇页，不新建独立导航章。真实句子的理解与迁移留在表达练习。新独立专题须有多个相关卡点、自然语境、边界和迁移任务，并显式登记 nav.json；只增加条目数或考试标签不构成新章理由。原 course.json 已废弃。

先读 `course/编纂与维护/编纂约定.md` 判定文档角色：学习主线、表达练习、查阅资料、候选、隔离待修。隔离待修文档不得作为用法正确性的依据；查阅资料属于待审材料，引用某条之前仍须核对语境和来源。现行文档已按目录用途迁移，审校与掌握状态不决定文件位置；编辑状态不等于用户掌握。

Chunks 收集文档的统一排版与录入使用 `.agents/skills/chunk-collection/SKILL.md`；旧三列表规则已替换。词汇积累文档归 `course/词汇/`。

当前知识文档分别是 `course/Chunks 收集/精选 Chunks.md` 与 `course/词汇/生词与熟词新义.md`；从原句候选精选时检查同形同义、语域、槽位与出处。旧独立章节的全文、练习和来源在 `engineering/archive/learning-chapters-2026-10-13/`，不得把存档误认为用户已学会。站点目录由 nav.json 显式登记，不自动扫描；新增真正独立的文章后验证 /api/catalog 的标题、分组、全文。

先读 engineering/agents/book-editorial/README.md、engineering/agents/book-editorial/BACKLOG.md 和相关已有章节，避免重复。按 engineering/agents/book-editorial/TEMPLATE.md 的规范写实际内容；模板与 backlog 不算教学章。排版统一按 TEMPLATE.md 的「紧凑学习卡」风格（2026-09-16 用户定版，以当前 TEMPLATE.md 为准）：语义加粗一句话、例句引用块中英对照、结构拆解代码块、变体对比表格，不叙事铺陈。

常用义项和搭配给自然语境、解释、结构、边界、变式练习；自造例句注明。对不确定的用法先查权威词典或一手语料，保留实际查阅链接，不能伪造来源。

用户只说扩增时，默认一批 1–2 个主题、约 6–10 个表达，深入辨析并优先追加到现有知识文档；如确需新文档，再保持前端与文件系统的目录一致，显式登记 nav.json。更新 engineering/agents/book-editorial/CHANGELOG.md 和 BACKLOG.md；材料扩增不修改掌握等级。

## 句式骨架挖掘

挖掘成文语料（教材/真题/字幕）中的句子句式骨架时，先读 engineering/methodology/2026-09-16-frame-mining.md：发现句式骨架靠 LLM 逐句通读（每批300句，句式骨架须≥2句重复验证，例句逐字复制并双重校验），regex 仅用于为已确认句式骨架回收例句。通读对象是所有成文内容（含听力原文），不是只有课文正文。

## 下载资料选源与归一化

TED 资料沿用用户确认的“带基本信息的 TXT”格式例外，执行前读 `materials/HANDBOOK.md` 的 TED 说明及 `course/编纂与维护/资料来源.md`；不默认恢复 JSON/SRT/VTT，也不把获取脚本成功当成 manifest、索引与校验已经更新。

规则唯一出处：materials/HANDBOOK.md（2026-09-16 定版，含下载五原则、选源四级优先序、目录五分类、数据层/可读层分离、catalog 白名单、工具速查与不变式）。要点：优先公开仓库/官方平台，下载即登记 manifest；原件不改写，可读层由 references/normalize_materials.py 生成（幂等重跑），json/csv/jsonl 豁免不转；批量前先抽查质量。执行时照手册走即可。

## 记录与边界

**资料下载与归一化（2026-09-16 定版）**：规则唯一出处 materials/HANDBOOK.md（由旧「总则」与「选源规则」合并而来），执行时照手册走，不再临场决策。

**对话决策落档（2026-09-16 起，用户明确要求）**：与用户对话中决定的项目改动——工程怎么改、内容怎么改、背景/思路/方法论怎么改——必须在当轮对话内写入对应文件（工程改动→CURRENT.md 或 engineering/design/，内容改动→book/ 及 CHANGELOG/BACKLOG，背景与思路→course/我的学习/学习者背景.md、course/我的学习/学习方法与教学思想.md、engineering/methodology/，记忆类→.catpaw/memory）。只对话不落档视为未完成。落档后当轮回复里告知用户写入位置。

学习背景写 course/我的学习/学习者背景.md，教学方法写 course/我的学习/学习方法与教学思想.md；网页对话功能已删，不再自动保存原答与反馈。Codex 对话中的实际练习可把必要原答、提示与反馈写入 progress/ 作为证据，私人情境先去身份化。不要跨写 ml-foundations。Book 正式编辑由用户在 Codex 中提出扩编请求后执行，避免把未经审校的每次回答自动收进教材。

站点已恢复纯只读查看器（2026-10-13 用户要求），无前端编辑或后端写入接口。支持本地运行与 GitHub Pages 静态构建；公开网站的内容使用 `site/publish-nav.json` 显式登记，不默认公开个人学习档案、维护文档或原始材料。首次实际发布需确认发布清单；测试：python3 site/test_server.py。

## 数据库学习记录（已归档）

2026-09-23 站点收敛为纯查看器时，learning.sqlite3（学习原答、自评与复习调度）与 combined_dictionary.sqlite3（合并词典）已移出仓库至 ~/workspace/english-archive/。旧约定全文见 git 历史中的 AGENTS.md；若恢复学习功能，从该目录取回数据库、在 git 历史找回 learning_store.py / dictionary_store.py，并重读当时的调度与 schema 约定。在此之前：不要把历史 SQLite 标记或用户自评当成经过独立考查的掌握证明，学习状态以 progress/ 诊断与用户口述为准。
