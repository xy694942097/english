# English Book 编辑分层清单

日期：2026-09-28。范围：`book/` 下 43 篇教学内容 Markdown；不含 README、TEMPLATE、BACKLOG、CHANGELOG。此清单决定**教学角色与站点可见性**，不代表用户已学会，也不宣称逐句完成语言审校。文件路径暂时保留，避免破坏生成脚本与原有相对链接；站点按 `nav.json` 呈现角色。

## 判定顺序

1. **正确性阻断**：已有明确错误、损坏句子或污染了衍生文档的材料，列为“隔离待修”；保留源文件，不进入站点目录和搜索，修复并抽检后再考虑恢复。
2. **用途**：有具体卡点、可管理的范围、语境与迁移练习的，进入“学习主线”；大量条目、长篇汇编或同一语料的视图，进入“查阅资料”。学习主线是**可试教**，不是全面质量背书。
3. **成熟度**：单条尚未形成完整讲解与练习的，列为“候选”；不因出自真实语料就自动入正式课程。
4. **学习证据另计**：资料已写、已讲解、独立作答、延迟迁移是不同状态；本清单只评材料。

## 学习主线 · 26 篇（可试教，仍需持续审校）

| 方向 | 文件 |
|---|---|
| 阅读与熟词生义 | `book/01-reading/01-context.md`；`02-resigned.md`；`03-evidence.md`；`04-outcomes.md` |
| 单词专题与辨析 | `book/03-四六级词汇/00-guide.md`；`01-familiar-verbs.md`；`02-evidence-claims.md`；`03-causes-effects.md`；`04-preposition-patterns.md`；`05-change-development.md`；`06-degree-quality.md`；`07-judgment-reasoning.md`；`08-abstract-meanings.md`；`10-take.md` |
| 句型与特殊句子 | `book/05-patterns/01-nothing-but.md`；`02-not-until.md`；`03-unfamiliar-shapes.md` |
| 句式骨架小章 | `book/08-frames/00-guide.md`；`01-degree-comparison.md`；`02-emphasis-focus.md`；`03-concession-contrast.md`；`04-stance-commentary.md`；`05-narrative-logic.md`；`06-condition-subjunctive.md`；`09-exam-recall.md` |
| 中文到英文表达 | `book/10-expression/01-relationship-options.md` |

这里保留章节导览页。对部分四、六级词汇章和家族骨架章尚未做完整的逐条词典复核；“可试教”只表示没有本次抽查已确认的阻断错误，并有相对完整的教学形态。实际练习从用户原答决定是否需降级或修订。

## 查阅资料 · 12 篇（待逐条审校）

| 类别 | 文件 | 放在查阅区的原因 |
|---|---|---|
| 词组与介词指南 | `book/01-reading/05-phrasal-verbs-guide.md`；`06-phrase-structures-guide.md`；`book/03-四六级词汇/09-phrase-index.md`；`11-prepositions-guide.md` | 体量或目录型用途高于单次教学用途；需要按真实卡点抽取小章 |
| 教材与真题骨架 | `book/08-frames/07-school-recall.md`；`12-readthrough-recall.md`；`13-cet4-readthrough.md`；`15-kaoyan-readthrough.md` | 每章条目多，章末迁移题覆盖少；先作有出处的检索库，使用前核对原文与语域 |
| 口语、叙事、长句 | `book/08-frames/16-oral-dialogue-actions.md`；`17-narrative-cognition-actions.md`；`19-long-sentences-guide.md` | 单条例句与实践密度不均，需挑重点形成短课 |
| 千句解析 | `book/09-guides/02-ielts-1000-analyzed.md` | 体量大，部分“解析”仅标语法类别；可查阅，不能把题量当已学知识 |

“待审校”是明确状态：来源可查不等于用法、难度和练习都已核准。查阅资料可以帮助编课和解答，但不作为按顺序学完的课程。

## 候选 · 1 篇（不在站点目录）

- `book/08-frames/18-self-picked.md`：活页仅登记一个骨架和一条例句。保留来源与思路，等增加自然语境、对比与迁移练习后再决定归入学习主线或查阅区。

## 隔离待修 · 4 篇（不在站点目录）

| 文件 | 已确认的阻断原因 | 恢复条件 |
|---|---|---|
| `book/01-reading/07-fixed-phrases-guide.md` | “中式英语”表将 `put forward a suggestion`、`solve a problem`、`get experience` 等可用表达误标为错误；其他规则尚需抽检 | 逐项核对所有 ❌／✓ 对照与义项边界，修订后再分类 |
| `book/09-guides/01-ielts-1000-sentences.md` | 第 5 句损坏为 `s.`；与另一千句视图重复且未完成一致性核验 | 回源修复、逐项比对两个视图，并审视“雅思级别”标签依据 |
| `book/08-frames/14-cet6-readthrough.md` | 原始 OCR 噪声 `social inedia` 被当正文引用；省略 `that` 的 it-cleft 被称为“假分裂” | 清理或标注文本噪声，复核句式分类及其余补编条目 |
| `book/08-frames/08-frames-collection.md` | 由分章合成，包含六级章的上述问题；直接修改会被再生成覆盖 | 上游六级章审校后修复总集生成脚本对已废弃 `course.json` 的依赖，重建并抽检 |

隔离不等于整篇毫无价值；它表示目前有已确认的错误足以阻断“放心拿来学”。原文件和历史保持可追溯。

## 恢复与后续审校次序

先核 `07-fixed-phrases-guide` 的错误对照，再修千句库的损坏数据与双视图一致性；随后核六级章原文噪声和分析，并重建总集。查阅区按用户实际遇到的卡点逐项复核，不按页数或表达条数宣称完成。每次把一篇移回学习主线前，确认来源、语义与边界、自然例句、练习解析和新语境迁移；学习者掌握仍由独立作答与延迟复测决定。
