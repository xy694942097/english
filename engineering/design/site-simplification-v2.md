# 站点收敛 v2：纯 markdown 查看器（2026-09-23）

## 决策

用户定版：站点只需要 **markdown 阅读、关键词搜索、主题切换**，对照 `~/workspace/play/docsite` 的形态。据此砍掉全部附加功能面：

| 砍掉 | 涉及 |
|---|---|
| 学习工作台（知识库/复习队列/录入/SRS/导入备份） | learning_store.py、learning.js/css、/api/learning/* 13 个端点、starter_tasks.json、Codex 候选生成 |
| 词典 | dictionary_store.py、/api/dictionary/* 3 个端点、app.js 查词视图与双击查词 |
| 专题主页 | topicHome、course.json 的 featured/start 元数据 |
| 写侧安全机制 | TOKEN、do_POST、Origin 校验（只读站点不再需要） |
| 全仓自动发现 | rglob + materials 白名单 + hidden 规则（被显式登记取代） |

## 配置归一

此前文档归属有四套机制并存（course.json / nav.json / rglob 全仓发现 / materials 白名单）。收敛为**单一 nav.json 显式登记**：

- 组名 + 相对路径，支持组内子标签 `{"sub": ..., "items": [...]}`（沿用既有 schema）
- 标题自动取自文档一级标题，不手写（本项目相对 docsite 的省事之处）
- 未登记 = 不进站点。docsite 的「所见即所得」心智 + 本项目的「少写一半字段」
- 教材五个专题组由 course.json 一次性转换生成（23 登记章 + 14 未登记章按目录归组），course.json 随即废弃

## 数据归档

learning.sqlite3（99M，学习记录）与 combined_dictionary.sqlite3（546M，词典库）移至 `~/workspace/english-archive/`。不在仓库内保留死数据；两库均可在需要时取回接续。

## 渲染器

自研 55 行 markdown 解析器替换为 vendor 的 marked.min.js + highlight.min.js（自 docsite/vendor/ 复制，离线可用）。收益：GFM 完整支持（嵌套列表、删除线等 readable 合集用到的方言）、代码高亮。新增 `/files/` 静态路由供 markdown 内相对路径图片使用（防路径穿越）。注意：readable 合集引用的 `images/*.png` 实际未下载过，路由已通、图片仍缺，日后按 HANDBOOK 补下载即可显示。

## 代价与边界

- 学习/词典功能不可经开关找回，须从 git 历史 + 归档目录恢复（有意为之：仓库四类内容中只有「正式文章」需要被站点服务）
- /api/catalog 全量下发正文（含 readable 合集约 6.5M），本地访问无感知；嫌大可改按需拉取
- github-dark.min.css 单一高亮主题，浅色模式下代码块沿用深色高亮
- 测试 9 → 2（test_server.py 单元 + test_reader.cjs 冒烟）

## 验证

python3 site/test_server.py 全绿；test_reader.cjs 冒烟全绿（首文档渲染、7 组 48 文档导航、答案折叠、md 深链改写、搜索、主题、/files/ 边界、移动端宽度）。
