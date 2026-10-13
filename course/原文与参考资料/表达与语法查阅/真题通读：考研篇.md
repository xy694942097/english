# 真题通读：考研篇

本章解决：考研真题（2016-2020 真题 + 2005-2025 精翻正文）里的句式骨架——议论文语域最密的论证骨架、评注插入和书面倒装。来源：2026-09-17 对 2,089 信息句（真题 8 份 + 精翻 22 份英文正文）LLM 逐句通读，级联去重（中学/四级/六级已提取的不重复收）后筛出 21 个；另 3 条短语级降级条目按短语档收录（2026-09-21 补编：按 frame-miner skill 标准复筛，把 A 类未编 11 条补入本章，其中 Rather than 换主语版与句尾 without 版挂已编家族变体）。同日续裁（用户指令「继续」）：89 条 candidate 全裁决——39 条入章（## 22-60，含 A 类未编的 [A], not [B] 后置否定对比与 It is all very well…but），7 条降短语档，3 条并入已编条目变体注（Now comes word that、he notes 主谓间插入、anything less than 对举），40 条掠过并注理由。例句逐字校验（精翻正文经引用块解析器逐句抽取），中间物存 references/cascade_mining/。

**语料与披露**：精翻语料是英一阅读正文的社区整理版（2005-2025），与真题年份互补；精翻引用块中的高亮与定位标记已剥除，正文措辞未改动。不宣称与官方出版物逐字一致。


## 本章预览

| 编号 | 句式骨架 | 一句话语义 |
|---|---|---|
| 1 | [S V ...], and/or [助动词/情态词]（独用） | …也一样 |
| 2 | [V/be] less [on/about] [A] and more [on/about] [B] | 少在A，多在B |
| 3 | whether that be [A] / be it [A], [B] or [C] | 无论是… |
| 4 | Suppose/Imagine (that) [情景]，[推演] | 假设/想象… |
| 5 | All [S] have/need to do is (to) [V] | 只需要…就… |
| 6 | It is/was [时段] before [S did] | 过了…才… |
| 7 | [A], if not [B]（插入让步） | 即使不是B，也是A |
| 8 | [介词短语] is/was [真正主语（+修饰从句）] | 争论所在是… |
| 9 | [句子], the [argument/idea] goes, [句子] | 论调说… |
| 10 | Nor + [助动词/be] + [S] [V] | …也不… |
| 11 | [S] is where [S V] | ……正是……所在/症结所在 |
| 12 | [主句], [S] says/said, [主句续]（报道插入） | ……，某某说，……（分隔前后成分） |
| 13 | Rather than/Instead of [A], [新主语] [V] | 与其A，B反而……（主语常换） |
| 14 | It is crucial that [S (should) V原形] | 关键/要求类 that 从句用虚拟语气动词原形 |
| 15 | [S/连词], it seems/appears, [谓语/从句] | （插入语：）似乎……（跳过先接主干） |
| 16 | [S] responded (to [X]) by [V-ing] | 以……方式回应 |
| 17 | [X] come(s) as a surprise (to [sb]) | ……（对某人）出人意料 |
| 18 | [S] would not [V] without [NP] | 没有……就不会……（句内双重否定） |
| 19 | [程度] removed from [NP] | 与……相隔（某种程度） |
| 20 | To [V] is/means to [V] | 做……就是/意味着做…… |
| 21 | As so often (is the case), [主句] | 正如惯常的情形（照例如此） |
| 22 | There is no reason why [S] cannot [V] | 没有理由不让…＝完全可以 |
| 23 | [S V], never to [V] | …了，从此再未… |
| 24 | In this as in much else, [S V] | 此事一如其他许多事…… |
| 25 | Any [评价N] of [A] must start by [V-ing] that [B] | 任何对A的评判都得先承认B |
| 26 | It is not enough to say that [S V] | 仅说…并不够 |
| 27 | [S] was, and still is, [C] | 过去是且现在仍是… |
| 28 | There is as much [A] as there is [B] | 对A的…丝毫不亚于对B的… |
| 29 | Whichever [N], [主句] | 无论选哪个，反正… |
| 30 | Never mind [A], [祈使句] | 别管A了，（先）B吧 |
| 31 | [A] is succeeding where [B] is failing | A 恰在 B 失败之处成功 |
| 32 | [S] be born [V-ing] | 并非天生就会… |
| 33 | Hence the [N] of [X] as [Y] / hence [NP]（无动词句） | 由此得名／这就是…的由来 |
| 34 | have a long way to go before [S V] | 距…还差得远 |
| 35 | The mere [N] (of X) was enough to [V] | 仅凭…就足以… |
| 36 | such as when [S V] | 比如／譬如当…时 |
| 37 | It's not as if [S V] | 又不是… |
| 38 | It is a [adj] [N] that [V]（反语让步） | 再…的N也未必V |
| 39 | [主句], if only as [NP] | …，哪怕只是作为… |
| 40 | [N] being what it is, [主句] | 鉴于N本来就是这副样子… |
| 41 | [说法] has it that [S V] | 俗话说／据称… |
| 42 | nothing more than [X] | 只不过是… |
| 43 | to hear [sb] tell it, [主句] | 照某人的说法… |
| 44 | is it any wonder (that) [S V]? | 难怪… |
| 45 | nothing gets [sb] [V-ing] like [NP] | 没有什么比…更能让某人… |
| 46 | can't afford not to [V] | 不能不… |
| 47 | wonder if [S] aren't [V-ing]（揣度否定） | 琢磨…是不是正在… |
| 48 | on the grounds that [S V] | 以…为理由 |
| 49 | have no option/choice but to [V] | 别无选择只能… |
| 50 | [NP] aside, [主句] | 撇开…不谈，… |
| 51 | There is a strong case that [S should V] | 有充分理由主张… |
| 52 | And if [S were [X]]? | 那要是…呢？ |
| 53 | [前句], which in turn [V] | 这反过来又… |
| 54 | There's no [N] like [N] | 没有什么比得上… |
| 55 | the same may be true of [X] | …可能同样如此 |
| 56 | I'd be lying if I said [S V] | 我要说…就是撒谎 |
| 57 | It's enough to make [sb] [V] | 足以让人… |
| 58 | It comes at a time when [S V] | 这恰好发生在…之际 |
| 59 | [A], not [B]（后置否定对比） | 是A，而不是B |
| 60 | It is all very well [S V-ing], but [主句] | ……固然不错，但是…… |

## 1. [S V ...], and/or [助动词/情态词]（独用）

**语义：…也一样。** 助动词/情态词独自承接前句——谓语省略、情态保留。

> Wasted time is a drag on Americans' economic and private lives, not to mention infuriating. And it should [be].（真题·英一 2017 改述：And it should: …）

（浪费时间拖累美国人的经济与私人生活，更别提多让人生气了。——确实如此。）

> But many middle-class occupations—trucking, financial advice, software engineering—have aroused their interest, or soon will.（真题·英一 2018）

（但许多中产职业——货运、理财咨询、软件工程——已经引起了它们的兴趣，或很快就会。）

**结构拆解：**

```
S V …, and/or + 助动词/情态词（句尾独用，谓语省略）
承接 = 前句谓语的拷贝：will [arouse] / should [be]
否定承接用 nor（见句式骨架 10）
```

**常见误读：** 句尾孤零零一个 will/should 不是残句——它「拷贝」了前句谓语。读到助动词独用时回前句找它承接的动作。

## 2. [V/be] less [on/about] [A] and more [on/about] [B]

