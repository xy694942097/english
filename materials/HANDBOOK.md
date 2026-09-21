# 资料手册（HANDBOOK）——下载、选源与归一化规则

本页是本项目资料工作的**唯一规则处**（2026-09-16 定版，合并自 references/README「下载与归一化总则」与 materials/README「下载资料选源规则」）。此后下载新资料、做格式归一化、调整 catalog 可见范围，一律照本页执行，不需要重新决策。资料清单与批次记录见 [materials/README.md](README.md)；词表导入细节见 [references/README.md](../references/README.md)。

## 一、下载原则

1. **优先 GitHub 公开仓库与官方平台**（如国家智慧教育平台）；通用搜索引擎结果多为垃圾/网盘诱饵，直接搜仓库。探索仓库用 `gh api repos/<owner>/<repo>/git/trees/<branch>?recursive=1`，下载用 raw.githubusercontent.com 直链（中文路径 URL 编码）。
2. **来源必须可复核**：每个文件登记进 [downloads-manifest.json](downloads-manifest.json)（`{created_at, files:[...]}` 列表结构，每条含 bytes/sha256/source/url/description/downloaded）；manifest 是唯一登记处，写入前先读旧结构。下载完成即算 SHA-256，批量完成后全量复验。
3. **许可要记录**：有 LICENSE 的记类型（如 CC BY-SA / CC BY-NC-SA / MIT），无 LICENSE 的注明「仅本地个人学习使用，不再分发」。
4. **同一资料优先选文本原生格式**（txt/md/json）＞带文本层的 PDF＞扫描 PDF（需 OCR）；同一内容多版本时选紧凑版（如 300KB 文本版 PDF 而非 20MB 扫描版）。质量太差就找替代格式的资源，不硬转。
5. **版本边界如实披露**：社区整理版不宣称与官方发行版逐字一致；OCR 结果注明质量边界（如中文不可靠）；不可机读的部分明说并找机读替代层。

## 二、选源规则（格式优先序，同内容多源时严格取前者）

PDF 不是好的机器语料源：提取后断字（"fi ve"）、乱序、无 ToUnicode 的扫描件完全不可机读（考研手译本、2020 英一 OCR 件都是实证）。

1. **结构化带元数据（首选）**：JSON/JSONL/CSV/SQLite，且字段里带出处（版本/册别/单元/年份）。范例：高中教材句子库（每句带版本+册别+单元）、rich 版词表（词条直接带例句）。拿来即用，溯源成本为零。
2. **规整纯文本/Markdown**：可直接正则扫描。范例：六级 62 份 TXT、考研精翻 markdown、初中教材 md。
3. **文字层完好的 PDF（无替代时才收）**：收下不算完成——必须当场派生出 txt/md 并抽查派生物质量（断字、乱序、填空残片）；manifest 登记以原始 PDF 哈希为准，派生物在来源说明里注明。
4. **扫描/图片型 PDF（默认不收）**：仅当「人读原件」用途且无任何替代（如手译本）才收，登记时标注「不可机读，阅读件」，不进入任何挖掘/导入管线。

通用要求：下载前先明确用途（挖句式骨架/例句导入/阅读参考），不为「收而不用」而收；无 LICENSE 声明的仓库仅本地学习用；优先选带出处元数据的源。

## 三、目录分类（按资料形态与用途，不按考试）

`materials/` 下五类：`vocabulary/`（词表）、`dictionaries/`（词典数据）、`papers/`（真题试卷）、`textbooks/`（教材）、`corpus/`（平行语料）。新类别先建子目录再下载，manifest 的 file 路径与实际位置一致。

## 四、归一化规则（数据层与可读层分离）

- **数据层（原件）**：PDF/JSON/平行文本保持原样，绝不为统一格式而改写原件——格式本身是可复核性的一部分。原件不进 git（.gitignore 排除 materials/*，仅白名单 manifest 与 README/HANDBOOK）。
- **派生物**：PDF 抽文本用 pdftotext -layout（表格/排版保留更好）或 pypdf；扫描件 OCR 用 pytesseract（注意运行环境通常只有 eng 语言包）。派生物（*.txt 抽取件）放原件旁，哈希以原件为准，manifest 不登记派生物。
- **可读层（前端可见）**：想在网上读的内容转成 md。**纯文本类（txt）一律转 md**；**json/jsonl/csv 等结构化数据豁免**（转 md 是有损降维，查询走学习库/脚本），只保留 md 统计说明页。
- **生成物不手改**：`readable/`、`dictionaries/wordbooks-md/` 合集、真题原件旁 md 均为脚本生成物，重跑 `references/normalize_materials.py` 重建。
- **归一化前先抽查质量再批量**：中文层数汉字数（经验：手译版 26 万字符仅 188 汉字＝无 ToUnicode 映射不可机读）、OCR 先跑 2 页看样本。提取失败/质量差的，按第一节第 4 条换替代源（如手译版→阅读精翻 md 替代）。

## 五、catalog 可见范围（site/server.py 白名单）

materials 顶层 md（README/HANDBOOK）、`readable/` 子树（合集页）、`dictionaries/wordbooks-md/`（合集）入左侧目录；papers 原件旁 md 与 textbooks/ 教材原件不入目录（合集版在 readable/ 下，不重复）；其余数据文件不进目录。改放行范围必须同步 site/test_server.py 用例。

合集化原则（2026-09-16 用户定版）：学习资料是参考资料，大概率不细读，按考试专题各合 1 个文档——词源书三册各一、四/六/考研真题各一、考研精翻一、雅思真题/资料各一、初中教材一；宁少而全不多而碎。

学城（km）来源合集（2026-09-21）：个人学城知识库文档经 citadel CLI 导出后放 `readable/guides/`，按主题各合 1 个文档（语法表达类一、千句库一），每节前带 `<!-- 来源：学城文档 <id> <url> -->` 注释。学城侧为源，本地合集不随后续学城编辑自动更新；无 downloads-manifest 登记（非下载文件），来源 URL 即复核凭证。

## 六、工具速查

PDF 工具经 pdf skill 的 runtime 调用（`catdesk runtime exec --manifest ~/.catpaw/skills/pdf/dependencies.json --layer convert -- pdftotext ...`；OCR 层用 `--layer ocr`）。

归一化统一入口（子命令，幂等可重跑）：

```bash
python3 references/normalize_materials.py all      # 全量重建（papers/wordbooks/ielts/readable）
python3 references/normalize_materials.py papers   # 真题 txt → 原件旁 md + 精翻/词源转换
python3 references/normalize_materials.py ielts    # 雅思文字层分级与可读层
python3 references/normalize_materials.py readable # materials/readable/ 汇总层
```

## 七、不变式（改任何一处都要检查的联动点）

manifest 登记 ↔ 实际文件路径一致；改 catalog 白名单 ↔ test_server 用例；改归一化脚本 ↔ 重跑验证生成物不变；新批次下载 ↔ materials/README 批次记录 + CHANGELOG。
