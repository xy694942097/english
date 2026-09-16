# 教材回收：通读篇

本章解决：教材里那些**没有钩子词**的句子骨架——regex 搜不出来、只有逐句通读才能发现的结构型框架。来源与 07 章不同：不是预设模式扫描，而是 2026-09-16 对初中五册+高中人教 8,523 句全语料做 LLM 逐句通读（16 批 × 300 句，方法见 methodology/2026-09-16-frame-mining.md），聚类去重得 67 个候选，按三条判据（骨架/误读/语域）筛出本章收录的 12 个，例句全部为通读阶段逐字命中并经双重校验。

**语料与披露**：通读池 4,649 句（≥8 词信息句，剔除练习指令、题目模板、填空残片、断字行——指令模板的同构重复是伪框架源，如 "Combine each pair of sentences using..." 已在池外）。例句后的全语料反查计数基于定制 regex，结构型框架（同位语插入等）计数为下限。教材为社区 OCR 整理版，不宣称与官方出版物逐字一致。

## 本章预览

| 编号 | 框架 | 一句话语义 |
|---|---|---|
| 1 | one of the + 最高级 + [复数N] | 位居最…之列 |
| 2 | What [小句] is/was [焦点] | 之所以…，关键在于… |
| 3 | Could you (please) tell me [wh-陈述语序] | 请问… |
| 4 | [V] + 疑问词 + to do | 搞清楚怎么做/怎么办 |
| 5 | with + [NP] + [补语] | 带着/伴随… |
| 6 | [S] have/get [O] [V-ed] | 让人把…做了 |
| 7 | [前句], which [谓语] | 这意味着…/其中… |
| 8 | [主句], V-ing [结果/评注] | 从而/结果… |
| 9 | Some [A], (and) others [B] | 有的…有的… |
| 10 | Not all/every [A] + [肯定谓语] | 并非所有…都… |
| 11 | For one thing...; For another... | 一方面…另一方面… |
| 12 | [S] was/were [V-ing]...when [突发分句] | 正在…这时突然… |

## 1. one of the + 最高级 + [复数N]

**语义：位居最…之列。** 评价性定位框架，通读命中 17 例、全语料反查 50 例，教材密度第一。

> Did you know that China is one of the oldest countries in the world?（八年级下，教材）

你知道中国是世界上最古老的国家之一吗？

> One of the most famous places in the world for karsts is Guilin.（必修一，教材）

世界最著名的喀斯特地貌区之一就是桂林。

**结构拆解：**

```
one of the + 最高级/限定词 + 复数名词
"之一"由 one of 承担；最高级不因"之一"降级
变体：one of the great mysteries / one of those people who…
```

**常见误读：** 中文习惯说"最著名的之一"会写成 one of the most famous place（漏复数）。反查变体 those people who… 中 one of those 后从句谓语用复数。

## 2. What [小句] is/was [焦点]

**语义：之所以…，关键在于…。** 假拟分裂句——把长句的主语/表语压缩进 what 从句，再聚焦到尾部。通读命中 8 例、全语料 49 例。

> What John Snow showed to the world was how cholera could be overcome.（选择性必修二，教材）

约翰·斯诺向世界证明的是：霍乱是可以被战胜的。

> What surprised Xie Lei was that she found herself speaking up in class after just a few weeks.（选择性必修二，教材）

让谢蕾吃惊的是，短短几周后她发现自己竟在课堂上主动发言了。

**结构拆解：**

```
What + [完整小句] + is/was + 焦点（名词短语/that 从句/how 从句/to do）
what = the thing(s) that…（先行词内置）
时态：从句与主句可错位——What surprised her was…（过去事，现在总结）
```

**常见误读：** what 从句是主语从句整体作主语，谓语动词用单数（What…**is**）。把 what 读成疑问词"什么"会读岔——这里没有疑问义。

## 3. Could you (please) tell me [wh-陈述语序]

**语义：请问…。** 礼貌求助框架，通读命中 8 例、全语料 20 例，初中九年级集中教学。

> Could you possibly tell me the way to the village school?（九年级，教材）

您能告诉我去乡村学校的路吗？

> Could you tell me where I can get something to eat?（九年级，教材）

能告诉我在哪儿能弄点吃的吗？

**结构拆解：**

```
Could you (please/possibly) tell me + wh- 从句【陈述语序】
where I can get…（✓）不是 where can I get…（✗）
礼貌梯度：Can you < Could you < Could you possibly
```