**语义：少在A，多在B。** less…and more… 挂资源/注意力再分配——议论文建议句的标配。

> Curriculums—from grammar school to college—should evolve to focus less on memorizing facts and more on creativity and communication skills.（真题·英一 2018）

（从小学到大学的课程应该演进：少关注记忆事实，多关注创造力与沟通技能。）

> College officials tend to emphasize that the goal of grade forgiveness is less about the grade itself and more about encouraging students to retake courses.（真题·英一 2019）

（校方倾向强调：「成绩宽恕」的目的与其说是分数本身，不如说是鼓励学生重修课程。）

**结构拆解：**

```
focus less on A and more on B：less/more 对偶挂介词
be less about A and more about B：about 版
同族句式骨架：四级篇 be more A than B（取舍定性）；本条是「再分配」义
```

**常见误读：** less…more… 不是「少而且多」——是「从 A 移向 B」的转移。两句均出自真题主旨句位置，考题直接考这个转移方向。

## 3. whether that be [A] / be it [A], [B] or [C]

**语义：无论是…。** 虚拟让步——be 原形表「不管是什么情况」。

> There's always a constant fear of falling behind everyone else on the socially perpetuated "race to the finish line," whether that be through academics, sports, or college applications.（真题·英二 2017）

（总有一种在代代相传的「冲线竞赛」中落后的恐惧——无论是学业、体育还是大学申请。）

> There are a number of approaches to mastering the art of deep work—be it lengthy retreats dedicated to a specific task; deep work rituals; or training one's mind.（真题·英二 2018）

（掌握深度工作有不少路径——无论是专注一事的长期闭关、深度工作仪式，还是心智训练。）

**结构拆解：**

```
whether that be A, B, or C：whether + that（回指前述内容）+ be 虚拟原形
be it A or B：省 whether 的版（更书面）
= no matter whether it is（陈述版）
```

**常见误读：** be 是虚拟原形不是错误——「无论它是什么」。that 回指前文的恐惧/路径，别读成「那个存在」。

## 4. Suppose/Imagine (that) [情景]，[推演]

**语义：假设/想象…。** 思想实验的开场——先立场景，后推演。

> Imagine that you favor increasing the minimum wage in our state, and I do not.（真题·英一 2019）

（设想你支持提高本州最低工资，而我不支持。）

> Suppose you are in a room with someone you don't know and something within you says "I want to talk with this person."（真题·英二 2018）

（设想你和一个陌生人同处一室，内心有个声音说「我想和这个人聊聊」。）

**结构拆解：**

```
Suppose/Imagine + (that) + 场景句, + 推演句（and 链或独立句）
常接祈使句+and（已编四级篇句式骨架 4 的分析版变奏）
```

**常见误读：** suppose 祈使用法「设想」不是「假定成立」——下文必有推演，当前句只是脚手架。

## 5. All [S] have/need to do is (to) [V]

**语义：只需要…就…。** 强调极简条件——All 提前，is 后挂原形。

> All he needs to do is shell out $30 for a paternity testing kit at his local drugstore.（真题·英一精翻 2009）

（他所需要的只是在当地药店花 30 美元买个亲子鉴定试剂盒。）

> All I have to do is to go to my CD shelf, or boot up my computer and download still more recorded music.（真题·英一精翻 2011）

（我要做的就是走到 CD 架前，或打开电脑再下载些录制好的音乐。）

**结构拆解：**

```
All + S + have to do / need to do + is + (to) V
to 可省：is (to) V——两种形态都对
= The only thing S must do is V
```

**常见误读：** is 后接原形不是省略错误——All…is 结构允许 to 不定式的裸形。读慢点在「is 后怎么直接是动词」——这是预设考点。

## 6. It is/was [时段] before [S did]

**语义：过了…才…。** 时间流逝句——before 挂「之后才发生」的事。

> It was a year before she became head of a tiny Internet-based commodities exchange.（真题·英一精翻 2011）

（过了一年她才当上一家小型互联网商品交易公司的负责人。）

**结构拆解：**

```
It + is/was + 时段 + before + S 过去式
It 是时间引导词，时段是「等待长度」
主句将来版：It will be years before…（还要过好几年才…）
```

**常见误读：** before 不是「在…之前」的介词用法——此处是从句「直到…才」。整句方向：先过了时段，事件才发生。

## 7. [A], if not [B]（插入让步）

**语义：即使不是B，也是A。** if not 插入——抬升而非否定。

> We have an excellent chance of surviving for a long time, if not forever.（真题·英一精翻 2013）

（我们的物种有极好的机会长期存续——即使不是永远。）

> When it comes to born-digital information, the terrifying answer can be: if not librarians and archivists, then no one.（真题·英一精翻 2025）

（说到原生数字信息，可怕的答案可能是：不是图书管理员和档案员，就没人管。）

**结构拆解：**

```
A, if not B, ：B 是 A 的升级版（万亿→更多/长期→永远）
位置：名词/形容词后插入
第二例是句首疑问缩略：if not A, then no one（不是A就没人）
```

**常见误读：** if not 不是条件「如果不」——是「即便不说成 B，至少也是 A」。方向永远向上抬。

## 8. [介词短语] is/was [真正主语（+修饰从句）]

**语义：争论所在是…。** 表语前置倒装——介词短语提前，主语后置且常拖长从句。

> At issue is the TMT's planned location on Mauna Kea, a dormant volcano worshiped by some Hawaiians as the piko.（真题·英一精翻 2017）

（争议所在是 TMT 拟建在莫纳克亚山——一座被部分夏威夷人奉为「肚脐」的休眠火山。）

> Among the annoying challenges facing the middle class is one that will probably go unmentioned in the next presidential campaign.（真题·英一精翻 2018）

（中产面临的种种恼人挑战中，有一项在下届总统竞选中大概不会被提及。）

**结构拆解：**

```
介词短语（At issue / Among N / In N）+ is/was + 主语（常带同位语/从句）
正常语序：主语 + is + 介词短语
倒装动机：主语长，后置安放
家族：六级篇句式骨架 13（Also due…is）同族异构
```

**常见误读：** is 前的介词短语不是主语——主语在后面。At issue is X = X is at issue（X 是争点）。考研阅读定位题常考倒置后的主语。

## 9. [句子], the [argument/idea] goes, [句子]

**语义：论调说…。** 引述他人论调的插入件——「有人说」的名词版。

> Why, the argument goes, should a car-driving pensioner from Lincolnshire have to subsidise the daily commute of a stockbroker?（真题·英一精翻 2021）

（论调是：为什么林肯郡开车领养老金的人要补贴股票经纪人每日通勤？）

**结构拆解：**

```
X, the argument/idea goes, Y：插入「论调是」
= so the argument runs / as the saying goes
后常接作者要反驳的靶子（立靶件）
```

**常见误读：** goes 不是「去」——「论调的内容如下」。见到 the argument goes，预备读到作者将要反驳的观点。

## 10. Nor + [助动词/be] + [S] [V]

**语义：…也不…。** Nor 句首倒装承接否定——延续+倒装一步到位。

> Nor should their work be considered only as an object of study.（真题·英一精翻 2022）

（他们的作品也不应只被当作研究对象。）

> Nor are highly paid managers themselves immune from the harm caused by the ERA's unjustified dismissal procedures.（真题·英一精翻 2022）

（高薪经理人自己也未能免于 ERA 不公正解雇程序造成的伤害。）

**结构拆解：**

```
Nor + 助动词/be + S + V：部分倒装
承接：前句必须否定（或本条自足否定）
= and…not… either 的强调版
```

