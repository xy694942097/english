# 词表下载与导入记录（已归档）

2026-09-23 站点收敛为纯查看器时，词表导入线整体归档：学习库（learning.sqlite3）与词典库已移至 `~/workspace/english-archive/`，`materials/vocabulary/`（词表原始数据）与 `materials/dictionaries/`（ecdict/wordnet/wordbooks）一并移去同处。本页只留历史记录与恢复指引。

## 当年做了什么（2026-09-14 批次）

- 导入四级 4544 词 / 六级 3991 词 / 专八 12410 词 / NGSL 高频 2809 词及关联词组到 learning.sqlite3，合计 53972 条
- 来源：[KyleBing/english-vocabulary](https://github.com/KyleBing/english-vocabulary)（上游 kajweb/dict 整理，非逐项核验的官方大纲）、[NGSL 1.2 社区镜像](https://github.com/RealKai42/qwerty-learner/pull/1069)（CC BY-SA 4.0，未与官网 CSV 逐项比对）
- 处理规则、质量边界与导入报告见 [references/README.md](../references/README.md)；脚本 import_wordlists.py / import_voc_examples.py 仍在 references/

## 恢复路径

原始数据在 `~/workspace/english-archive/vocabulary/` 与 `~/workspace/english-archive/dictionaries/`（SHA-256 见 materials/downloads-manifest.json，或按 URL 重新下载）；导入脚本在 git 历史与 references/ 现存文件中。若重建学习库：恢复 learning.sqlite3（同归档目录）后重跑导入脚本即可。

下载、选源与归一化规则仍是 [materials/HANDBOOK.md](HANDBOOK.md)——日后新下载照手册执行。
