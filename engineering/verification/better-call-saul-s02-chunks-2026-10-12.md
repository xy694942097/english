# Better Call Saul S02 Chunks：全集选材与核查

日期：2026-10-12。沿用 `engineering/agents/chunks-expression-coach-prompt.md` 的全集流程：按 cue 顺序分段通读，检查每句的表达动作与内部搭配，再回看未选字幕。原件是 `materials/corpus/tv-subtitles/better-call-saul/S02/` 中十集本地英文社区字幕；没有听音校对。读者页是 `Chunks 收集/Better Call Saul：Chunks 积累.md` 的 S02E01–S02E10 小节，逐条出处在 `references/chunks/better-call-saul-s02e01-selection.json` 至 `better-call-saul-s02e10-selection.json`。

| 集数 | 连续字幕 cue | 保留候选 |
|---|---:|---:|
| S02E01 | 701 | 92 |
| S02E02 | 557 | 109 |
| S02E03 | 669 | 104 |
| S02E04 | 535 | 115 |
| S02E05 | 656 | 140 |
| S02E06 | 488 | 84 |
| S02E07 | 619 | 118 |
| S02E08 | 637 | 98 |
| S02E09 | 708 | 105 |
| S02E10 | 604 | 93 |
| 合计 | 6,174 | 1,058 |

## 去重和分轨

与先前已收条目比较时，完全相同的表达、相同意思和用途不再重复建条目；S02E01 的 S01E10 对话重放尤其如此。首轮筛选里另外发现并跳过 43 个与先前条目相同用法的明确重复候选：E02 4、E03 10、E04 6、E05 5、E06 1、E07 4、E08 4、E09 4、E10 5。这里的数字是明确记录的同形重复，不包括逐句阅读时未提为候选的普通复现。

**同形新义保留两项**：E04 `It's on me.` 是“责任在我”，E07 是“我请客”；E04 `be up to sth.` 是“在搞什么”，E09 是“有本事／可能做某事”。其余跨集英文标题经规范化比较无重复。近似表达若只换宾语而不增加新的学习点，也在人工筛选时略去；形似但句法和使用场景有独立价值的表达仍可并存。

单词义项与可复用表达分轨：例如 `ballpark`、`rock-solid`、`low-maintenance`、`labor-intensive`、`heart-rending`、`snag`、`tailor-made`、`doctor`（篡改文件）和 `DNR`，本轮未把它们伪装成多词 chunk，也没有新建 S02 词汇页。此处是代表性转轨候选，并非第二季词汇的全面提取。

不把剧中临时杜撰或不宜优先仿用的说法当通用模板：E02 的 `deaf as a doornail` 意思可懂，但本轮优先教学 [Cambridge 收录的 `deaf as a post`](https://dictionary.cambridge.org/us/dictionary/english/as-deaf-as-a-post)；`deaf as a doornail` 另有旧式用例，不能武断称为角色说错或字幕错误。E02 的 `a fishing trip` 在本句指警察套取信息，阅读页标明更常见的说法是 [Collins 收录的 `fishing expedition`](https://www.collinsdictionary.com/us/dictionary/english/fishing-expedition)；E05 的 `set the ship straight` 未当作固定习语收录。`get sb. out of Dutch`（E05）按“摆脱麻烦”记录，并注明旧式用法；[Dictionary.com 的 in Dutch 释义](https://www.dictionary.com/browse/in-dutch)用于核对意思。这些查阅均不能证明本集表达的总体频率。

## 技术核查与边界

十集 selection JSON 均记录源路径、原件 SHA-256、cue 范围、起止时间及连续 cue 的原句。已核对字幕编号从 1 连续到每集末条、所有 1,058 条引文与时间码可由原件重建、学习页标题与 JSON 一一对应且逐集按时间排序。`python3 site/test_server.py` 六项通过；浏览器 `site/test_reader.cjs` 的文档渲染、折叠、目录跳转与移动端宽度检查通过，无页面错误。阅读页只移除字幕 HTML 标记并合并断行，不改原始 SRT。上述校验保证**已选条目的出处一致**，不能证明再无漏选，也不能把候选数等同于用户掌握数。
