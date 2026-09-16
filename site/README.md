# English Book 本地站点

参考相邻 ml-foundations/book-site 的目录、全文搜索、阅读布局和主题切换；英语站增加本地对话后端。

## 运行

```bash
cd /Users/xianyi/workspace/learn/english
python3 site/server.py
```

默认 http://127.0.0.1:4174 ，可用 `--port 4175` 换端口。只监听回环地址。停止终端服务后网页无法连接，重新启动即可恢复记录。

Python 3.10+、Codex CLI 及有效登录；前端无安装依赖、无 CDN。阅读与历史查看不调用模型，点发送或重试才调用。老师按当前 CLI 默认模型配置运行。

## 查词典

站点内置合并词典页面：打开 `#dictionary` 可手动输入单词，打开 `#dictionary/indignant` 可直接查指定词。页面调用 `/api/dictionary/lookup`，展示中文解释、英英解释、词根词缀、WordNet 义项、词组、例句、同义/反义/派生关系和联想辨析。

正文阅读时可选中英文单词后点“查选中词”，也可以双击英文词跳转到词典页；词典页会保留“回到原文”链接并尽量恢复原阅读位置。词典 API 是只读接口，不写学习进度，也不把词典材料自动计入掌握记录。返回数量可通过 `examples`、`phrases`、`relations`、`senses`、`notes` 等查询参数控制，避免一次性把大词典塞进前端。

## 内容与对话

目录自动扫描 LEARNER.md、METHOD.md、progress/CURRENT.md、Book 导览与 book/*/*.md；兼容保留的历史 vocabulary 讲义。新章节只需一个主题子目录与一个 Markdown 文件。其余仓库 Markdown（methodology、design、progress 诊断报告、references 说明、AGENTS.md 等知识文档与 agent 文档）也自动发现并分组展示在侧边栏「学习档案与扩展阅读」；site/data/sessions/.git/node_modules/references 的 downloads 与 imports 不扫描。章节用一级标题，答案用 `## 参考答案` 放在末尾，网页折叠显示。

渲染支持标题、段落、引用、列表、代码块、行内代码、加粗和 Markdown 链接；不执行 Markdown 原始 HTML。复杂表格与数学排版尚未加入，英语教材无需依赖它们。

每次发送附上档案、方法、进度、当前整章与最近 30 条网页消息。所有原始消息按会话保存为 sessions/web/<id>.json。近期上下文窗口并非无限记忆，较早历史可以由 Codex 读取原文件恢复。

`codex exec --ephemeral --sandbox read-only` 在隔离的临时工作目录运行；服务器通过输入提供学习材料。它不会接续桌面任务，也不直接编辑正式教材。网页不接受任意 shell 命令或文件路径。服务检查 Host、Origin 与本次启动令牌。

同一会话只允许一个进行中的回复，全站同时最多两个；240 秒超时。问题先保存，失败、服务重启后可以重试，不重复追加原问题。

## 验证

```bash
python3 site/test_server.py
python3 site/test_learning.py
node --check site/public/app.js
node --check site/public/learning.js
node site/test_dictionary_ui.cjs
```

覆盖新章自动发现、背景与语境输入、原答持久化及路径边界。另需实测页面搜索、答案折叠、对话回复与刷新恢复。

## 数据库、导入与复习

2026-09-14升级为schema v2：增加collections、collection_items、catalog_heads，保存词表归属和独立来源正文。知识库使用/api/learning/browse分页查询标题与含义，每页最多100项，详情页再读取正文。/api/learning/items保留给旧接口与按章节查阅，不用于整库前端加载。

批量词表脚本为references/import_wordlists.py，按下载文件哈希和来源保留报告。词头可关联多个考试/高频集合，附加解释不会覆盖旧Book学习记录。v1迁移前自动保存SQLite快照；新导出格式包括三张来源关联表。

learning_store.py负责SQLite访问；server.py仅接收受约束的业务参数，模型无权直接生成或执行SQL。类型包括word/phrase/sentence/grammar/expression；条目id按类型、规范化标题和含义计算，支持同词不同义项与多个教材来源。用户标记只覆盖当前条目范围，不代表整词所有义项。

初次载入扫描Book中的词条和主搭配，并加入starter_tasks.json。后续扫描更新教材正文，不重置学习记录；改义项会形成新id，删除章节不自动删除已有知识或用户记录。数据迁移若涉及合并义项，应专门处理，不静默合并进度。

items保存知识；links保存章节关系；progress保存理解/表达各自的下次复习；events保存原答、自评、提示程度、手动分钟数、前后状态与撤销标志。写入使用事务；请求编号防止重复记账；只能逐次撤销某条目同方向的最新未撤销事件。

调度v1：首次学习次日；忘了后10分钟并回到重新学习阶段；费力用当前阶段间隔的一半且至少1天；顺利按1/3/7/14/30/60天逐级递进（首次学习后的首次顺利复习为3天）。允许提前复习，间隔从实际本次记录时间计算。时间内部为UTC，页面以浏览器本地时间显示。

导入为预览→编辑→确认；可只有词而没有解释，明确显示释义未补充。AI候选经结构验证但没有外部词典核验；生成最多20条，4分钟超时，作业文件保存在data/drafts。离开页面或刷新可恢复最后一个生成任务。候选确认后按义项去重；不自动覆盖已存在条目的正文。

## 备份与恢复

知识库页面“备份数据库”使用SQLite备份接口，保存至data/backups；“导出数据”下载知识、关联、进度和事件JSON。原始网页会话仍在sessions/web，Markdown仍在book，应一并备份english目录。

恢复数据库：先停止本地服务，将当前learning.sqlite3另行留存，再把所选快照复制到data/learning.sqlite3，重新启动。初版没有网页覆盖恢复按钮。不要把测试数据库当作真实学习记录。

## 隔离测试

```bash
python3 site/server.py --port 4175 --data-dir /tmp/english-workbench-test
```

以上将数据库、生成候选和测试聊天保存到独立目录。test_workbench.cjs验证学习、刷新、分模式复习、撤销、多行录入与去重；需要安装Playwright或通过PLAYWRIGHT_MODULE指定本机模块路径。ENGLISH_TEST_URL指定测试服务，默认4175。使用新的测试目录执行完整流程，避免复用已有测试进度。