**常见误读：** Nor 句首必倒装（Nor should…/Nor are…）——不倒装的 Nor + 主语形态（Nor their work…）是错的。与已编 07 章 neither…nor 的分工：那条是句内并列，这条是句间承接。


## 11. [S] is where [S V]
**语义：……正是……所在/症结所在**

> It's that gap in between, and that's where the problem is.（真题·英2 2017）

> Trust me, eye contact is where all the magic happens.（真题·英2 2018）

**结构拆解：**

```
where 从句作表语，表定位不表地点：is where the problem is / is where all the magic happens
产出侧：中文『症结所在』只会写 is the key problem，母语者 is where…
变体：This is where / Here's where（语篇指示词打头）
```

**常见误读：** where 读成地点义（『问题在哪里』找方位）；此处是抽象定位——把抽象概念钉在某处的高频评论动作。

## 12. [主句], [S] says/said, [主句续]（报道插入）
**语义：……，某某说，……（分隔前后成分）**

> The losers, said retail analyst Neil Saunders, are online-only retailers, especially smaller ones.（真题·英1 2019）

> While climate is a key element, Moritz says, it shouldn’t come at the expense of the rest of the equation. “ The human systems and the landscapes we live on are linked, and the interactions go both ways,” he says.（真题·英2 2017）

**结构拆解：**

```
报道动词短语插在主谓之间或从句与主句之间
The losers, said [同位语], are…——主语与系动词被隔开
已编家族：引语后置报道——本条是其主谓间插入版（考研更爱用）
```

**常见误读：** said Neil Saunders 插在 The losers 与 are 之间——先跳过插入语把 losers…are 接上；同位语堆在插入语里时句主干最容易被冲散。

变体（09-21 补）：主谓间短插入版——The average time for holding a stock…, he notes, has…（真题·英一 2019）；消息传来版 Now comes word that…（真题·英一 2018，与 13章##28/14章##13 家族注呼应）。

## 13. Rather than/Instead of [A], [新主语] [V]
**语义：与其A，B反而……（主语常换）**

> Rather than pulling students back, a gap year pushes them ahead by preparing them for independence, new responsibilities and environmental changes—all things that first-year students often struggle with the most.（真题·英2 2017）

> Instead of wordy, worthy strategies, future governments need to do more to provide the conditions for sport to thrive.（真题·英2 2017）

**结构拆解：**

```
Rather than + V-ing/NP 句首，主句换主语给相反面
Rather than pulling students back, a gap year pushes them ahead——两主语（students / a gap year）不同
已编家族：rather than + V-ing + 祈使句（与其A不如B）——本条是换主语对比版，功能是『反向重估』
```

**常见误读：** 以为 rather than 后的动作与主句主语共享（对齐失误）；这条的要点恰是主语切换——A 被否，B 用新主语翻盘，是考研议论文高频论证动作。

## 14. It is crucial that [S (should) V原形]
**语义：关键/要求类 that 从句用虚拟语气动词原形**

> If we are ever going to protect the atmosphere, it is crucial that those new plants be environmentally sound.（真题·英一精翻 2005）

> Publishers have responded to the demand that they make their product free to readers by charging their writers fees to cover the costs of preparing an article.（真题·英1 2020）

**结构拆解：**

```
It is crucial/essential/vital + that + 主语 + 动词原形（should 可省）
名词版同构：the demand that they make their product free（that 从句里 make 原形）
触发词族：crucial / essential / vital / important / the demand / the requirement
```

**常见误读：** 单数主语后接 be/do 原形（plants be / they make）被当成语法错误改掉——是虚拟语气残留，正式书面语常态；改卷与读文都别误判。

## 15. [S/连词], it seems/appears, [谓语/从句]
**语义：（插入语：）似乎……（跳过先接主干）**

> Feelings of righteous indignation, it seems, are not the preserve of people alone.（真题·英一精翻 2005）

> Because our conscious mind is occupied with daily life we don't always think about the emotional significance of the day's events until, it appears, we begin to dream.（真题·英一精翻 2005）

**结构拆解：**

```
it seems / it appears + 双逗号，插在主谓之间或连词与从句之间
插入语是评注不是真主语：先跳过它把 feelings…are 接上
变体：it would seem（更含蓄）、or so it seems（句尾反讽版）
```

**常见误读：** 把 it seems 当主句主语另起炉灶，把真主语（Feelings of righteous indignation）读成宾语；评注插入语的第一动作永远是跨过它接主干。

## 16. [S] responded (to [X]) by [V-ing]
**语义：以……方式回应**

> Some western farmers have responded by moving operations to Mexico.（真题·英2 2019）

> Publishers have responded to the demand that they make their product free to readers by charging their writers fees to cover the costs of preparing an article.（真题·英1 2020）

**结构拆解：**

```
respond(ed) + (to [X]) + by + V-ing：by 短语回挂 responded
中间可隔长从句（to the demand that they make…），by 的宾语可再接长链
产出侧：中文『以……回应』自造句子常写成 respond with（可接受）或 resorted to（变味）
```

**常见误读：** by 短语隔了十几个词后回挂 responded——别把它读成新手段状语挂错主句；respond…by… 是「以某动作应对某事」的标准答句。

## 17. [X] come(s) as a surprise (to [sb])
**语义：……（对某人）出人意料**

> The mystery is that this should come as a surprise to any boss.（真题·英一精翻 2007）

> One of the reasons why the appointment came as such a surprise, however, is that Gilbert is comparatively little known.（真题·英一精翻 2011）

**结构拆解：**

```
come + as + a surprise：come 不是「来」，是「呈现为/结果是」
常带 should（this should come as a surprise 表意外）或 such（came as such a surprise）
同族：come as a relief / come as no surprise（反方向）
```

**常见误读：** come as 读成「作为……而来」字面直译卡住；as a surprise 整体是结果补语——『落地的效果是意外』，评论语体的事件定性动作。

## 18. [S] would not [V] without [NP]
**语义：没有……就不会……（句内双重否定）**

> The southern states would not have signed the Constitution without protections for the “peculiar institution,” including a clause that counted a slave as three fifths of a man for purposes of congressional representation.（真题·英一精翻 2008）

> Thus poor countries might not be able to escape their poverty traps without political changes that may be possible only with broader formal education.（真题·英一精翻 2009）

**结构拆解：**

```
主句否定（would not have signed / might not escape）+ 句尾 without 短语
without 短语是含蓄条件（= if it were not for），否定靠句尾挂回来
已编家族：Without [NP], [主句(would…)]（句首版）——本条是句尾后置版，反转主句极性
```

**常见误读：** without 挂在句尾时读漏否定回挂——主句的 not/might not 与 without 配合才构成「没它就不行」；拆读成两个独立信息会丢掉条件关系。

## 19. [程度] removed from [NP]
**语义：与……相隔（某种程度）**

> We are even farther removed from the unfocused newspaper reviews published in England between the turn of the 20th century and the eve of World War II, at a time when newsprint was dirt-cheap and stylish arts criticism was considered an ornament to the publications in which it appeared.（真题·英一精翻 2010）

> If people in the network just two degrees removed from the initial influential prove resistant, for example, the cascade of change won't propagate very far or affect many people.（真题·英一精翻 2010）

**结构拆解：**

```
removed from = 分词形容词表「相隔/远离」，非「被移除」
程度词前置：even farther removed / just two degrees removed
产出侧：中文『与……相差甚远』只会写 far away from（地点义），母语者 removed from（抽象距离义）
```

