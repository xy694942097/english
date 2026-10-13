# main 自动发布 GitHub Pages

2026-10-13 用户确认：push 到 main 自动构建发布。

- 工作流：`.github/workflows/pages.yml`，main push 与手动触发。
- 先运行 `site/test_server.py` 中只读界面与公开清单两个专项测试（完整本地测试依赖未入 Git 的原文合集），再构建公开清单，上传 Pages artifact 并部署。
- Pages Source 改为 GitHub Actions；不再依赖 gh-pages 分支发布。
- 公开范围仍由 `site/publish-nav.json` 控制；个人学习档案、原始材料不会自动公开。
- 当前其他任务未提交的教材与导航修改不随本次工程改动提交。
- 日常更新：提交需要发布的改动后 `git push origin main`；查看 Actions 运行结果。

验证状态：待完成干净提交构建与线上工作流验证。
