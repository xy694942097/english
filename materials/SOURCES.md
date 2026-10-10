# 资料来源

本页记录实际使用过的资料网站及操作方法，方便继续搜集英文原文、字幕和口语 chunks。文件下载、来源登记和原件保存的通用规则见 [资料手册](HANDBOOK.md)；已经下载的资料见 [资料清单](README.md)。以下操作于 **2026-10-08** 实际验证，网站界面和下载地址以后可能变化。

## TED：官方英文原文，最终保留 TXT

TED 这轮的选题、实际接口、基本信息格式、断行合并校验、084 源时长差异和后续刷新方法，统一见 [TED 资料收集经验与维护](../references/ted/README.md)。[100 篇选材目录](../references/ted/ted-100-catalog.md) 与 [TXT 文件清单](../references/ted/ted-100-download-report.md) 是当前入口。

用户指定 TED 只需带基本信息的 TXT；不默认另存字幕 JSON、SRT、VTT。具体格式例外已写入 [HANDBOOK](HANDBOOK.md)，后续执行时沿用，不重复决定格式。

## SubtitleCat：找英文字幕，保留时间码回查

网站：[SubtitleCat](https://www.subtitlecat.com/)。它提供用户上传的字幕以及多语言翻译、下载入口。本项目把它作为**英文字幕的检索与下载来源**：用字幕寻找可复用表达，用时间码回到原演出核对语气和上下文。字幕是社区资料，不自动等于官方逐字稿。

### 1. 搜作品，先确认是哪一场

用英文演员名、演出名和年份搜索。可以直接在搜索引擎输入：

```text
site:subtitlecat.com/subs/ "George Carlin" "Again"
site:subtitlecat.com/subs/ "George Carlin" "Doin It Again"
site:subtitlecat.com/subs/ "George Carlin" "Back in Town"
```

点进具体作品页，再核对标题、年份和页面下方的 **Original subtitles**。同一场演出可能有不同发行版、不同时间偏移或重复上传；仅叫 `George Carlin` 的模糊标题先不收。`File Not Found` 页面没有可用原件，应换一个结果。不要把致敬节目、纪录片或含有演员名字的其他影视作品误当成他的脱口秀专场。

### 2. 找 English 行，区分下载与翻译

作品页列出许多语言，每种语言旁可能显示 `Download` 或 `Translate`：

| 页面元素 | 操作与判断 |
|---|---|
| **English → Download** | 获取该页已有的英文 SRT；还要确认下方原字幕本身是英文 |
| **English → Translate** | 当前需要生成英文翻译；本项目优先换一个有英文原字幕的页面 |
| **Original subtitles** | 抽读开头、中间、结尾，检查是否是自然英文、有时间码、内容与作品相符 |
| `.en`、`[eng]`、`-en.srt` | 是语言线索，不足以单独证明它是英文原文或质量良好 |

我们要的是**英文演出的英文字幕**。如果原字幕是其他语言、English 是翻译生成的，不作为原生英语用法的证据。

### 3. 下载 SRT：从页面取链接，不猜地址

点击 English 行的 `Download`，或复制它的链接再下载。**作品页与 SRT 下载地址可能位于不同编号目录**，不能把作品页的 `.html` 后缀机械替换成 `.srt`。

例如，实际验证过的《Doin' It Again》入口是：

- [作品页](https://www.subtitlecat.com/subs/572/George.Carlin.Doin.It.Again.1990.DVDRip.html)
- [英文 SRT 下载链接](https://www.subtitlecat.com/subs/874/George.Carlin.Doin.It.Again.1990.DVDRip-en.srt)

在终端下载单份文件的示例（从 `english/` 项目目录运行）：

```bash
mkdir -p materials/corpus/standup-subtitles/george-carlin
curl -fL --retry 2 --max-time 60 \
  'https://www.subtitlecat.com/subs/874/George.Carlin.Doin.It.Again.1990.DVDRip-en.srt' \
  -o materials/corpus/standup-subtitles/george-carlin/doin-it-again-1990.en.srt
```

地址失效时回作品页重新取得 English 下载链接。搜索页能打开、网页工具能读正文，不保证下载链接也能由同一个工具抓取；本次网页工具返回 `Cache miss`，但终端 `curl` 成功取得了 SRT。连接超时可少量重试，仍失败就换上传版本，不把网页错误页保存成字幕原件。

### 4. 下载后检查，再登记

1. **检查实际文件**：应有编号、`00:00:00,000 --> 00:00:00,000` 时间码和英文正文；不能是 HTML、验证码或错误信息。
2. **检查可读性与覆盖**：抽读开头、中间、结尾；检查乱码、缺大段内容、异常重复、字幕编号及时间码顺序。结尾时间码只表示该文件覆盖到哪里，不自动证明与视频完整同步。
3. **检查是否重复**：同一作品只保留一个合适的版本；文件哈希一致表示原件完全相同，文本相似还可能是不同时间轴版本。
4. **记录出处**：按 [HANDBOOK](HANDBOOK.md) 写入 `downloads-manifest.json`，保存本地路径、作品名、来源页、下载直链、字节数、SHA-256、下载日期和许可说明。

原始 SRT 保存到 `materials/corpus/standup-subtitles/<演员>/`，保持下载字节不变。需要合并断行、整理句子或生成阅读稿时另做派生文件，保留原时间码映射；不要直接改写原件。未见明确许可的资料仅作本地个人学习，不再分发。

### 5. 从字幕进入 chunks 收集和编课

先通读一段相邻字幕，恢复完整语境，再选搭配、短语动词、话语套语或句式骨架。一次字幕换行不是一句话的边界；一句舞台笑话也不一定是可复用词块。

- **候选采集**：保存表达、暂定中文意思、例句及“作品名＋时间码＋本地文件／来源链接”，按 [Chunks 收集箱格式](../references/chunks/FORMAT.md) 录入。去重只比较收集箱内已有条目。
- **正式编课**：核对原演出、词义、固定部分和开放位置，判断离开笑话是否仍自然可用；教学自造例句明确标注，不能冒充演出原话。把夸张、讽刺和角色台词的语气另行解释。

### 本项目已下载的 George Carlin 字幕

以下 4 份已经入库；后续可以直接使用本地文件，不必重复下载。

| 作品 | 来源页 | 相对 `materials/` 的本地路径 |
|---|---|---|
| Again! (1978) | [SubtitleCat](https://www.subtitlecat.com/subs/1577/George%20Carlin%20-%2002%20-%20Again%20%5B1978%5D.html) | `corpus/standup-subtitles/george-carlin/again-1978.en.srt` |
| Doin' It Again (1990) | [SubtitleCat](https://www.subtitlecat.com/subs/572/George.Carlin.Doin.It.Again.1990.DVDRip.html) | `corpus/standup-subtitles/george-carlin/doin-it-again-1990.en.srt` |
| Back in Town (1996) | [SubtitleCat](https://www.subtitlecat.com/subs/1184/%281996%29%20George%20Carlin%20-%20Back%20in%20Town.html) | `corpus/standup-subtitles/george-carlin/back-in-town-1996.en.srt` |
| It's Bad for Ya (2008) | [SubtitleCat](https://www.subtitlecat.com/subs/1215/George%20Carlin...%20It%20s%20Bad%20for%20Ya%20%20%282008%29.DVDRip.iNTiMiD.en.html) | `corpus/standup-subtitles/george-carlin/its-bad-for-ya-2008.en.srt` |

来源直链、文件哈希和下载日期的唯一登记处是 [downloads-manifest.json](downloads-manifest.json)。相关课程见 [脱口秀口语 Chunks](../book/11-spoken-chunks/01-standup-conversation-moves.md)。