**常见误读：** removed 读成被动「被移除」（误以为什么东西被拿走了）；这里是静态形容词——表时间、代际、抽象层面的距离，考研评论文的标配定位动作。

## 20. To [V] is/means to [V]
**语义：做……就是/意味着做……**

> To read such books today is to marvel at the fact that their learned contents were once deemed suitable for publication in general-circulation dailies.（真题·英一精翻 2010）

> To take this approach to the New Englanders normally means to start with the Puritans' theological innovations and their distinctive ideas about the church - important subjects that we may not neglect.（真题·英一精翻 2009）

**结构拆解：**

```
不定式作主语（To read such books today）+ 系动词 + 不定式表语（to marvel at…）
两个 to do 镜像对举：定义动作——A 就是 B
产出侧：下定义自造句常写成 Doing A is B（可）或 A means B（名词化丢动作感），镜像式更有力
```

**常见误读：** 句首 To 读成目的状语（『为了读书……』）——它是不定式主语；两个 to do 对举的下定义句是议论文开题的常规武器。

## 21. As so often (is the case), [主句]
**语义：正如惯常的情形（照例如此）**

> As so often, the past holds the key to the future: we have now identified enough of the long-term patterns shaping the history of the planet, and our species, to make evidence-based forecasts about the situations in which our descendants will find themselves.（真题·英一精翻 2013）

> As so often is the case, stating that principle doesn't ease the challenge of line-drawing.（真题·英一精翻 2015）

**结构拆解：**

```
As so often + 逗号：话语标记整存整取，『照例』
完整版 As so often is the case；短版直接 As so often
功能：把当下事件挂到规律性上——评论文从个案推向常态的桥
```

**常见误读：** 按 as 从句硬拆语法（so often 是什么成分？）——它是固化话语标记，不当从句分析；整存整取，读到即知作者要借惯例抬升论点。


## 22. There is no reason why [S] cannot [V]

**语义：没有理由不让…＝完全可以。** 双重否定开出许可证——no reason 与 cannot 两个否定抵消成强肯定，比直接说 can 更郑重更有力，是论证放行的常用动作。

> There is no reason why everyone cannot be welcomed on Mauna Kea to embrace their cultural heritage and to study the stars.（真题·英一 2017）

（没有理由不让所有人都被欢迎登上莫纳克亚山，去拥抱他们的文化遗产、去研究星空。）

**结构拆解：**

```
There is no reason why + S + cannot [V]
两个否定相消：no reason（没理由）+ cannot（不能）→ 完全可以
产出侧：许可句自造只会 Everyone can be welcomed——双否定版语气更重
```

**常见误读：** cannot 挂在 why 从句里被读成整体否定（『没理由可以欢迎』）——方向读反；两处否定要一起数。

## 23. [S V], never to [V]

**语义：…了，从此再未…。** 结果不定式收尾——never to return / never to be seen again，一句话写完余生；传记与叙事的收束动作。

> Yet two years before Dickens's birth, his mother's father was caught stealing and fled to Europe, never to return.（真题·英一 2017）

（然而在狄更斯出生前两年，他的外祖父因行窃被抓，逃往欧洲，再未返回。）

**结构拆解：**

```
主句（完整事件）+ 逗号 + never to + [V]
不定式作结果状语：never to = 结果是『再也不』
不可逆色彩：常配 fled / died / vanished 等收场动词
```

**常见误读：** never to return 读成目的状语（『为了不再回来』）——是结果（『结果再没回来』）；never 隔在 to 前容易断错。

## 24. In this as in much else, [S V]

**语义：此事一如其他许多事……。** 类比引入——把个案挂到『很多事都这样』的总括上，in A as in B 的介词骨架装类比动作，评论文由小及大的开场。

> In this as in much else, those who wish to influence the future must prepare for it.（真题·英一 2017）

（此事一如其他许多事：想影响未来的人，必须为未来做好准备。）

**结构拆解：**

```
In this as in much else + 逗号 + 主句
in this（这件事）as in much else（一如其他许多事）
as 对称介词短语：两个 in 挂同一个 as，类比标记
```

**常见误读：** as in much else 当插入语跳过——它是论证承重墙：作者正把个案升格为规律。

## 25. Any [评价N] of [A] must start by [V-ing] that [B]

**语义：任何对A的评判都得先承认B。** 先让步后立论的礼数开场——评价前必须先过一道程序，把对方善意设为前提，再开刀；驳论文的标准起手。

> Any fair-minded assessment of the dangers of the deal between Britain's National Health Service (NHS) and DeepMind must start by acknowledging that both sides mean well.（真题·英一 2018）（截自无噪声句（原句前有社区版 OCR 噪声串））

（对英国国民医疗服务体系（NHS）与 DeepMind 之间交易风险的任何公允评判，都必须从承认双方都出于善意开始。）

**结构拆解：**

```
Any + 评价N + of [A] + must start by + V-ing + that [B]
must start by：程序性强制——『得先』
acknowledging that：让步承认——给对手垫底再反击
```

**常见误读：** start by acknowledging 读成作者立场（『作者承认』）——那是设定的程序步骤，作者的真立场在后文。

## 26. It is not enough to say that [S V]

**语义：仅说…并不够。** 让步后转出真正论点——先把浅层解释按下（『光说 X 不够』），再把深层要求端出来；驳『速效药』式论证的转轴。

> It is not enough to say that the algorithms DeepMind develops will benefit patients and save lives.（真题·英一 2018）

（仅说 DeepMind 开发的算法将造福患者、挽救生命，是不够的。）

**结构拆解：**

```
It is not enough to say that + S V
It 外置主语；not enough 给浅层答案判不及格
后文必接真正论点（It must also… / The question is…）
```

**常见误读：** 读成作者否认 that 从句内容（『算法没益处』）——否认的是『光说这句』的论证力度，内容评判随后文。

## 27. [S] was, and still is, [C]

**语义：过去是且现在仍是…。** 双时态并置强调延续——插入 and still is，一个逗号对把时间轴拉通；声明『这不是过时事实』的动作。

> Before applying for university I told everyone that I would study journalism, because writing was, and still is, one of my favourite activities.（真题·英一 2017）

（申请大学之前我告诉所有人我要学新闻，因为写作过去是、现在仍是我最喜爱的活动之一。）

**结构拆解：**

```
S + was, and still is, + C
两个时态共用一个表语：was…still is
逗号对括住 and still is：插入式补强
```

**常见误读：** 拆成 was and（？）still is（？）断链——识别逗号对插入的整体；产出侧只会写 is still，双时态版更有说服力。

## 28. There is as much [A] as there is [B]

**语义：对A的…丝毫不亚于对B的…。** 存在句装平行比较——两个 there is 对称架起 as much…as，『A 与 B 一样多/一样真』；报道给两方配平的动作。

> There is as much joy over a puffed-out first-timer being clapped over the line as there is about top talent shining.（真题·英一 2017）

（看到气喘吁吁的新手被鼓掌护送过终点线的喜悦，丝毫不亚于看到顶尖人才闪耀全场。）

**结构拆解：**

```
There is as much [A] + as there is [B]
两个存在句镜像：as much…as 把它们拉平
much 可换具体名词（joy / support / doubt）
```

**常见误读：** as there is 处断句（以为新话题开始）——它是比较的另一翼；两个 there is 是一双。

## 29. Whichever [N], [主句]

**语义：无论选哪个，反正…。** wh-限定词悬空省略——Whichever 后不接完整从句，直接逗号另起主句；把选项悬置、直奔要点的动作。

