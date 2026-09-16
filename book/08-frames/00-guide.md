# 句式框架（Frames）：比语法分析高一层的学习单位

本章解决：单个语法规则都懂，句子还是读不顺、写不出。把学习单位从"规则"升级为"框架"。

专题起源：2026-09-16 拆解诊断句 `more ambitious than anyone in the room had thought feasible, let alone advisable` 时确认——学习者缺的不是语法知识，而是**没见过这个框架**。就像见过 so...that 一样，框架是母语者整存整取的预制件。

## 一、什么是框架

框架 = **半固定的句子级模板**：一部分词序、虚词是固定的，留下若干槽位填内容。

```
more [A] than anyone had thought [B], let alone [C]
   固定骨架 ________________________  槽位：A/B/C 均为形容词
```

它和三个已知概念的关系：

- 比语法规则**高一层**：语法规则描述所有可能句子，框架只描述母语者高频使用的那一小撮。知道 than 从句的语法，不等于见过"than 从句里塞宾补省略"这个具体用法。
- 和词组（chunks）同族但更大：词组是词级预制件（take issue with），框架是**句级预制件**。语料库语言学（Pattern Grammar, Hunston & Francis）和构式语法（Construction Grammar）在学术上就是这个观点：语言知识很大程度以"形式-意义配对的构式"存储，不是规则+词表。
- 加工优势直接继承词块：整存整取，不占实时句法资源。这正是"读得慢、写不出"的对症药——**记一个框架，等于把一整段句法计算变成一次查表**。

## 二、怎么学一个框架（四步，接证据分级）

1. **Notice 注意**：在真实语料里撞见它（阅读、影视、文档都算）。没撞见过的框架不提前背。
2. **Unpack 拆解**：难的框架拆一次内部结构（本书负责），拆通即可，不必每次重新分析。
3. **Imitate 仿写**：用自己的内容同构写一句。仿写通过 = 证据分级里的"能够运用"入门。
4. **Collect 变体**：之后在语料中遇到变体（如 more than words can express 是换了比较基准的变体），追加记录。

不按此流程"背框架清单"——下面的索引是**地图和采集登记表**，不是背诵任务。状态列里"已学"指已完成 Notice→Unpack→Imitate 至少一轮。

## 三、框架索引（六大家族）

例句均为教学自造。每条含：形式 / 语义 / 例句 / 结构注（难者）。详细拆解见各家族专章（逐步扩编）。

### 家族 A：程度与比较（详见 [01-degree-comparison](01-degree-comparison.md)）

> 2026-09-16 已按定版风格「紧凑学习卡」重写：每框架固定顺序（语义→例句→结构拆解→误读/变体表），例句大半换成 voc14w 语料真实例句并标注（语料）/（自造）。

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| more [A] than anyone had thought [B] | 比任何人认为[B]的上限还[A] | The refactor ran longer than anyone had thought possible. | than 从句里 thought 的宾语 it 被省，B 是宾补 | 已学 09-16 |
| [A], let alone [B] | 前项尚且达不到，后项更别提 | He can't walk, let alone run. | let alone 是连词，B 平行于前项同位置成分 | 已学 09-16 |
| not so much [A] as [B] | 与其说[A]不如说[B] | It was not so much a mistake as a misunderstanding of the requirements. | A、B 语法类别须对等；语义重心在 B | **已编 09-16（各家族章）** |
| nothing less than [X] / nothing short of [X] | 简直是、不折不扣的 | The delay was nothing short of a disaster for the launch plan. | 双重否定出强肯定，常带评价色彩 | **已编 09-16（各家族章）** |
| if anything | 甚至可以说；恰恰相反 | The new version isn't slower — if anything, it's faster. | 句首/句尾插入的评注语 | **已编 09-16（各家族章）** |
| all the more [A] because [B] | 正因[B]而更[A] | The silence was all the more striking because everyone had expected an answer. | all the more 修饰比较级 | **已编 09-16（各家族章）** |
| nothing if not [A] | 极其[A]（不常用） | The documentation is nothing if not thorough. | 字面"如果不是A就什么都不是"→极A | **已编 09-16（各家族章）** |

