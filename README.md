# English 学习资料

网页和文件系统使用同一组织方式：

```text
course/
  词汇/
    生词与熟词新义.md
  表达练习/
  Chunks 收集/
    精选 Chunks.md
    Chunks 收集箱.md
    按作品整理的积累页…
  原文与参考资料/
    原文、教材与影视/
    表达与语法查阅/
  我的学习/
  编纂与维护/
```

`course/` 是教程目录。文档文件名取标题；nav.json 以项目根目录为基准登记 `course/...` 路径，只控制顺序和可见性。站点运行方法见 [site/README.md](site/README.md)。新增文章放进对应文件夹，再登记到同名前端分组。

当前学习知识按 **Chunks 与生词** 两类收拢：单项先添入对应文档，不为一个词或一个表达新建导航章节。真实句子的精读与迁移在“表达练习”中进行。原 26 篇零散学习章节的全文、练习和来源备份见 `engineering/archive/learning-chapters-2026-10-13/`；旧网页书签跳转到合并后的入口。

materials/ 保存原始下载数据及来源 manifest；references/ 保存生成工具和选材数据；engineering/ 保存工程记录与未展示旧资料；site/ 是查看器；progress/ 保留后台练习证据。它们不作为额外学习分组。

实际教学与录入规则见 [AGENTS.md](AGENTS.md)，迁移说明见 [course 目录迁移记录](engineering/design/course-directory-2026-10-13.md)。