> Whichever approach, the key is to determine your length of focus time and stick to it.（真题·英一 2018）

（无论选哪种方法，关键都是确定你的专注时段长度并坚持下去。）

**结构拆解：**

```
Whichever + N + 逗号 + 主句
省略版：Whichever approach (you choose)
完读版 whichever approach you take 常被砍到只剩名词
```

**常见误读：** 等 Whichever 后面的谓语等不到（悬空）——识别省略，别在原地打转找从句。

## 30. Never mind [A], [祈使句]

**语义：别管A了，（先）B吧。** 让步切换话题再给指令——Never mind 把前项整个撇下（『且不说…』），祈使句端出真正指令；贬前抬后的动作。

> Never mind the quality, then, count the number.（真题·英一 2019）（截自长句）

（那么，先别管质量了，数数量吧。）

**结构拆解：**

```
Never mind + [A] + 逗号 + 祈使句
Never mind：撇开（让步）——『更别提/先不管』
祈使句：真正的指令或判断
```

**常见误读：** Never mind 读成安慰语（『别在意』）——这里是论证让步：暗示 A 根本不值得 mind。

## 31. [A] is succeeding where [B] is failing

**语义：A 恰在 B 失败之处成功。** where 引对照场域——一个 where 把两方成败钉在同一点上，褒贬对照一步到位；对比论证的骨架。

> Parkrun is succeeding where London's Olympic "legacy" is failing.（真题·英一 2017）

（公园跑正在伦敦奥运「遗产」失灵之处取得成功。）

**结构拆解：**

```
[A] + is succeeding + where + [B] + is failing
where 从句表场域（在…之处），非地点
进行时对举：succeeding ↔ failing 同点对撞
```

**常见误读：** where 从句找地点（『在伦敦成功』）——where 指抽象场域『在 legacy 失灵的同一件事上』。

## 32. [S] be born [V-ing]

**语义：并非天生就会…。** born 后直接挂现在分词补语——aren't born knowing / was born liking，一句话划出天性与习得的分界；常与 rather, they learn 对举。

> Children aren’t born knowing how to say “I’m sorry”; rather, they learn over time that such statements appease parents and friends – and their own consciences.（真题·英一 2019）

（孩子们并非生来就会说「对不起」；而是随着时间推移才学会——这类话能安抚父母朋友，也安抚他们自己的良心。）

**结构拆解：**

```
S + be born + V-ing（knowing / liking / speaking）
born + 分词：出生即带（或不带）的状态
否定版 aren't born knowing 最高频：先天不具备
```

**常见误读：** knowing 当定语回头找先行词——它是 born 的补语；产出侧只会写 don't naturally know，born knowing 版更地道。

## 33. Hence the [N] of [X] as [Y] / hence [NP]（无动词句）

**语义：由此得名／这就是…的由来。** hence 直接接名词短语，全句无谓语——书面语的高密度推论收束；无动词句读熟了是利器。

> Hence the description of America as a "graveyard" for languages.（真题·英一精翻 2006）

（因此有了把美国称作语言「坟场」的说法。）

> The founders deliberately focused their projects around light—hence the "visual studies" in the name.（真题·英一精翻 2022）

（创始人们刻意把项目围绕「光」来做——名称里的「视觉研究」即由此而来。）

**结构拆解：**

```
Hence + NP（无谓语！）
= Hence we have the description of… 的压扁版
句中版：—hence the … in the name（破折号挂尾）
```

**常见误读：** 等谓语等不到（把 hence 当副词等主句）——hence 本身就是收束标记；无动词句是正式书面体。

## 34. have a long way to go before [S V]

**语义：距…还差得远。** 长路隐喻装差距——字面『还有很长的路要走』，实指『离目标还远』；报道现状的标配降温动作。

> Even dairy farms, where robots do a small share of milking, have a long way to go before they’re automated.（真题·英一 2019）

（即使是机器人只承担一小部分挤奶工作的奶牛场，距离实现全自动化也还有很长的路要走。）

**结构拆解：**

```
S + have a long way to go + before + S V
before 从句：到『才算到位』之前的路
字面路 → 抽象差距：隐喻已固化
```

**常见误读：** 按『旅途』字面读——a long way to go 全指程度差距；even dairy farms（连…都）是叠加降温。

## 35. The mere [N] (of X) was enough to [V]

**语义：仅凭…就足以…。** mere 一词压秤——『光是存在就够』，把触发条件降到最低以凸显反应之烈；实验报告与论证的强调动作。

> Indeed, the mere presence of a grape in the other chamber (without an actual monkey to eat it) was enough to induce resentment in a female capuchin.（真题·英一精翻 2005）

（确实，另一格子里光有一颗葡萄（并没有猴子真的吃它），就足以引发一只母卷尾猴的怨愤。）

**结构拆解：**

```
The mere + N + was enough to + [V]
mere：仅仅是——把门槛降到地板
enough to：足以引发（后果）
```

**常见误读：** mere 溜过去没接住（读成 the presence）——mere 是全句秤砣：条件越轻，结论越重。

## 36. such as when [S V]

**语义：比如／譬如当…时。** such as 后接整句——举例不止切到名词，还能切到 when 小句；把抽象评价词（antagonistic）实例化的动作。

> But it can also be antagonistic such as when a political candidate turns toward their competitor during a debate and makes eve contact that signals hostility.（真题·英一 2020）（OCR 噪声：makes eve contact 即 makes eye contact（社区版文本讹误））

（但敌意也可能由此而生——比如辩论中一名候选人转向竞争对手、做出传递敌意的眼神接触时。）

**结构拆解：**

```
抽象评价词 + such as when + S V
such as 后不只接名词短语：整个 when 从句作实例
= for example, when… 的压紧版
```

**常见误读：** 以为 such as 后必是名词短语而断错句；注意本例社区版文本的 OCR 噪声（eve→eye）。

## 37. It's not as if [S V]

**语义：又不是…。** 反驳对方预设——『又不是说…』，as if 从句内容是被否定掉的预设情景；口语书面通吃的顶嘴骨架。

> But it's not as if earlier times didn't know perpetual war, disaster and the massacre of innocents.（真题·英一精翻 2006）

（但又不是说什么早先的时代就不曾见识连绵的战争、灾难与对无辜者的屠戮。）

**结构拆解：**

```
It's not as if + S V
as if 从句：对方预设的情景
not 否掉整个预设；从句内可再含否定（didn't know）——两处否定要数清
```

**常见误读：** not 和 as if 分家读——not 否的是整个 as if 情景；产出侧只会写 But earlier times also knew…，反语版更有力。

## 38. It is a [adj] [N] that [V]（反语让步）

**语义：再…的N也未必V。** 形似强调句实为让步反语——谚语式『再聪明的父亲也未必认得自己的孩子』；It is…that 外壳里装的是『未必』。

> It is a wise father that knows his own child, but today a man can boost his paternal (fatherly) wisdom - or at least confirm that he's the kid's dad.（真题·英一精翻 2009）

（再聪明的父亲也未必认得自己的孩子；但如今，男人可以增强自己做父亲的智慧——或者至少确认自己就是孩子的爸爸。）

**结构拆解：**

```
It is a + adj + N + that + [V]
形似强调句（02章##2），实为让步反语
a（非 the）：泛指任何一例都难逃『未必』；后常接 but 转折
```

**常见误读：** 按强调句读成『正是这位聪明父亲认出了孩子』——方向全反；识别 a + that 的谚语气。

## 39. [主句], if only as [NP]

**语义：…，哪怕只是作为…。** 最低限度让步——if only 非『但愿』，是『哪怕仅仅』；给动机兜底的稳妥动作。

