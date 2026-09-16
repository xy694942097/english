# 家族B：强调与聚焦

本章解决：读长句时抓不住"作者到底在强调什么"，写句子时无法突出重点。5 个框架。特殊来源：全部在 2026-09-16 句法诊断中真实撞见（Q2/Q4/Q7/Q10），Notice 一步已完成，本章是 Unpack。例句标注同家族A。

## 本章预览

| 编号 | 框架 | 一句话语义 |
|---|---|---|
| 1 | What … is/was … | 把"…的"推到句子焦点位置 |
| 2 | It was [X] that … | 正是X（不是别的） |
| 3 | Only [状语] did … | 只有到/只有在…才… |
| 4 | That [X], rather than [Y], was [Z] | 是X而非Y（导致了Z） |
| 5 | do/does/did + 动词原形 | 确实…（口语与书信中的强调） |

## 1. What … is/was …

**语义：把"…的"推到句子焦点位置。** 书面语最常用的强调骨架，诊断句 Q2/Q10 都是它。

> What he felt was more akin to pity than love.（语料）

他感受到的更像怜悯，而不是爱。

> What annoyed him most was that he had received no apology.（语料）

最令他生气的是没人向他道歉。

**结构拆解：**

```
What S V  = 主语从句（"…的东西/事情"）
What he felt        → 他感受到的（东西）
was                 → 是
…                   → 焦点：说话人真正想说的
套路：把普通句 He felt pity 装进 What…was…，pity 被推到句尾焦点位
```

**诊断句还原：**

| 原句 | 还原成普通句 |
|---|---|
| What the committee failed to anticipate was how quickly costs would escalate.（Q2） | The committee failed to anticipate something. |
| What began as a debugging exercise ended up revealing a design flaw.（Q10） | Something began as a debugging exercise. |

**变体采集：**

| 变体 | 焦点位置 | 例 |
|---|---|---|
| What S V is/was … | 句尾 | What matters is the interface. |
| What happened was (that) … | 句尾从句 | What happened was that the disk filled up. |
| All (that) S V is … | 句尾 | All you need is one clean backup. |

## 2. It was [X] that …

**语义：正是X（不是别的）。** 分裂句，强调句中某个成分。

> It was only later that the drug was shown to be addictive.（语料）

直到后来才证明该药会成瘾。

> It was the config file, not the code, that caused the outage.（自造）

正是配置文件而非代码导致了宕机。

**结构拆解：**

```
普通句：The config file caused the outage.
分裂：  It was [the config file] that caused the outage.
              强调成分为宾语 ↑
注意：不是所有 It was … that 都是分裂句！
  It was imperative that he act …（语料）→ that 从句是主语从句（it 形式主语）
  判别：去掉 it was…that 还能还原成完整句 → 分裂句；不能 → 形式主语
```

**常见误读：**

| 误读 | 正解 |
|---|---|
| 见到 It was…that 就当"正是" | 先做还原测试，可能只是形式主语 |
| 强调主语时动词跟着改 | It was he who…（强调主语用 who，正式） |

## 3. Only [状语] did …

**语义：只有到/只有在…才…。** only + 状语放句首，触发部分倒装。诊断句 Q4。

> Only when the last children had disappeared did Sister Agatha break her rigid pose.（语料）

直到最后一个孩子走远，阿加莎修女才放开她那僵硬的姿态。

> Only once did we hit on a question which foxed one of the experts.（语料）

我们只碰到过一个把专家也难住了的问题。

**结构拆解：**

```
普通句：The true sequence became apparent only after the logs had been correlated.（Q4）
倒装：  Only after … did the true sequence of events become apparent.
规则：only + 状语（从句/介词短语/副词）位于句首 → 助动词提前（did/can/have…）
陷阱：only 修饰的不是状语时不倒装：Only he did it（= 是他做的，不倒装）
```

**与 not until 的关系：** 同属"否定/限制状语前置→倒装"家族。not until 详见 [05-patterns/02-not-until](../05-patterns/02-not-until.md)。

## 4. That [X], rather than [Y], was [Z]

**语义：是X而非Y（导致了Z）。** 主语从句 + rather than 平行插入，诊断句 Q7 的骨架。

> That the outage was caused by a misconfigured certificate, rather than by the attack initially suspected, was established only after a week of investigation.（自造，Q7 原型）

宕机由配置错误的证书导致，而非最初怀疑的攻击——这一点在调查一周后才确认。

**结构拆解：**

```
That S V = 主语从句（整个句子做主语）
rather than Y = 平行插入，否定 Y、肯定 X
  X: caused by a misconfigured certificate
  Y: by the attack initially suspected（同为 by 短语，平行）
难点：主语太长，谓语 was established 离句首远——
  读法：先跳读谓语动词，再回头装主语
```

**阅读策略：** 遇到 That 开头的长句，先找第一个独立谓语动词（这里 was established），主干即"那件事被确认"，再拆 That 从句内部。

## 5. do/does/did + 动词原形

**语义：确实…（口语与书信中的强调）。** 助动词强调，不倒装、不加否定。

> The test did pass yesterday — I checked twice.（自造）

测试昨天确实通过了——我查了两遍。

> You do have a choice here.（自造）

你在这里确实有选择。

**结构注：** 只强调现在/过去单次的确定语气，不用于进行时。书面正式文里少见，邮件和口语高频。与 really 强调的区别：do 强调的是"事实与预期相反或值得确认"，语气更硬。

## 迁移练习（用你诊断时的原句回炉）

1. 拆 What began as a debugging exercise ended up revealing a design flaw. 的主干，指出焦点。
2. Only after the third retry did the service come back up. 还原成不倒装的普通语序。
3. It was surprising that no one had noticed the drift. 是分裂句吗？为什么？
4. 用 What S failed to anticipate was … 写一句你们系统里真实发生过的事。
5. That the bug was in the parser, rather than in the lexer, was confirmed by the unit tests. 主干是什么？rather than 否定的是哪个？

## 参考答案

1. 主干：What began… ended up revealing…（什么结束了→揭示出缺陷）。焦点是 a design flaw（句尾），句子的强调在"起点是调试练习"与"终点是设计缺陷"的反差上。
2. The service came back up only after the third retry.（倒装消失，only after 回到句中。）
3. 不是。做还原测试：*No one had noticed the drift* 是完整句，但 it 在这里没有实义指代、that 从句是真正主语（= That no one had noticed the drift was surprising 的变体），所以是形式主语句。分裂句版本应是 It was surprising how no one had noticed —— 还原后仍是强调结构。判别口诀：能拆出"被强调成分"的是分裂句，拆不出的是形式主语。
4. 参考：What we failed to anticipate was how fast the event stream would grow. 骨架：What S V was 焦点。
5. 主干：That…was confirmed（那件事被单元测试确认了）。rather than 否定 in the lexer（词法分析器），肯定 in the parser（语法分析器）。
