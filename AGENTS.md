# English 项目约定

适用范围仅为 english。用户当前明确要求优先。

## 恢复

先读 LEARNER.md、METHOD.md、progress/CURRENT.md，再读当前章节及相关 sessions/web 记录。不要重复背景问卷，不从旧考试分数推断当前等级。

## 教学

遵守 METHOD.md。用户当前在搭建系统时，不擅自推进测验。听力暂缓，长难句是候选章节而非已证实短板。保留用户纠正，区分事实、假设、已讲解与掌握。

## 编纂 Book

主线以book/course.json中的五个专题组织：熟词生义、整句词组、常用句型、特殊句子、单词专题。新增主线章先明确阅读卡点、对照和新语境，再将已有Markdown路径加入课程清单；不要只增加词条数或按考试标签铺满首页。没有正文的未来主题只放BACKLOG，不作为可开始章节展示。

course.json可用unit_kinds显式指定章节知识点类型，如grammar。目录迁移不移动旧文件或重置学习记录。老师恢复时优先读取当前专题与相关正文。

正式教材源文件在 book/，按主题目录保存 Markdown；目录与搜索由 site/server.py 自动扫描。每章一级标题唯一。新增章后验证 /api/catalog 能发现标题、分组、全文。

先读 book/README.md、book/BACKLOG.md 和相关已有章节，避免重复。按 book/TEMPLATE.md 的规范写实际内容；模板与 backlog 不算教学章。排版统一按 TEMPLATE.md 的「紧凑学习卡」风格（2026-09-16 用户定版，样张 book/08-frames/_样式样张A-紧凑学习卡.md）：语义加粗一句话、例句引用块中英对照、结构拆解代码块、变体对比表格，不叙事铺陈。

常用义项和搭配给自然语境、解释、结构、边界、变式练习；自造例句注明。对不确定的用法先查权威词典或一手语料，保留实际查阅链接，不能伪造来源。

用户只说扩增时，默认一批 1–2 个主题、约 6–10 个表达，深入辨析，避免以词条数量代替质量。可增加新主题目录，前端无需改代码。更新 book/CHANGELOG.md 和 BACKLOG.md；材料扩增不修改掌握等级。

## 记录与边界

**对话决策落档（2026-09-16 起，用户明确要求）**：与用户对话中决定的项目改动——工程怎么改、内容怎么改、背景/思路/方法论怎么改——必须在当轮对话内写入对应文件（工程改动→CURRENT.md 或 design/，内容改动→book/ 及 CHANGELOG/BACKLOG，背景与思路→LEARNER.md/METHOD.md/methodology/，记忆类→.catpaw/memory）。只对话不落档视为未完成。落档后当轮回复里告知用户写入位置。

学习背景写 LEARNER.md，教学方法写 METHOD.md，原答与反馈写 sessions/，进度证据写 progress/。不要跨写 ml-foundations。网页老师负责对话，服务器保存原答；Book 正式编辑由用户在 Codex 中提出扩编请求后执行，避免把未经审校的每次回答自动收进教材。

站点仅本地运行，不默认部署公网。网页对话使用本机 Codex 登录，API 不接受任意 shell 命令、任意文件路径或模型选项。测试：python3 site/test_server.py。

## 数据库学习记录

第一版已加入 data/learning.sqlite3。网页学习原答、自评和复习时间以数据库events/progress为准；恢复用户状态时结合该库与sessions/web，不只读静态CURRENT.md。不要把SQLite标记或用户自评升级为经过独立考查的掌握证明。

数据库以类型、标题和含义区分学习条目，章节通过links关联。Book扫描可更新讲解，不应重置学习记录。正文修改不代表用户需要重新考试，义项拆分/合并要保留旧证据与迁移关系。

AI录入候选可由网页生成，用户编辑确认后入库；区别于正式Book增编，不自动改写Markdown。已完成四级、六级、专八与NGSL社区词表的批量来源导入；源文件、哈希与规则见references/README.md。整书自动提取尚未实施。调度只提供网页到期队列，未设置系统定时通知。

数据库schema v2加入collections、collection_items、catalog_heads。额外词典解释按来源保存，不覆盖Book或重置进度。大型词库页面使用browse分页接口，不一次加载全部正文。新来源应先隔离试导入、检查义项/词头去重与事件不变，再备份发布；不能把社区词表标签写成已核验的最新官方大纲。

新功能测试用 --data-dir 指定隔离目录，不在真实库写测试学习事件。回归：python3 site/test_learning.py；浏览器测试说明见site/README.md。快照使用SQLite备份接口，不能在运行中直接复制活跃事务文件代替可靠备份。