> Later, more established companies raced to add such patents to their files, if only as a defensive move against rivals that might beat them to the punch.（真题·英一精翻 2010）

（后来，更成熟的公司竞相把这类专利收入囊中，哪怕只是作为防守动作，以防对手抢先。）

**结构拆解：**

```
主句 + 逗号 + if only as + NP
if only = 哪怕只是（最低限度）
as：以…身份（作为防御动作）
```

**常见误读：** if only 读成『要是…就好了』（虚拟叹息）——此处是让步限定；专利语境 beat them to the punch = 抢先一步。

## 40. [N] being what it is, [主句]

**语义：鉴于N本来就是这副样子…。** 独立主格 + 固定死词串 what it is——『人性如此，没办法』；带无奈的归因开场：先接受现实，再给对策。

> Human nature being what it is, most people stick with default settings.（真题·英一精翻 2013）

（人性本来如此，大多数人便守着默认设置不放。）

**结构拆解：**

```
N + being what it is + 逗号 + 主句
独立主格：N + being…（无连词）
what it is：固定死词串——『就它那个样子』
```

**常见误读：** being what it is 逐词硬拆（『正在作为它是什么』）——整存整取；产出侧只会写 Because of human nature。

## 41. [说法] has it that [S V]

**语义：俗话说／据称…。** 引谚语的固定阀——saying / legend / rumor has it that，it 形式宾语、that 真宾语；把传闻挂出来再拆穿的动作。

> An old saying has it that half of all advertising budgets are wasted - the trouble is, no one knows which half.（真题·英一精翻 2013）

（有句老话说，一半的广告预算都打了水漂——麻烦在于，没人知道是哪一半。）

**结构拆解：**

```
N（saying/legend/rumor）+ has it that + S V
has it = 说／称（it 为形式宾语）
that 从句：说法内容；后常接 the trouble is…（追扣拆穿）
```

**常见误读：** has it 读成『拥有它』——固定引语阀；产出侧只会写 As an old saying goes（也对），has it that 更书面。

## 42. nothing more than [X]

**语义：只不过是…。** 贬抑限定——nothing more than =『仅此而已』，把对象压到地板；与 nothing less than（01章##4 拔到天花板）方向相反。

> Dare to be different, please don't smoke!" pleads one billboard campaign aimed at reducing smoking among teenagers - teenagers, who desire nothing more than fitting in.（真题·英一精翻 2012）

（「敢与众不同，请别吸烟！」一块面向青少年的广告牌如此恳求——而这些青少年想要的，无非是融入群体。）

**结构拆解：**

```
nothing more than + X（N / V-ing）
nothing more than = merely：『无非』
对举：nothing less than（简直是）——天花板 vs 地板
```

**常见误读：** 读成『没有比…更多的』（比较级疑问）——固定贬抑词组整存整取；desire nothing more than fitting in（最想要的不过是从众）。

## 43. to hear [sb] tell it, [主句]

**语义：照某人的说法…。** 转述 + 暗含不信——to hear X tell it 固定插入，『按 X 的口径』，后文常藏反驳；引述设靶的礼貌版。

> No shock there, considering how much work it is to raise a kid without a partner to lean on; yet to hear Sandra and Britney tell it, raising a kid on their “own” (read: with round-the-clock help) is a piece of cake.（真题·英一精翻 2011）

（这没什么可惊讶的：想想没有伴侣可依靠、独自养孩子有多辛苦；可照桑德拉和布兰妮的说法，「自己」带孩子（读作：24 小时有人帮衬）简直小菜一碟。）

**结构拆解：**

```
to hear + sb + tell it + 逗号 + 主句
tell it：『讲述』的固定说法（it 无实指）
转述框架：接下来是某人的版本；常配 yet / but——转完就驳
```

**常见误读：** tell it 拆成 tell + it（告诉它？）——固定短语；读出转述的距离感才算读懂。

## 44. is it any wonder (that) [S V]?

**语义：难怪…。** 反问表肯定——『有什么可奇怪的？』＝『一点也不怪』；前文铺好成因后用反问收口。

> In a society that so persistently celebrates procreation, is it any wonder that admitting you regret having children is equivalent to admitting you support kitten-killing?（真题·英一精翻 2011）

（在一个如此执着颂扬生育的社会里，承认你后悔生了孩子，竟然等同于承认你支持残杀小猫，这有什么奇怪？）

**结构拆解：**

```
is it any wonder + that + S V + ?
反问＝肯定：难怪如此
any：『哪怕一丝』——加强反问；前文必有成因铺垫
```

**常见误读：** wonder 读成『想知道』（真的在问）——修辞性反问；产出侧只会写 It is not surprising that。

## 45. nothing gets [sb] [V-ing] like [NP]

**语义：没有什么比…更能让某人…。** 隐性最高级 + 使动——get sb doing（使动）配 like（比较），『最能让人…的莫过于』；让步皆收的夸张动作。

> It's no surprise that Jennifer Senior's insightful, provocative magazine cover story, “I love My Children, I Hate My Life,” is arousing much chatter - nothing gets people talking like the suggestion that child rearing is anything less than a completely fulfilling, life-enriching experience.（真题·英一精翻 2011）

（珍妮弗·西尼尔那篇颇具洞察力、又挑动神经的杂志封面文章《我爱我的孩子们，我讨厌我的生活》引发热议，毫不意外——没有什么比「养孩子未必是一件完全令人满足、充实生命的事」这一说法更能让人议论纷纷的了。）

**结构拆解：**

```
nothing gets + sb + V-ing + like + NP
get sb doing：使动（让人谈论起来）
like：比较（比得上）——非『喜欢』；nothing…like = 隐性最高级
```

**常见误读：** like 读成『喜欢』、gets 拆成 get+s——是『没什么比这更能让人…』的夸张最高级；与 13章##5 few 隐性最高级同族。

## 46. can't afford not to [V]

**语义：不能不…。** 双重否定表必须——not to 挂在 afford 后，『承担不起不做的后果』；把『不做』设为奢侈的倒逼动作。

> Vanity is a constant; people will only start shopping more sustainably when they can't afford not to.（真题·英一精翻 2013）

（虚荣是常态：只有当人们『不做』的代价高到承担不起时，他们才会开始更可持续地购物。）

**结构拆解：**

```
can't afford not to + V（句尾省略版）
afford not to：『负担得起不做』
can't：连『不做』都负担不起 → 必须做；not to 后动词可承前省略
```

**常见误读：** not to 漏读一个 not（读成 can't afford to『不能做』）——方向全反；两处否定要一起数。

## 47. wonder if [S] aren't [V-ing]（揣度否定）

**语义：琢磨…是不是正在…。** 否定问句藏倾向——if 从句用否定（aren't），表面疑问实则认同该情景；揣度 + 委婉肯定，读反就丢立场。

> But it's interesting to wonder if the images we see every week of stress-free, happiness-enhancing parenthood aren't in some small, subconscious way contributing to our own dissatisfactions with the actual experience（真题·英一精翻 2011）（截自长句）

（但有意思的是可以琢磨一下：我们每周看到的那些无忧无虑、为幸福加成的育儿画面，是不是正以某种微小而潜意识的方式，加剧了我们对真实育儿体验的不满……）

**结构拆解：**

```
wonder if + S + aren't V-ing
if 从句否定式疑问：『是不是不是…』
实指：恐怕正是在…（揣度+认同倾向）；wonder 自问式框架
```