**常见误读：** 从句语序不倒装是唯一考点——间接问句用陈述语序。与直接问句 Where can I get…? 对照记。

## 4. [V] + 疑问词 + to do

**语义：搞清楚怎么做/怎么办。** 疑问词+不定式作宾语，通读命中 7 例、全语料 96 例。

> However, it is important to learn how to use the right language in different situations.（九年级，教材）

然而，学会在不同场合使用得体的语言很重要。

> The first-aid instructor should explain what to do, while the victim and the rescuer should act out the situation.（选择性必修二，教材）

急救讲师应讲解该做什么，"伤员"和"施救者"则把情境演出来。

**结构拆解：**

```
V + (how/what/where/when/whether) + to V
= 宾语从句的压缩：learn how you should use…
know/show/teach/learn/decide/wonder/explain 高频搭配
```

**常见误读：** why 没有 why to do 形态（须写从句 why you should…）。whether to 可作宾语，if to 不行。

## 5. with + [NP] + [补语]

**语义：带着/伴随…。** with 复合结构——介词 with 拖一个"小句"的缩略（名词+补语），通读命中 8 例、全语料反查数十例。

> Guangxi is full of karsts, with different parks for almost everything: food, culture, science…（选择性必修一，教材）

广西遍布喀斯特地貌，有各式主题公园：美食、文化、科学……

> The USA has the largest capacity, with over 80% generated in California.（选择性必修三，教材）

美国装机容量最大，其中八成以上在加州发电。

**结构拆解：**

```
with + NP + 补语（doing / done / adj / 介词短语）
补语形态取决于 NP 与动词的关系：
  主动进行 → V-ing（with businesses taking advantage…）
  被动完成 → V-ed（with over 80% generated in…）
```

**常见误读：** with 复合结构不是"和…一起"——它在句中当伴随状语，删掉不影响主干成立。反例可对照合成章（高中部分）with…taking advantage of the celebrations 一例。

## 6. [S] have/get [O] [V-ed]

**语义：让人把…做了。** 使役被动——主语"安排"动作而非"执行"动作，通读命中 4 例、全语料反查 132 例（含被动形态交叉）。

> They had castles built all around England, and made changes to the legal system.（必修二，教材）

他们在英格兰全境修建城堡，并改革法律体系。

> We'll need ten months at least to have the restaurant decorated.（选择性必修二，教材）

装修这家餐厅至少需要十个月。

**结构拆解：**

```
have/get + O + V-ed（宾语与动词是被动关系）
对比三兄弟：
  have O V-ed：安排别人做（had castles built）
  have O V：让某人做（have him call me）
  have just V-ed：完成体（have just finished）
```

**常见误读：** had castles built ≠ "建造了城堡"（自己动手），是"叫人建了"。判断口诀：have 后的宾语若是动作承受者，V-ed 是使役被动。

## 7. [前句], which [谓语]

**语义：这意味着…/其中…。** which 回指**整句**（不是某个名词）的续评框架，通读命中 3 例、全语料反查 125 例。

> People from the UK are called "British", which means the UK is also often referred to as Britain or Great Britain.（必修二，教材）

英国人被称为"British"，这意味着英国也常被叫作不列颠或大不列颠。

> The famous designer released her new line on Wednesday, which will no doubt start a new fashion trend this year.（选择性必修四，教材）

这位著名设计师周三发布了新系列，今年无疑将掀起时尚新风潮。

**结构拆解：**

```
[完整句], + which + 谓语（which = 前面整句/整件事）
高频谓语：means / suggests / makes it possible / is why
判别法：若 which 能换成 and this，就是回指整句
```

**常见误读：** 读长句时把 which 挂到最近的名词上（如 Britain）会整句读崩——先测"which=这件事"能否成立。

## 8. [主句], V-ing [结果/评注]

**语义：从而/结果…。** 句尾现在分词作结果或评注状语，与句首分词状语（合成章高中部分）互补，通读命中 3 例、全语料反查 125 例。

> Guangxi is full of karsts, giving it some of the most interesting—and beautiful—scenery in the world.（选择性必修二，教材）

广西遍布喀斯特地貌，由此拥有了世界上最有趣也最美丽的风景之一。

> All around the world, the Red Cross continues to help civilians caught in war, providing medical assistance…（选择性必修二，教材）

