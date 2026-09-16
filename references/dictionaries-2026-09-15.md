# 本地词典下载记录

日期：2026-09-15。

## 已完成：ECDICT

来源：[skywind3000/ECDICT](https://github.com/skywind3000/ECDICT)，本地路径：`references/downloads/ecdict/repo/`。

仓库提交：`bc015ed2e24a7abef49fc6dbbb7fe32c1dadaf8b`。

主要文件：

| 文件 | 大小/数量 | SHA-256 | 用途 |
| --- | ---: | --- | --- |
| `ecdict.csv` | 770611 词条 | `1a6947e04785db63613a92e14903cdae7954f7e84860b10e68e5c7cbb3f9c3cf` | 英英释义、中文释义、音标、考试标签、词频、词形变化 |
| `stardict.7z` | 49 MB | `f370a0ecb58ada758d9dfe739db1667fd4ed87ed3055a4a7cb6c7054ecdf83d6` | ECDICT 打包词典文件 |
| `wordroot.txt` | 370702 bytes | `4b400dc5980e4a362fa12c7a49b326bb621c4e6bebd5f37146fbdcbe9db6bb6e` | 词根、词缀、构词线索 |
| `resemble.txt` | 529302 bytes | `925cb321dd3871f13fa2e00d288e28a5e544525bb8860b916c0d8c2341e80ecc` | 近义词辨析、词组辨析、联想材料 |
| `lemma.en.txt` | 2318694 bytes | `e255b097404e3e0052060e2ddf6e15a1414f577071d63d51d2ca0ce9dacee0fc` | 词形还原、lemma 查询 |

ECDICT README 说明其字段包括 `word`、`phonetic`、`definition`、`translation`、`pos`、`collins`、`oxford`、`tag`、`bnc`、`frq`、`exchange`、`detail`、`audio`。其中 `detail` 和 `audio` 标注为待添加，不能假装有完整例句和音频。

## 已完成：WordNet 3.0

来源：[Princeton WordNet](https://wordnet.princeton.edu/)，下载地址：`https://wordnetcode.princeton.edu/3.0/WNdb-3.0.tar.gz`。

本地路径：`references/downloads/wordnet/`。

文件：`WNdb-3.0.tar.gz`，SHA-256：`658b1ba191f5f98c2e9bae3e25c186013158f30ef779f191d2a44e5d25046dc8`。

已解包到 `references/downloads/wordnet/dict/`，包括 `index.*` 和 `data.*`。可用于英英释义、同义词集合、反义词关系、上位/下位关系和部分例句。抽样验证：`resign` 包含义项 `accept as inevitable`，并含例句 `He resigned himself to his fate`。

## 部分下载：Kaikki / Wiktionary English

来源：[Kaikki English machine-readable dictionary](https://kaikki.org/dictionary/English/)，文件：`kaikki.org-dictionary-English.jsonl`。

目标大小：3244676342 bytes。当前本地部分文件：`references/downloads/kaikki-wiktionary/kaikki.org-dictionary-English.jsonl`，已下载 1184970056 bytes。

该来源覆盖 Wiktionary 的英英释义、词源、例句、发音、词形、语义关系、派生词、相关词和短语，最接近“丰富词典层”的目标。但当前网络到 Kaikki 的 HTTPS/Range 连接不稳定，下载卡在 36.5%。该文件暂不能作为已完成来源使用，后续可断点续传或寻找可靠镜像。

## 下一步建议

先把 ECDICT 和 WordNet 合成一个本地 `dictionary_entries` / `dictionary_relations` 索引层，用于查询、入库辅助和老师解释。Kaikki 全量 Wiktionary 等网络稳定后继续补齐，作为词源、派生词、真实用例和短语的增强层。
