# English 项目约定

适用范围仅为 english。用户当前明确要求优先。

## 目录体系（2026-09-23 更新：站点为纯 markdown 查看器）

- **nav.json**：站点侧边栏目录的唯一登记处。显式列出要展示的文档（组名 + 路径，支持组内子标签），标题自动取自文档一级标题；未登记的文件不进站点（详见 site/README.md）。
- **engineering/**：工程文档总目录，不进站点导航。内含子目录 agents/（agent 文档）、design/（设计方案）、methodology/（调研方法）、archive/（已完成或被取代的历史文档，只进不出，不删除）。新增工程文档放对应子目录。整理原则：文档失去现实效力（计划全部完成、被新文档取代、纯历史记录）就移入 archive/，保留路径与引用。
- **AGENTS.md**：根目录唯一保留的 agent 文档；被它引用的其它 agent 文档放 engineering/agents/（目录职责见其 README.md）。
- **progress/**：学习进度与能力诊断（非工程建设进度），保持根目录。
- **book/**：教材，按主题目录保存 Markdown。书入口 README 与工程配套（TEMPLATE/BACKLOG/CHANGELOG）不进导航。
- **engineering/skills/**：既有英语内容生产 skill 的源文件（frame-miner 拆句式骨架、english-content-forge 生成句集/指南）；中译英训练 `translation-coach` 的源文件在 `.agents/skills/translation-coach/`，此处保留指向它的站点阅读链接。三个 Skill 的 SKILL.md 与中译英计划已登记进 nav.json「内容生产 Skills」组；新增句集/完全指南类内容按 english-content-forge 流程（数据 jsonl → 渲染脚本出视图）执行。
- **references/**：教材构建与归一脚本（build_chapter_previews / build_frames_collection / normalize_materials 等）及导入报告。挖掘中间数据（批次 json、句池、裁决存档）2026-09-24 已移入 engineering/archive/，脚本与报告留在原处。
- **vocabulary/**：历史讲义（1 篇旧课，已在 nav.json「学习档案→历史课堂」登记）。
- **materials/**：下载资料总库（词表/词典/真题/教材/语料），只有 readable/ 合集在 nav.json 登记。每个文件登记 materials/downloads-manifest.json（SHA-256+URL+许可）。下载、选源与归一化规则唯一出处是 materials/HANDBOOK.md——照手册执行，不需重新决策；资料清单与批次记录见 materials/README.md。

## 恢复

先读 background/LEARNER.md、background/METHOD.md、background/CURRENT.md，再读当前章节。不要重复背景问卷，不从旧考试分数推断当前等级。

## 教学

遵守 background/METHOD.md。用户当前在搭建系统时，不擅自推进测验。听力暂缓，长难句是候选章节而非已证实短板。保留用户纠正，区分事实、假设、已讲解与掌握。

用户要求中译英练习、中文与自然英文素材采集、表达课程计划或翻译评改时，使用 `engineering/skills/translation-coach/SKILL.md`；整句表达与交际意图优先，单词、词组和句式骨架按卡点嵌入。计划与来源规则见该 Skill 内的 `PLAN.md` 和 `references/sources-and-coverage.md`。

## 编纂 Book

主线五个专题（熟词生义、整句词组、常用句型、特殊句子、单词专题）在 nav.json 里以分组体现（原 course.json 已于 2026-09-23 废弃）。新增主线章先明确阅读卡点、对照和新语境，再把 Markdown 路径登记进 nav.json 对应组；不要只增加词条数或按考试标签铺满目录。没有正文的未来主题只放BACKLOG，不作为可开始章节展示。

正式教材源文件在 book/，按主题目录保存 Markdown；站点目录由 nav.json 显式登记，不再自动扫描。每章一级标题唯一（它就是站点里显示的标题）。新增章后验证 /api/catalog 能发现标题、分组、全文。

先读 book/README.md、book/BACKLOG.md 和相关已有章节，避免重复。按 book/TEMPLATE.md 的规范写实际内容；模板与 backlog 不算教学章。排版统一按 TEMPLATE.md 的「紧凑学习卡」风格（2026-09-16 用户定版，样张 book/08-frames/_样式样张A-紧凑学习卡.md）：语义加粗一句话、例句引用块中英对照、结构拆解代码块、变体对比表格，不叙事铺陈。

常用义项和搭配给自然语境、解释、结构、边界、变式练习；自造例句注明。对不确定的用法先查权威词典或一手语料，保留实际查阅链接，不能伪造来源。

用户只说扩增时，默认一批 1–2 个主题、约 6–10 个表达，深入辨析，避免以词条数量代替质量。可增加新主题目录，前端无需改代码。更新 book/CHANGELOG.md 和 BACKLOG.md；材料扩增不修改掌握等级。

## 句式骨架挖掘

挖掘成文语料（教材/真题/字幕）中的句子句式骨架时，先读 engineering/methodology/2026-09-16-frame-mining.md：发现句式骨架靠 LLM 逐句通读（每批300句，句式骨架须≥2句重复验证，例句逐字复制并双重校验），regex 仅用于为已确认句式骨架回收例句。通读对象是所有成文内容（含听力原文），不是只有课文正文。

## 下载资料选源与归一化

规则唯一出处：materials/HANDBOOK.md（2026-09-16 定版，含下载五原则、选源四级优先序、目录五分类、数据层/可读层分离、catalog 白名单、工具速查与不变式）。要点：优先公开仓库/官方平台，下载即登记 manifest；原件不改写，可读层由 references/normalize_materials.py 生成（幂等重跑），json/csv/jsonl 豁免不转；批量前先抽查质量。执行时照手册走即可。

## 记录与边界

**资料下载与归一化（2026-09-16 定版）**：规则唯一出处 materials/HANDBOOK.md（由旧「总则」与「选源规则」合并而来），执行时照手册走，不再临场决策。

**对话决策落档（2026-09-16 起，用户明确要求）**：与用户对话中决定的项目改动——工程怎么改、内容怎么改、背景/思路/方法论怎么改——必须在当轮对话内写入对应文件（工程改动→CURRENT.md 或 engineering/design/，内容改动→book/ 及 CHANGELOG/BACKLOG，背景与思路→background/LEARNER.md、background/METHOD.md、engineering/methodology/，记忆类→.catpaw/memory）。只对话不落档视为未完成。落档后当轮回复里告知用户写入位置。

学习背景写 background/LEARNER.md，教学方法写 background/METHOD.md；网页对话功能已删，不再自动保存原答与反馈。Codex 对话中的实际练习可把必要原答、提示与反馈写入 progress/ 作为证据，私人情境先去身份化。不要跨写 ml-foundations。Book 正式编辑由用户在 Codex 中提出扩编请求后执行，避免把未经审校的每次回答自动收进教材。

站点仅本地运行，不默认部署公网；纯只读查看器，无对话与写接口。测试：python3 site/test_server.py。

## 数据库学习记录（已归档）

2026-09-23 站点收敛为纯查看器时，learning.sqlite3（学习原答、自评与复习调度）与 combined_dictionary.sqlite3（合并词典）已移出仓库至 ~/workspace/english-archive/。旧约定全文见 git 历史中的 AGENTS.md；若恢复学习功能，从该目录取回数据库、在 git 历史找回 learning_store.py / dictionary_store.py，并重读当时的调度与 schema 约定。在此之前：不要把历史 SQLite 标记或用户自评当成经过独立考查的掌握证明，学习状态以 progress/ 诊断与用户口述为准。