世界各地，红十字会持续帮助战乱中的平民，提供医疗援助……

**结构拆解：**

```
主句 + , + V-ing（逻辑主语=主句主语或整句）
结果义（giving/making/leaving…）最常见
= which gives…（框架 7 的分词版）
```

**常见误读：** 句尾 V-ing 不是进行体——主句谓语在前面，分词是追加的伴随结果。误当新句子开头会断错句。

## 9. Some [A], (and) others [B]

**语义：有的…有的…。** 对举框架，通读命中 3 例。

> Some people, for example, needed far fewer than 10,000 hours, and others many more.（选择性必修四，教材）

比如，有些人远不需要一万小时，另一些人则要多得多。

> Not everyone knows what they want to be.（八年级上，教材）——见框架 10。

**结构拆解：**

```
Some + NP, (and) others + 谓语/补语
others 后可承前省略谓语（and others many more = and others needed many more）
变体：Some…; others…; still others…（三分对举）
```

**常见误读：** others 后的省略结构——and others many more 里没有动词，动词从前句"借"。单数 another 与复数 others 别混。

## 10. Not all/every [A] + [肯定谓语]

**语义：并非所有…都…。** 部分否定框架，通读命中 2 例。

> While not all farm-to-table restaurants are part of the slow food movement, all slow food restaurants are farm-to-table.（选择性必修二，教材）

虽然并非所有农场直供餐厅都属于慢食运动，但所有慢食餐厅都是农场直供的。

> Not everyone knows what they want to be.（八年级上，教材）

并非人人都知道自己想成为什么。

**结构拆解：**

```
Not all + 复数NP / Not every + 单数N / Not everyone
= All…are not…（英式旧用法，阅读会遇到）
对比全否定：None of… / No…
```

**常见误读：** not all 是"部分否定"——不是"全都不"。All is not lost 是"并非全盘皆输"，不是"一切都完了"。

## 11. For one thing...; For another...

**语义：一方面…另一方面…。** 列举理由的成对标记，通读命中 2 例。

> For one thing, cloning an extinct animal would be difficult. For another, it could be used to grow human organs or tissue in animals.（选择性必修一，教材改编，两例合并展示）

一方面，克隆灭绝动物很难；另一方面，（该技术）可用于在动物体内培育人体器官或组织。

**结构拆解：**

```
For one thing, [理由A]; For another, [理由B]
口语/议论文列举两条理由的固定开场
与 on one hand…on the other 的区别：后者强调对立面，本框架只并列列举
```

**常见误读：** For another 后不接"hand"（× For another hand）。两条理由须并列同向（都支持/都反对），不像 on the other hand 可转折。

## 12. [S] was/were [V-ing]...when [突发分句]

**语义：正在…这时突然…。** 进行体+when 的叙事框架，when 不当时间从句读，通读命中 2 例、全语料反查 16 例。

> Peter was walking over to help the boy, when he heard a man shouting "Stop!"（选择性必修二，教材）

彼得正走过去帮那男孩，忽然听到有人大喊"站住！"

> "I was having breakfast with my three children when water started filling my home."（必修一，教材）

"我正和三个孩子吃早饭，这时水开始灌进家里。"

**结构拆解：**

```
was/were V-ing + when + 一般过去时（突发）
when = at that moment（这时），从句是"打断者"
时体对照：背景用进行体，打断事件用简单过去
```

**常见误读：** when 从句在前时无此效果（When I was having breakfast, … 只是时间）。框架的关键是**顺序**：进行体在前、when 在后。中文对应"正…忽然…"，是叙事文本的高频骨架。

## 新语境练习

用本章框架改写或翻译（先自己写，再展开参考答案对照）：

1. 这个系统是世界上最大的之一。（one of）
2. 让我吃惊的是，整个流程只花了十分钟。（What…is）
3. 我们上周请人把办公室刷了墙。（have…done）
4. 我正在改 bug，这时测试环境突然挂了。（was doing…when）

## 参考答案

1. This system is one of the largest in the world.（自造；one of + 复数）
2. What surprised me was that the whole process took only ten minutes.（自造；what 从句作主语，谓语单数）
3. We had the office walls painted last week.（自造；宾语是承受者→V-ed 使役被动）
4. I was fixing a bug when the test environment suddenly went down.（自造；进行体在前+when 打断）