**常见误读：** aren't 读成期待否认的疑问（『不是在…吧？』）——揣度否定实为委婉肯定：『恐怕正是它们在加剧不满』。

## 48. on the grounds that [S V]

**语义：以…为理由。** 正式归因框架——政府公文与评论的标配，grounds（依据/理由）常复数；把决定挂到理由上的动作。

> Successive governments have permitted such increases on the grounds that the cost of investing in and running the rail network should be borne by those who use it, rather than the general taxpayer.（真题·英一精翻 2021）

（历届政府允许这类涨价，理由是铁路网络投资与运营的成本应由使用者承担，而非全体纳税人。）

**结构拆解：**

```
S V + on the grounds that + S V
grounds：理由（法律/正式语境高频复数）
that 从句：理由内容；比 because 更正式、可挂在名词后
```

**常见误读：** grounds 读成『地面』、on the grounds 读成『在场地上』——正式归因固定件；后文 rather than 挂对立项。

## 49. have no option/choice but to [V]

**语义：别无选择只能…。** but to 接不定式——no option but to do，『除了…没别的选项』；被逼无奈的正式表达。

> It has become a grimly reliable annual ritual: every January the cost of travelling by train rises, imposing a significant extra burden on those who have no option but to use the rail network to get to work or otherwise.（真题·英一精翻 2021）

（这已成了一种铁打不变的年度仪式：每年一月，火车票价上涨，给那些别无选择、只能坐火车上下班的人添上一笔沉重的额外负担。）

**结构拆解：**

```
have no option/choice + but to + [V]
but = except：除…之外（无选项）
but to do：不定式必带 to；those who have no option but to… 报道弱势方标配
```

**常见误读：** but 当转折连词断句（『别无选择，但是为了…』）——but 是介词；不定式的 to 勿漏读。

## 50. [NP] aside, [主句]

**语义：撇开…不谈，…。** 名词 + aside 前置让步——joking aside / Nostalgia aside，把异议先搁置再入正题；比 apart from 更利落的撇开动作。

> Nostalgia for ink on paper and the rustle of pages aside, there's plenty of incentive to ditch print.（真题·英一精翻 2016）

（撇开对纸墨香气与翻页沙沙声的怀旧不谈，弃印转网有充足的理由。）

**结构拆解：**

```
NP + aside + 逗号 + 主句
aside：撇到一边（让步）
NP 常为情感/反对类名词（nostalgia / joking / qualms）
```

**常见误读：** aside 找错挂靠（当后置定语读）——前置让步标记；产出侧只会写 Apart from nostalgia。

## 51. There is a strong case that [S should V]

**语义：有充分理由主张…。** case 论证框架——a strong case that / for，『可以立一个有力的论证』；把主张包装成论证的动作，常配 should。

> However, there is a strong case that those who have been worst affected by industrial action should receive compensation for the disruption they have suffered.（真题·英一精翻 2021）

（然而，有充分的理由主张：受罢工影响最严重的人，应就所受的干扰获得补偿。）

**结构拆解：**

```
There is a strong case + that + S should V
case：论证/理由（make a case for 同族）
strong 可换 good/solid；that 从句：主张内容——社论标配
```

**常见误读：** case 读成『案件/案例』——论证义；there be + case 的存在句式把主张推上前台。

## 52. And if [S were [X]]?

**语义：那要是…呢？。** 悬置条件问句——if 从句虚拟式直接加问号，主句刻意省略；把对方的假设推到荒诞处的反问动作。

> And if Peretti were in charge at the Times?（真题·英一精翻 2016）

（那如果掌管《纽约时报》的是佩雷蒂呢？）

**结构拆解：**

```
And if + S + were X + ?
虚拟式条件句 + 问号 = 主句省略
『那又怎样/结果会不同吗』的反问；And 承接他人观点
```

**常见误读：** 等主句等不到（以为句子残缺）——问号就是收束；虚拟 were 是『假设而已』的标记。

## 53. [前句], which in turn [V]

**语义：这反过来又…。** 非限定从句表连锁反应——which 回指前句整个命题，in turn 标记因果链的下一环；多米诺叙事的连接件。

> But it has already sparked significant controversy, with the United States trade representative opening an investigation into whether the tax discriminates against American companies, which in turn could lead to trade sanctions against France.（真题·英一精翻 2020）

（但这已引发重大争议：美国贸易代表正在调查该税是否歧视美国企业，而这反过来可能导致对法国的贸易制裁。）

**结构拆解：**

```
前句 + 逗号 + which + in turn + [V]
which 回指：前面整个事件（非单个名词）
in turn：作为下一环/反过来——链条感 A→B→C
```

**常见误读：** which 就近找先行名词（investigation?）——它回指整句事件；in turn 读成『轮流的』丢掉链条义。

## 54. There's no [N] like [N]

**语义：没有什么比得上…。** 谚语式夸张——There's no place like home 的骨架槽位化；否定 + 同词重复出顶点意味。

> There’s no business like show business — but in Los Angeles, it feels like there’s no business at all.（真题·英一精翻 2026）

（「没有任何行业能像演艺业这样」——但在洛杉矶，感觉更像是『根本就没有这个行业』。）

**结构拆解：**

```
There's no + N + like + N
同一名词两现：no X like X（顶点）
谚语源：no place like home；本例后半为仿拟（no business at all）
```

**常见误读：** 两现名词相同以为重复冗余——刻意修辞；读出顶点夸张才算接住。

## 55. the same may be true of [X]

**语义：…可能同样如此。** 类比外推标记——前文说完 A，用 the same may be true of B 把结论外推；评论从个案扩面的桥，may 留退路。

> If you’re heading for your nearest branch of Waterstones, the biggest book retailer in the UK, in search of the Duchess of Sussex’s new children’s book The Bench, you might have to be prepared to hunt around a bit; the same may be true of The President’s Daughter, the new thriller by Bill Clinton and James Patterson.（真题·英一精翻 2023）

（如果你正走向最近的沃特斯通书店——英国最大的图书零售商——去找苏塞克斯公爵夫人的新童书《长凳》，可能得做好多找几家的准备；克林顿与帕特森合著的新惊悚小说《总统的女儿》，可能同样如此。）

**结构拆解：**

```
the same + may be true of + X
the same：承接前文结论（= as above）
may：留出不确定（外推更严谨）；be true of：对…成立
```

**常见误读：** the same 无指代对象硬读——必回前文找已成立的命题；true of 的 of 是『对…而言』。

## 56. I'd be lying if I said [S V]

**语义：我要说…就是撒谎。** 虚拟语气表断然否认——if I said（虚拟）+ I'd be lying，『恕我直言，绝非如此』；比 not 否定更有人格温度。

> As a librarian whose day job revolves around special collections and digital assets, I share the night terrors of historians, and I’d be lying if I said a comprehensive preservation solution currently exists.（真题·英一精翻 2025）

（作为一名日常工作围着特藏与数字资产打转的图书馆员，我和历史学家们共享同样的深夜恐慌——要说我以为如今已存在一套全面的保存方案，那是撒谎。）

**结构拆解：**

```
I'd be lying + if I said + S V
虚拟过去式 said：与事实相反（我不会说）
字面『说了就是撒谎』→ 实指：绝非如此；第一人称限用，人格背书
```

**常见误读：** said 读成真实过去（『他曾说过』）——虚拟标记（would be）在场；语气是断然否认。

## 57. It's enough to make [sb] [V]

**语义：足以让人…。** 夸张评注收束——字面『足够让人…』，实为感叹：荒唐到让人放下手机拿起扫帚；评论文的收尾动作。

