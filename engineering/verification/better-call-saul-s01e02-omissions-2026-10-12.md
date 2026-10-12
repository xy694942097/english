# Better Call Saul S01E02：遗漏候选复查

2026-10-12。按字幕第 1–612 条顺序复看，对照本集现有 50 条；只记录能迁移的固定／半固定表达、常用搭配或句式骨架。这里是候选清单，不是最终录入，也不代表用户尚未掌握。

| cue | 遗漏候选（保留字幕形式） | 值得复查的点 |
|---:|---|---|
| 18 | `stood on the gas` | 踩油门；动词搭配 |
| 50 | `damn straight` | 那当然／说得对；口语强语气 |
| 63 | `hurry it up` | 快点；口语命令 |
| 130 | `a minor fender bender` | 轻微剐蹭；交通口语名词短语 |
| 141 | `could have gone a couple ways` | 可能有几种情况；推断骨架 |
| 145 | `go with glass half full` | 按乐观方向判断；隐喻 |
| 155 | `Signed, sealed, and delivered.` | 说定／办妥；套语 |
| 169 | `clear 2 grand` | 净赚两千美元；金钱口语搭配 |
| 177 | `taking a header` | 头朝下摔；口语短语 |
| 200 | `it turns out…` | 结果发现……；叙述骨架 |
| 235 | `You got me.` | 你识破我了／被你抓到了；回应套语 |
| 258 | `The next words out of your mouth…` | 你接下来说的话……；强调式骨架 |
| 271 | `a bad case of…` | 严重的……；半固定搭配 |
| 319 | `from dawn till dusk` | 从早到晚；固定短语 |
| 326 | `they're all she's got` | 他们是她仅有的依靠；all sb. has got 骨架 |
| 338 | `beat the living hell out of sb.` | 把某人狠揍一顿；粗俗强化说法 |
| 348 | `eye for an eye` | 以眼还眼；固定说法 |
| 369 | `hit them where they live` | 击中他们最在乎／最依赖之处；比喻 |
| 433 | `take it black` | 咖啡不加奶；常用搭配 |
| 488 | `It's showtime, folks.` | 该上场了／开始干活了；口语套语 |
| 498 | `look sharp` | 看起来精神体面；熟词搭配 |
| 578 | `have no recourse` | 没有求助／追索途径；搭配 |
| 582 | `a finder's fee` | 介绍费／线索酬金；名词搭配 |
| 599 | `I owe you.` | 我欠你个人情；人际表达 |

共 24 项。边界：词汇型的 `fender bender`、`finder's fee` 等是否进入 Chunks 页，需按词块／词汇分轨筛选；粗俗表达要标语域。`throw some oil on troubled waters`（cue 197）偏离常见的 `pour oil on troubled waters`，暂不把字幕原句当作标准模板。`Could happen to anyone`、`keep my mouth shut` 等也可讨论，但本轮保守清单未计入。

## 漏选原因与流程回查

现行 Coach Prompt 在本次修改前已经要求逐句通读、检查外层骨架与内部词块；因此不能把漏选归因于完全没有这条原则。较有把握的解释是**执行缺少覆盖记录和第二遍复核**：原有 49 项及后来补入的 `You got a mouth on you.` 均可对回原句，但来源与时间码校验只验证已选项，不会暴露未选项。

这 24 项显示了几种容易被第一遍忽略的形式：短回应／套语（`damn straight`、`You got me.`、`I owe you.`）、普通词组成的固定搭配（`take it black`、`look sharp`）、句中骨架（`could have gone a couple ways`、`The next words out of your mouth…`）、强语气口语（`beat the living hell out of sb.`），以及应在词汇轨道复核的名词短语（`fender bender`、`finder's fee`）。这些归类是对漏例的事后分析，不能据此证明某个具体模型当时如何取舍。

已将“分批连续读—两层扫描—候选留痕—未选字幕第二遍复查—覆盖与出处核对”写入 `engineering/agents/chunks-expression-coach-prompt.md`。这份 S01E02 清单可以作为**回归用例**：改版流程应至少能发现这些项目并为未收录项给出转轨、重复或舍弃理由；它不是未经提示的独立效果测试。未来整集首次提取的实际漏选率，仍需用未参与编写规则的新集和用户反馈检验。
