# Better Call Saul S02E01：新版 Prompt 首轮试提

日期：2026-10-12。字幕原件：`materials/corpus/tv-subtitles/better-call-saul/S02/Better.Call.Saul.S02E01.en.srt`。共 701 条，范围 1–701；SHA-256：`8d062932b7fd31afc0bea0771bb4607b6118b83960f27967980e098b08cee5c7`。这是本地社区字幕，未听校。

## 执行与结果

按 `engineering/agents/chunks-expression-coach-prompt.md` 的新流程，依编号顺序分七段读完整集，合并跨字幕行的句子；分别检查表达骨架和句内搭配。随后重看未选字幕，重点回查短回应、普通搭配、服务场景套语和同句中的另一层表达。保留 92 项候选，按时间排序，已写入 `course/Chunks 收集/Better Call Saul：Chunks 积累.md` 的 `S02E01` 小节；每条的 cue、时间码和原句存 `references/chunks/better-call-saul-s02e01-selection.json`。

第一遍先列 82 项；第二遍及筛选修订后，最终新增了 20 个第一遍未留下的有效条目，并移除了重复项与单词义项，落地 92 项。第二遍补进的类型包括 `It's got no legs.`（cue 260）、`if you get a chance`（427）、`dole out assignments`（520）、`be exposed to the elements`（561–562）、`the more…, the less…`（567–568）、`Just wondering your thoughts.`（575）、`change sth. out`（670–671）。这说明补漏步骤确有实际作用；它不能证明没有其他遗漏。

## 有意不收录

跨集相同表达、同一功能且没有独立新义的 9 项未在本集重复收录：

| 表达 | 已收集于 |
|---|---|
| `on God's green Earth` | S01E10；本集重放旧场景 |
| `I hate to do this, but…` | S01E05 |
| `Help me out here.` | S01E10；本集重放旧场景 |
| `Your point being?` | S01E10；本集重放旧场景 |
| `That's as far as it goes.` | S01E10；本集重放旧场景 |
| `part ways` | S01E07 |
| `I'll tell you what.` | S01E04 |
| `believe it or not` | S01E06 |
| `time is of the essence` | S01E03 |

`ballpark`（cue 361）、`rock-solid`（383）、`low-maintenance`（686）主要是单词义项，暂留作词汇轨道候选，本轮未新建 S02 词汇页。`the gravy train` 已覆盖同场的 `All aboard` 比喻；`toss sth. away` 已覆盖本集较早的 `throwing away money`。`catch lightning`（390）在字幕中不是完整的常见习语，未把它当标准模板。用户明确表示不需要反复收的 `Can we just talk?` 也未录入。

## 校验边界

选中条目的原句已从连续字幕 cue 回取，展示层只去 HTML 标签、合并字幕断行；原始 SRT 未改。`the more…, the less…` 的字幕后半句较别扭，学习页已提示，不把该原句当完全规范的仿写模板。92 是候选积累数，不是用户掌握数；单集出现不证明常见频率。要检验新版 Prompt 的真实漏选率，还需要用户用本集指出漏项，或用新集做独立复查。