### 家族 B：强调与聚焦

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| What … is/was … | （假分裂）…的是 | What the team needed was a rollback plan, not a patch. | what 从句做主语，is 后是信息焦点 | **已编 09-16（家族B章）** |
| Only [when/after…] did … | 直到…才（倒装） | Only after the third retry did the service come back up. | only+状语前置触发部分倒装 | **已编 09-16（家族B章）** |
| It was [X] that … | （分裂句）正是X | It was the config file, not the code, that caused the outage. | 强调 X，其余部分挂 that 后 | **已编 09-16（家族B章）** |
| not until …（it was not until … that …） | 直到…才 | It was not until the logs were correlated that the pattern emerged. | 详见 [05-patterns/02-not-until](../05-patterns/02-not-until.md) | 已编 |
| do/does/did + 动词原形 | （口语强调）确实 | The test did pass yesterday — I checked twice. | 助动词强调，书面少用 | **已编 09-16（家族B章）** |

### 家族 C：让步与对照（详见 [03-concession-contrast](03-concession-contrast.md)）

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| [A/Adv/N] as/though [S V] | 尽管…（倒装让步） | Strange as it sounds, the bug only appears on Tuesdays. | 表语/状语/名词提前，as=though | 已见（06章 Try as he might） |
| much as [S V] | 尽管… | Much as I admire the design, I can't defend the cost. | much as 整体=although | **已编 09-16（各家族章）** |
| for all [X] | 尽管[有]X | For all its popularity, the framework has serious gaps. | for all + 名词短语 | **已编 09-16（各家族章）** |
| far from [A/V-ing] | 不但没有 | Far from improving latency, the patch made it worse. | far from 后接动名词/形容词 | **已编 09-16（各家族章）** |
| be that as it may | 即便如此（不常用） | Be that as it may, we still have to ship this week. | 固定虚拟式让步句 | **已编 09-16（各家族章）** |

### 家族 D：评述与立场（stance）（详见 [04-stance-commentary](04-stance-commentary.md)）

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| if you will / so to speak / as it were | 可以这么说（缓冲语） | We painted ourselves into a corner, so to speak. | 插入语，不占句子成分 | **已编 09-16（各家族章）** |
| granted / admittedly / to be sure | 诚然…（先让后转） | Admittedly, the test coverage is thin — but the risk is contained. | 先承认再转折的论证套路 | **已编 09-16（各家族章）** |
| suffice it to say (that) … | 无需多说，只说一句（不常用） | Suffice it to say the migration did not go smoothly. | 固定虚拟式 | **已编 09-16（各家族章）** |
| far be it from me to [V] | 我岂敢…（不常用，反语客气） | Far be it from me to question the architect, but has anyone profiled this? | 固定虚拟式+不定式 | **已编 09-16（各家族章）** |
| There is no [V-ing] | …是不可能的 | There's no denying the results speak for themselves. | no+动名词，there be 存现句 | **已编 09-16（各家族章）** |
| [X] is one thing; [Y] is another | X是X，Y是Y（不可混同） | Writing the code is one thing; maintaining it is another. | 平行名词化结构 | **已编 09-16（各家族章）** |

### 家族 E：叙事与逻辑推进（详见 [05-narrative-logic](05-narrative-logic.md)）

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| What began as [X] ended up [Y] | 始于X而终于Y | What began as a quick fix ended up reshaping half the module. | 假分裂+end up V-ing | 已见（诊断句Q10） |
| What [S] failed to anticipate was [Y] | 没料到的是 | What we failed to anticipate was how fast the data would grow. | 假分裂，焦点在补语 | 已见（诊断句Q2） |
| That [X], rather than [Y], was [Z] | 是X而非Y | That the delay was caused by DNS, rather than the database, was confirmed by the traces. | that 主语从句+rather than 平行插入 | **已编 09-16（家族B章）** |
| not least because | 尤其因为 | The plan survived, not least because two engineers refused to let it die. | not least=特别是，不弱化反而加重 | **已编 09-16（各家族章）** |
| insofar as | 在…范围内 | The tool helps, insofar as you already know what to look for. | 程度限定从句连词 | **已编 09-16（各家族章）** |

