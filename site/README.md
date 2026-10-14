# English Book 本地站点

只读 Markdown 站点：侧边栏目录、全文搜索、右侧自动目录、标题折叠与深浅主题。2026-10-13 按用户要求移除编辑功能，支持生成 GitHub Pages 静态网站。

## 运行

```bash
cd /Users/xianyi/workspace/learn/english
python3 site/server.py            # http://127.0.0.1:4174，可用 --port 换端口
```

只监听回环地址。Python 3.10+，无其他运行依赖；前端零安装、无 CDN（marked 和 highlight.js 在 `site/public/vendor/`）。

## 配置 nav.json

侧边栏目录由根目录 `nav.json` 显式登记，改完刷新页面即生效（服务端禁用缓存）：

```json
{
  "groups": [
    {"title": "组名", "items": ["course/组名/yyy.md"]},
    {"title": "有子标签的组", "items": [
      "course/有子标签的组/a.md",
      {"sub": "子标签", "items": ["course/有子标签的组/子标签/b.md"]}
    ]}
  ]
}
```

- 教程统一放在 `course/`；其下前端组名／子标签与实际父目录同名。nav.json 使用相对项目根目录的 `course/...` 路径，只控制排序与可见性。
- 路径相对仓库根；**标题自动取自文档的一级标题 `# `**，无需手写
- 未登记的文件不会出现在站点里（搜索也搜不到）
- 学习主线按 Chunks 收集、Shadowing、词汇排序；原文与参考资料、我的学习为辅助分组。当前知识入口收拢为“生词与熟词新义”和“精选 Chunks”；原文候选与编纂资料分别保留在来源组和维护入口。
- `maintenance` 与 `groups` 使用相同条目格式，在下方独立折叠的“编纂与维护”入口展示；仍可通过深链访问和全文搜索。

## 功能说明

- **首页**：直接打开网站显示用途简介、精选入口和内容分区；点击站点名称或侧栏“首页”可返回。分区依据当前目录生成，电脑双列、手机单列。文档深链继续直接打开文章。
- **左右侧栏**：左侧知识导航可由屏幕左边中间的按钮收起与展开，并记住本机选择；右侧文章目录从屏幕右边中间打开，悬停显示操作名称。
- **搜索**：顶栏输入框，前端全文过滤标题与正文（正文随 /api/catalog 一次下发，本地访问无感知）
- **深链**：`#文档路径` 打开文章，`#编码后的文档路径::编码后的标题锚点` 打开指定小节，支持刷新及浏览器前进／后退；相对 `.md#标题锚点` 链接自动转换。
- **右侧目录**：从 h2/h3 自动生成，点击屏幕右边中间的小图标打开目录抽屉，h3 缩进；展开后将指针移到边缘按钮会显示“收起目录”；点击该按钮、目录条目或按 Escape 可关闭。正文中不插入目录。所有标题获得稳定的 Markdown 风格锚点，重复标题追加 `-1`、`-2`。文章中 `[文字](#标题锚点)` 也可跳转。跳入折叠的参考答案会自动展开。源 Markdown 不需额外维护一份重复目录。
- **图片**：markdown 里的相对路径图片经 `/files/` 路由加载（路径穿越被拒）
- **参考答案**：正文 `## 参考答案` 或 `## 参考 Chunk` 之后的内容默认折叠
- **渲染**：marked（GFM：表格、删除线、嵌套列表等）+ highlight.js 代码高亮；不执行原始 HTML
- **主题**：跟随系统深浅色，可手动切换并记忆

## 验证

```bash
python3 site/test_server.py        # 单元：目录、路径、只读界面与静态构建
python3 site/server.py &
ENGLISH_TEST_URL=http://127.0.0.1:4174 node site/test_reader.cjs   # Playwright 冒烟
```

浏览器测试需本机 Playwright，或用 `PLAYWRIGHT_MODULE` 指定模块路径（如全局 npm 安装位置）。

## 已归档数据

学习记录（learning.sqlite3）与合并词典库（combined_dictionary.sqlite3）已移出仓库至 `~/workspace/english-archive/`。若日后恢复学习功能，从该目录取回数据库，并在 git 历史中找回 `learning_store.py` / `dictionary_store.py`（2026-09-23 之前的提交）。

## 2026-10-11 文档目录迁移

面向学习的文档统一位于 `course/`，当前同名前端目录为“Chunks 收集／Shadowing／词汇／原文与参考资料／我的学习／编纂与维护”；表达练习已归入 Chunks。旧书签（包括迁移前根目录路径和更早的 book/ 路径）通过 aliases 直接映射到现址；原始下载数据和工程工具保留在后台目录。

## 标题折叠

文章的二级及以下标题可以点击收起其正文与子标题；“展开正文／收起正文”控制当前文章的标题块。右侧目录定位时会展开目标的父级。参考答案和参考 Chunk 保持单独折叠。

## GitHub Pages 发布

先审阅 `site/publish-nav.json` 的公开清单（含原文与参考资料、编纂与维护；不含个人学习与 Shadowing 记录），再运行：

```bash
python3 site/build_static.py
```

输出为 `site/dist/`，只包含选中的文章正文、阅读器资源及明确引用的图片。八篇本地全文合集以来源入口页展示，其他选中文档正常阅读；个人档案和原始材料不进入站点。构建目录须为空；可用 `--output` 指定新目录。

正式发布由 `.github/workflows/pages.yml` 自动执行：提交改动并 `git push origin main` 后，GitHub Actions 先运行只读界面与公开清单的专项测试（完整本地测试包含未入 Git 的原文合集），再按 `site/publish-nav.json` 构建并发布。也可在 Actions 中手动运行 Publish reading site。

仓库 Settings → Pages 的 Source 设为 **GitHub Actions**。构建失败不会替换现有网站；更新结果可在 Actions 的 Publish reading site 查看。推送其他分支不会发布。

公开仓库可使用免费 Pages，地址为 `https://xy694942097.github.io/english/`。`site/deploy_pages.py` 是旧的 gh-pages 分支发布工具，日常发布无需运行；不要与 Actions 发布混用。
