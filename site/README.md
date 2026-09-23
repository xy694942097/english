# English Book 本地站点

纯 markdown 文档查看器：侧边栏目录 + 关键词全文搜索 + 深浅主题切换。只读，无学习记录、无词典、无对话后端（2026-09-23 收敛，决策记录见 `engineering/design/site-simplification-v2.md`）。

## 运行

```bash
cd /Users/xianyi/workspace/learn/english
python3 site/server.py            # http://127.0.0.1:4174，可用 --port 换端口
```

只监听回环地址。Python 3.10+，无其他依赖；前端零安装、无 CDN（marked 与 highlight.js 在 `site/public/vendor/`）。

## 配置 nav.json

侧边栏目录由根目录 `nav.json` 显式登记，改完刷新页面即生效（服务端禁用缓存）：

```json
{
  "groups": [
    {"title": "组名", "items": ["book/xxx/yyy.md"]},
    {"title": "有子标签的组", "items": [
      "a.md",
      {"sub": "子标签", "items": ["sub/b.md"]}
    ]}
  ]
}
```

- 路径相对仓库根；**标题自动取自文档的一级标题 `# `**，无需手写
- 未登记的文件不会出现在站点里（搜索也搜不到）
- 教材五个专题组由原 course.json 转换而来（2026-09-23），此后增删章节直接改本文件

## 功能说明

- **搜索**：顶栏输入框，前端全文过滤标题与正文（正文随 /api/catalog 一次下发，本地访问无感知）
- **深链**：`#文档路径` 直接打开，hash 变化即路由；文档内相对 `.md` 链接自动改写为站内跳转
- **图片**：markdown 里的相对路径图片经 `/files/` 路由加载（路径穿越被拒）
- **参考答案**：正文 `## 参考答案` 之后的内容默认折叠
- **渲染**：marked（GFM：表格、删除线、嵌套列表等）+ highlight.js 代码高亮；不执行原始 HTML
- **主题**：跟随系统深浅色，可手动切换并记忆

## 验证

```bash
python3 site/test_server.py        # 单元：目录登记、标题提取、路径边界
python3 site/server.py &
ENGLISH_TEST_URL=http://127.0.0.1:4174 node site/test_reader.cjs   # Playwright 冒烟
```

浏览器测试需本机 Playwright，或用 `PLAYWRIGHT_MODULE` 指定模块路径（如全局 npm 安装位置）。

## 已归档数据

学习记录（learning.sqlite3）与合并词典库（combined_dictionary.sqlite3）已移出仓库至 `~/workspace/english-archive/`。若日后恢复学习功能，从该目录取回数据库，并在 git 历史中找回 `learning_store.py` / `dictionary_store.py`（2026-09-23 之前的提交）。