### 家族 F：条件与虚拟（不常用，书面）（详见 [06-condition-subjunctive](06-condition-subjunctive.md)）

| 框架 | 语义 | 例句 | 结构注 | 状态 |
|---|---|---|---|---|
| Were it not for [X] / But for [X] | 若非X | Were it not for the backup, we would have lost everything. | 省 if 的虚拟倒装 | **已编 09-16（各家族章）** |
| Should you [V] | 若您…（正式） | Should you encounter this error, file a ticket immediately. | 省 if 倒装，技术文档高频 | **已编 09-16（各家族章）** |
| as it stands | 以现状而论 | As it stands, the system can handle ten thousand users at most. | 独立评注语 | **已编 09-16（各家族章）** |

## 四、与既有内容的关系

- **05-patterns（nothing but / not until）**：本就是框架学习，现归入框架专题家族 A/B，原文件保留。
- **06-sentences（特殊句子）**：框架是它的解药——"结构陌生"的句子，多数是没登记过的框架。诊断句 Q2/Q4/Q7/Q10 已按此登记。
- **诊断（2026-09-16）**：盲区"两层嵌套+省略"与框架家族 A/B 直接对应，框架法是针对该盲区的主处方。

## 五、扩编规则

- 每个框架必须有**至少两条不同语境例句**才能入索引；难的框架附结构注。
- 只从真实卡点或真实语料登记新框架，不为凑数批量造框架。
- 家族专章按学习进度逐个展开，索引先行、专章跟上，避免"编完没人学"。

## 六、六大家族不是封闭分类（2026-09-16 用户确认）

六大家族只是当前索引的组织方式，**不是框架的定义域**。框架的判定标准只有一条：半固定骨架+槽位、母语者整存整取。据此：

- `not only ... but also ...`、`either ... or ...` 这类初高中教过的成对连接结构**就是框架**（词组级到句级的连续谱，not only...but also 属于最接近句子骨架的那一端），应从学过的教材中回收登记，不必重新发明。
- 索引扩编的两条主要来源：①真实语料归纳（见下）；②初高中教材/已学搭配回收。
- 长期方向：建立例句语料库（VOA/新闻/文学/影视台词），以语料归纳框架为常态扩编方式，而非依赖个人想到什么写什么。第一步先利用本地词典 examples 表（3.2万条，CET 词表自带）；后续再评估下载外部语料。
- 计划中的特殊章：**"没有框架的句子"**——讨论什么样的句子不含可提取骨架（成分完全自由组合的句子、一次性修辞性结构等），与框架章互为边界。此章先讨论后落笔（待用户确认）。

## 七、语料库与例句资源现状

- 本地 combined_dictionary.sqlite3 的 examples 表：**17.4 万条**（原 CET 例句 3.2 万 + 2026-09-16 新导入 voc14w 14.1 万，来自 github.com/zhenghaoyang24/english-vocabulary，中英对照含热度，导入脚本 references/import_voc_examples.py）。特点仍是单词对应型短句：查词/框架章配真实例句够用，**连贯文本归纳框架仍需新语料**。
- 框架归纳语料候选（待用户授权下载）：Tatoeba 英中子集（CC-BY，自然句）；OpenSubtitles/OPUS 影视字幕英中平行语料（口语域，对接交流目标）。体量控制在十万句级。
- 中文书籍先验（自行搜寻下载渠道，注意版权）：旋元佑《语法俱乐部》（句型思维最好的中文语法书）；《葛传捯英语写作》；《牛津英语搭配词典》英汉双解版（词级框架的人工编纂版）。

## 用法来源

框架概念：Hunston & Francis, Pattern Grammar (2000)；Goldberg, Constructions（构式语法）；词块加工优势见 engineering/methodology/2026-09-16-sla-research.md 第四节。例句自造，不冒充语料统计。