> It’s enough to make a person put down the smartphone and go out front with a yard broom.（真题·英一精翻 2026）

（这足以让人放下智能手机、拿起院子里的扫帚出门了。）

**结构拆解：**

```
It's enough to make + sb + [V]
enough to：足以——夸张触发
make sb do：使动；It 回指前文荒唐事
```

**常见误读：** 读成真实可能性评估——修辞性夸张；产出侧只会写 This makes people want to…，enough to make 版收束更有力。

## 58. It comes at a time when [S V]

**语义：这恰好发生在…之际。** 背景铺垫骨架——it 回指前文事件，at a time when 挂上时代背景；新闻给事件配语境的标配动作。

> It comes at a time when authors are already worried about the consequences of the proposed merger between PRH and another big publisher, Simon & Schuster（真题·英一精翻 2023）（截自长句）

（此事发生在作者们已经为企鹅兰登书屋与另一出版巨头西蒙-舒斯特拟议合并的后果忧心之际。）

**结构拆解：**

```
It + comes at a time when + S V
It：回指前文事件（勿找近处名词）
at a time when：时机框架（正值…之际）；新闻导语后第二句高频
```

**常见误读：** It 当无义虚主语——必须回指；comes 读成『到来』的字面方向感。

## 59. [A], not [B]（后置否定对比）

**语义：是A，而不是B。** 否定项后置修正——A 先出场，逗号 + not B 再做排除；嵌套长句里 not B 离核心远，最易读丢排除义。

> But the ruling reinforces the need for citizens and their elected representatives, not the courts, to ensure equality of access to government.（真题·英一精翻 2017）

（但这项裁决强化了这样一种必要性：确保政府渠道平等的，应是公民及其民选代表，而非法院。）

> The implication is that Millennials prefer news from the White House to be filtered through other sources, not a president’s social media platform.（真题·英一精翻 2018）

（言外之意是：千禧一代更希望白宫新闻经其他来源过滤而来，而非总统的社交媒体平台。）

**结构拆解：**

```
[A] + 逗号 + not [B]
not 插入修正：排除项后置
嵌套版：the need for [A], not [B], to V——A/B 隔着不定式；与 14章##22 反向同族
```

**常见误读：** not B 离主干远被读丢（the need for citizens…to ensure 中间的 not the courts 溜走）——读到逗号 + not 先找排除对象。

## 60. It is all very well [S V-ing], but [主句]

**语义：……固然不错，但是……。** 先让后驳——It is all very well（说得再好听）+ but（可惜）：给对方让足面子再收走；口语书面通吃的驳论起手，产出侧自己只会写 Although…。

> It is all very well train operators trumpeting the improvements they are making to the network, but passengers should be able to expect a basic level of service for the substantial sums they are now paying to travel.（真题·英一精翻 2021）

（铁路运营商大肆宣扬他们正在对路网进行的改进，这固然不错；但乘客花了如今这么高的票价，理应能期待一项基本水平的服务。）

**结构拆解：**

```
It is all very well + [S V-ing] + 逗号 + but + 主句
It 形式主语；all very well = 好是好的（让步肯定）
but 收走：真正立场在后半句
变体：It's all very well for sb to V… / It's all very well to say…
```

**常见误读：** very well 当程度副词滑过去——all very well 是反讽让步的固定串（「说得倒是好听」）；让步与驳斥的落差是全句火力所在。
## 值得学的短语（考研篇顺手收）

**all too [Adj/Adv]** — 实在太……（常含无奈或贬义）。误读点：all too 不是「全都」，是程度强化 + 负面预设。

> Such behaviour is regarded as "all too human".（真题·英一精翻 2005）

同族：all too often / all too easy / but only too well（反语）。

**the very [N]** — 正是/恰恰是那个 N。误读点：very 此处是形容词「正是」，不是副词「很」。

> they make the very idea of happiness seem unreliable.（真题·英一精翻 2006）

同族：the very thought of / the very fact that。

**It is (all) too easy to [V]** — 很容易就（会）……（暗含批评：这种做法其实站不住）。误读点：不是中性难度陈述，是让步前先贬的修辞。

> It is too easy, and misleading, to see such court rulings as merely standing up for the rights of land owners.（真题·英一精翻 2024）

同族：It is easy to（中性版，无贬义预设）。
**so much the [比较级]** — 那就更…了（反倒更…）。误读点：按 so much 字面读成「如此多」；so much the easier = 反倒更容易了。

> The development of "cloud computing", meanwhile, has made that exploration so much the easier.（真题·英一精翻 2015）

同族：all the more（01章##6 已编正向版）。

**only too [adj] to [V]** — 求之不得，非常乐意。误读点：与 too…to（太…而不能）方向相反，极易读反：only too ready = 巴不得。

> But in Osborneland, your first instinct is to fall into dependency - permanent dependency if you can get it - supported by a state only too ready to indulge your falsehood.（真题·英一精翻 2014）

同族：all too（本短语档已编，同 too 强化族）。

**not nearly as [A] as [B]** — 远远不及。误读点：nearly 修饰否定差值（差得远），不是「几乎一样」。

> AI “vision” today is not nearly as sophisticated as that of humans.（真题·英一精翻 2019）

同族：nowhere near as（同族强化）。

**albeit [短语]** — 尽管／纵然（书面让步缩略）。误读点：虽等于 though，但只接形容词/介词短语，不接从句。

> She is proud that several sculptures have even gone on display again, albeit sometimes beneath protective cases.（真题·英一精翻 2022）

同族：03章 [A] as/though [S V] 让步族。

**to name but a few** — 仅举几例（列举收尾）。误读点：but = only（只），非转折；清单示未尽。

> They have included Britain's DPT. (diverted profits tax), Australia's MAAL (multinational anti-avoidance law), and India's SEP (significant economic presence) test, to name but a few.（真题·英一精翻 2020）

同族：to name a few（口语版）。

**That said,** — 话虽如此（让步话语标记）。误读点：不是「那样说过」的过去陈述，是承接让步再转折的标记。

> That said, there is a way in which grade forgiveness satisfies colleges’ own needs as well.（真题·英一精翻 2019）

同族：04章##2 admittedly / granted / to be sure。

**to the extent (that) [S V]** — 在…的程度上／既然。误读点：that 常省略，to the extent 易被误读为程度名词短语收尾而断错句。

> If not placing jobs at risk, to the extent employment protection laws constrain business owners from dismissing under-performing managers, those laws act as a constraint on firm productivity and therefore on workers' wages.（真题·英一精翻 2022）

同族：insofar as（05章##5 已编）。

## 新语境练习

1. 新工具已经改变了教学，或者很快就会。（助动词独用）
2. 面试要点少看资历，多看解题思路。（less…and more…）
3. 无论是在通勤路上、咖啡馆还是家里，都能办公。（be it…）
4. 你只需要把这份文档发给负责人就完成了。（All … is）
5. 过了三个月构建才稳定下来。（It was…before）
6. 这个改法是重大改进——即使不算革命。（, if not,）

## 参考答案

1. The new tools have changed teaching—or soon will.（自造；will 承接 changed）
2. Interviewing should focus less on credentials and more on problem-solving.（自造；转移方向是考点）
3. Be it on the commute, in a café, or at home, the work can get done.（自造；be it 虚拟原形）
4. All you have to do is send the document to the owner.（自造；is 后裸不定式）
5. It was three months before the build stabilized.（自造；before=直到…才）
6. The rework is a major improvement, if not a revolution.（自造；if not 向上抬升）
