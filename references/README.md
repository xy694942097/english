# 来源数据与生成工具

这里是后台工作目录，不映射为前端学习章节。原始下载文件在 materials/，可读学习内容在 course/；本目录保存它们之间的选择依据和生成工具。

| 位置 | 内容 |
|---|---|
| chunks/ | Better Call Saul 的 Chunks 与词汇选择、原句定位 |
| ted/ | TED 选择数据、来源及渲染器 |
| presidential-speeches/ | 总统演讲选择、来源和去重证据 |
| translation-training/ | 练习题源、目标 Chunk 关联和覆盖记录 |
| subtitles/ | 字幕获取与处理的辅助代码 |
| 根目录 Python 脚本 | 素材获取、索引归一化、文档渲染与路径兼容 |

当前内容渲染入口：build_bcs_vocabulary.py、build_presidential_speeches.py、ted/render_learning.py。下载与归一化执行规则只维护在 [materials/HANDBOOK](../materials/HANDBOOK.md)。脚本重跑前先看其输入输出，保留源 ID、引文和来源证据。
