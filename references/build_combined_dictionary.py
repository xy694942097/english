#!/usr/bin/env python3
"""Build a local combined dictionary from downloaded English resources."""

import argparse
import csv
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / "materials" / "dictionaries"
DEFAULT_OUTPUT = ROOT / "data" / "combined_dictionary.sqlite3"
WORDNET_POS = {
    "noun": "n",
    "verb": "v",
    "adj": "a",
    "adv": "r",
}
POINTERS = {
    "!": "antonym",
    "@": "hypernym",
    "~": "hyponym",
    "%p": "part_meronym",
    "%m": "member_meronym",
    "%s": "substance_meronym",
    "#p": "part_holonym",
    "#m": "member_holonym",
    "#s": "substance_holonym",
    "+": "derivation",
    ";c": "domain_topic",
    "-c": "member_topic",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def norm(value):
    return " ".join(str(value or "").casefold().split()).strip()


def stripword(value):
    return "".join(ch for ch in str(value or "") if ch.isalnum()).casefold()


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def connect_output(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE entries(
          word TEXT PRIMARY KEY,
          sw TEXT NOT NULL,
          phonetic TEXT,
          definition TEXT,
          translation TEXT,
          pos TEXT,
          collins INTEGER,
          oxford INTEGER,
          tag TEXT,
          bnc INTEGER,
          frq INTEGER,
          exchange TEXT,
          detail TEXT,
          audio TEXT,
          source TEXT NOT NULL
        );
        CREATE INDEX entries_sw ON entries(sw, word COLLATE NOCASE);
        CREATE INDEX entries_tag ON entries(tag);
        CREATE INDEX entries_bnc ON entries(bnc);
        CREATE INDEX entries_frq ON entries(frq);

        CREATE TABLE wordnet_senses(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          word TEXT NOT NULL,
          pos TEXT NOT NULL,
          offset TEXT NOT NULL,
          gloss TEXT NOT NULL,
          examples TEXT NOT NULL,
          synonyms TEXT NOT NULL,
          source TEXT NOT NULL,
          UNIQUE(word,pos,offset)
        );
        CREATE INDEX wordnet_senses_word ON wordnet_senses(word);

        CREATE TABLE relations(
          word TEXT NOT NULL,
          relation TEXT NOT NULL,
          related_word TEXT NOT NULL,
          pos TEXT,
          source TEXT NOT NULL,
          UNIQUE(word,relation,related_word,pos,source)
        );
        CREATE INDEX relations_word ON relations(word, relation);

        CREATE TABLE roots(
          word TEXT NOT NULL,
          root TEXT NOT NULL,
          root_class TEXT,
          meaning TEXT,
          note TEXT,
          source TEXT NOT NULL,
          UNIQUE(word,root,source)
        );
        CREATE INDEX roots_word ON roots(word);

        CREATE TABLE resemble_notes(
          word TEXT NOT NULL,
          group_key TEXT NOT NULL,
          note TEXT NOT NULL,
          source TEXT NOT NULL,
          UNIQUE(word,group_key,note)
        );
        CREATE INDEX resemble_word ON resemble_notes(word);

        CREATE TABLE lemmas(
          form TEXT NOT NULL,
          lemma TEXT NOT NULL,
          source TEXT NOT NULL,
          UNIQUE(form,lemma)
        );
        CREATE INDEX lemmas_form ON lemmas(form);

        CREATE TABLE phrases(
          headword TEXT,
          phrase TEXT NOT NULL,
          meaning TEXT NOT NULL,
          source_collection TEXT,
          source TEXT NOT NULL,
          UNIQUE(headword,phrase,meaning,source_collection)
        );
        CREATE INDEX phrases_headword ON phrases(headword);
        CREATE INDEX phrases_phrase ON phrases(phrase);

        CREATE TABLE examples(
          headword TEXT,
          english TEXT NOT NULL,
          chinese TEXT,
          source_collection TEXT,
          source TEXT NOT NULL,
          UNIQUE(headword,english,chinese,source_collection)
        );
        CREATE INDEX examples_headword ON examples(headword);

        CREATE TABLE sources(
          id TEXT PRIMARY KEY,
          path TEXT NOT NULL,
          sha256 TEXT,
          rows INTEGER,
          note TEXT NOT NULL
        );

        CREATE TABLE build_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """
    )
    return conn


def int_or_none(value):
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def import_ecdict(conn, path):
    count = 0
    words = set()
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            word = row.get("word", "").strip()
            if not word:
                continue
            words.add(norm(word))
            batch.append(
                (
                    word,
                    stripword(word),
                    row.get("phonetic", ""),
                    row.get("definition", ""),
                    row.get("translation", ""),
                    row.get("pos", ""),
                    int_or_none(row.get("collins")),
                    int_or_none(row.get("oxford")),
                    row.get("tag", ""),
                    int_or_none(row.get("bnc")),
                    int_or_none(row.get("frq")),
                    row.get("exchange", ""),
                    row.get("detail", ""),
                    row.get("audio", ""),
                    "ECDICT",
                )
            )
            count += 1
            if len(batch) >= 5000:
                conn.executemany(
                    "INSERT OR REPLACE INTO entries VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    batch,
                )
                batch.clear()
        if batch:
            conn.executemany(
                "INSERT OR REPLACE INTO entries VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                batch,
            )
    return count, words


def load_wordroot(path):
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


def import_roots(conn, path, known_words):
    rows = []
    data = load_wordroot(path)
    for root, info in data.items():
        words = info.get("words") or info.get("word") or info.get("example") or []
        if isinstance(words, str):
            words = [words]
        note = json.dumps(info, ensure_ascii=False, sort_keys=True)
        for word in words:
            if norm(word) in known_words:
                rows.append(
                    (
                        word,
                        info.get("root") or root,
                        info.get("class", ""),
                        info.get("meaning", ""),
                        note,
                        "ECDICT wordroot.txt",
                    )
                )
    conn.executemany("INSERT OR IGNORE INTO roots VALUES(?,?,?,?,?,?)", rows)
    return len(rows)


def import_lemmas(conn, path):
    rows = []
    for raw in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        parts = raw.split()
        if len(parts) < 2:
            continue
        rows.append((parts[0], parts[1], "ECDICT lemma.en.txt"))
    conn.executemany("INSERT OR IGNORE INTO lemmas VALUES(?,?,?)", rows)
    return len(rows)


def import_resemble(conn, path, known_words):
    rows = []
    group_terms = []
    group_key = ""
    for raw in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%"):
            group_key = line[1:].strip()
            group_terms = [x.strip() for x in re.split(r"[,，]", group_key) if x.strip()]
            continue
        if not line.startswith("-"):
            continue
        body = line[1:].strip()
        term, _, note = body.partition(":")
        term = term.strip()
        note = note.strip() or body
        candidates = list(group_terms)
        if term:
            candidates.append(term)
        for word in dict.fromkeys(candidates):
            if norm(word) in known_words:
                rows.append((word, group_key, note, "ECDICT resemble.txt"))
    conn.executemany("INSERT OR IGNORE INTO resemble_notes VALUES(?,?,?,?)", rows)
    return len(rows)


def parse_wordnet_data_line(line):
    if "|" not in line:
        return None
    head, gloss_text = line.split("|", 1)
    parts = head.split()
    if len(parts) < 5:
        return None
    offset = parts[0]
    pos = parts[2]
    word_count = int(parts[3], 16)
    idx = 4
    words = []
    for _ in range(word_count):
        words.append(parts[idx].replace("_", " "))
        idx += 2
    pointers = []
    if idx < len(parts):
        pointer_count = int(parts[idx])
        idx += 1
        for _ in range(pointer_count):
            if idx + 3 >= len(parts):
                break
            pointers.append((parts[idx], parts[idx + 1], parts[idx + 2]))
            idx += 4
    examples = re.findall(r'"([^"]+)"', gloss_text)
    gloss = re.sub(r'"[^"]+"', "", gloss_text).strip(" ;")
    return {
        "offset": offset,
        "pos": pos,
        "words": words,
        "pointers": pointers,
        "gloss": gloss,
        "examples": examples,
    }


def load_wordnet_data(wordnet_dir):
    data = {}
    base = Path(wordnet_dir)
    for name, pos in WORDNET_POS.items():
        path = base / f"data.{name}"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line or line.startswith("  "):
                continue
            parsed = parse_wordnet_data_line(line)
            if parsed:
                data[(pos, parsed["offset"])] = parsed
    return data


def iter_wordnet_index(wordnet_dir, known_words):
    base = Path(wordnet_dir)
    for name, pos in WORDNET_POS.items():
        path = base / f"index.{name}"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line or line.startswith(" "):
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            word = parts[0].replace("_", " ")
            if norm(word) not in known_words:
                continue
            synset_count = int(parts[2])
            pointer_count = int(parts[3])
            offset_start = 4 + pointer_count + 2
            for offset in parts[offset_start : offset_start + synset_count]:
                yield word, pos, offset


def import_wordnet(conn, wordnet_dir, known_words):
    data = load_wordnet_data(wordnet_dir)
    senses = 0
    relation_rows = []
    for word, pos, offset in iter_wordnet_index(wordnet_dir, known_words):
        parsed = data.get((pos, offset))
        if not parsed:
            continue
        synonyms = [w for w in parsed["words"] if norm(w) != norm(word)]
        conn.execute(
            """
            INSERT OR IGNORE INTO wordnet_senses
            (word,pos,offset,gloss,examples,synonyms,source)
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                word,
                pos,
                offset,
                parsed["gloss"],
                json.dumps(parsed["examples"], ensure_ascii=False),
                json.dumps(synonyms, ensure_ascii=False),
                "Princeton WordNet 3.0",
            ),
        )
        senses += 1
        for related in synonyms:
            relation_rows.append((word, "synonym", related, pos, "Princeton WordNet 3.0"))
        for symbol, target_offset, target_pos in parsed["pointers"]:
            relation = POINTERS.get(symbol)
            target = data.get((target_pos, target_offset))
            if not relation or not target:
                continue
            for related in target["words"]:
                if norm(related) != norm(word):
                    relation_rows.append((word, relation, related, target_pos, "Princeton WordNet 3.0"))
    conn.executemany("INSERT OR IGNORE INTO relations VALUES(?,?,?,?,?)", relation_rows)
    return senses, len(relation_rows)


def extract_examples(body):
    lines = body.splitlines()
    examples = []
    for i, line in enumerate(lines):
        if not line.startswith("> "):
            continue
        english = line[2:].strip()
        chinese = ""
        for follow in lines[i + 1 : i + 4]:
            if follow.strip() and not follow.startswith(">") and not follow.startswith("#"):
                chinese = follow.strip()
                break
        if english:
            examples.append((english, chinese))
    return examples


def extract_phrase_lines(body):
    phrases = []
    for line in body.splitlines():
        m = re.match(r"-\s+(.+?)[：:](.+)$", line.strip())
        if m:
            phrases.append((m.group(1).strip(), m.group(2).strip()))
    return phrases


def source_headword(body, fallback):
    m = re.search(r"来自词目[:：]\s*([^\n]+)", body)
    if m:
        return m.group(1).split(",")[0].strip()
    return fallback


def import_learning_db(conn, learning_db, known_words):
    if not learning_db or not Path(learning_db).exists():
        return 0, 0
    examples = []
    phrases = []
    query = """
      SELECT i.kind,i.title,i.meaning,m.body,c.id AS collection_id
      FROM items i
      LEFT JOIN collection_items m ON m.item_id=i.id
      LEFT JOIN collections c ON c.id=m.collection_id
    """
    with sqlite3.connect(learning_db) as src:
        src.row_factory = sqlite3.Row
        for row in src.execute(query):
            body = row["body"] or ""
            collection = row["collection_id"] or ""
            if row["kind"] == "word":
                headword = row["title"]
                if norm(headword) in known_words:
                    for english, chinese in extract_examples(body):
                        examples.append((headword, english, chinese, collection, "learning.sqlite3 collections"))
                    for phrase, meaning in extract_phrase_lines(body):
                        phrases.append((headword, phrase, meaning, collection, "learning.sqlite3 collections"))
            elif row["kind"] == "phrase":
                headword = source_headword(body, row["title"].split()[0])
                if norm(headword) in known_words:
                    phrases.append((headword, row["title"], row["meaning"], collection, "learning.sqlite3 phrase item"))
    conn.executemany("INSERT OR IGNORE INTO examples VALUES(?,?,?,?,?)", examples)
    conn.executemany("INSERT OR IGNORE INTO phrases VALUES(?,?,?,?,?)", phrases)
    return len(examples), len(phrases)


def register_source(conn, source_id, path, rows, note):
    path = Path(path)
    digest = sha256(path) if path.exists() and path.is_file() else ""
    conn.execute(
        "INSERT OR REPLACE INTO sources VALUES(?,?,?,?,?)",
        (source_id, str(path), digest, rows, note),
    )


def build_dictionary(
    output=DEFAULT_OUTPUT,
    ecdict_csv=DOWNLOADS / "ecdict" / "repo" / "ecdict.csv",
    wordroot=DOWNLOADS / "ecdict" / "repo" / "wordroot.txt",
    resemble=DOWNLOADS / "ecdict" / "repo" / "resemble.txt",
    lemma=DOWNLOADS / "ecdict" / "repo" / "lemma.en.txt",
    wordnet_dir=DOWNLOADS / "wordnet" / "dict",
    learning_db=ROOT / "data" / "learning.sqlite3",
):
    conn = connect_output(output)
    try:
        with conn:
            entries, known_words = import_ecdict(conn, ecdict_csv)
            roots = import_roots(conn, wordroot, known_words)
            lemmas = import_lemmas(conn, lemma)
            resemble_notes = import_resemble(conn, resemble, known_words)
            wordnet_senses, wordnet_relations = import_wordnet(conn, wordnet_dir, known_words)
            learning_examples, learning_phrases = import_learning_db(conn, learning_db, known_words)
            register_source(conn, "ecdict", ecdict_csv, entries, "ECDICT main CSV")
            register_source(conn, "ecdict-wordroot", wordroot, roots, "ECDICT word roots and affixes")
            register_source(conn, "ecdict-resemble", resemble, resemble_notes, "ECDICT resemble and phrase notes")
            register_source(conn, "ecdict-lemma", lemma, lemmas, "ECDICT lemma map")
            register_source(conn, "wordnet", Path(wordnet_dir).parent / "WNdb-3.0.tar.gz", wordnet_senses, "Princeton WordNet 3.0")
            if learning_db:
                register_source(conn, "learning-db", learning_db, learning_examples + learning_phrases, "English learning database examples and phrases")
            actual = {
                "entries": conn.execute("SELECT count(*) FROM entries").fetchone()[0],
                "roots": conn.execute("SELECT count(*) FROM roots").fetchone()[0],
                "lemmas": conn.execute("SELECT count(*) FROM lemmas").fetchone()[0],
                "resemble_notes": conn.execute("SELECT count(*) FROM resemble_notes").fetchone()[0],
                "wordnet_senses": conn.execute("SELECT count(*) FROM wordnet_senses").fetchone()[0],
                "wordnet_relations": conn.execute("SELECT count(*) FROM relations").fetchone()[0],
                "learning_examples": conn.execute("SELECT count(*) FROM examples").fetchone()[0],
                "learning_phrases": conn.execute("SELECT count(*) FROM phrases").fetchone()[0],
            }
            report = {
                "built_at": now(),
                "output": str(output),
                **actual,
                "attempted": {
                    "entries": entries,
                    "roots": roots,
                    "lemmas": lemmas,
                    "resemble_notes": resemble_notes,
                    "wordnet_senses": wordnet_senses,
                    "wordnet_relations": wordnet_relations,
                    "learning_examples": learning_examples,
                    "learning_phrases": learning_phrases,
                },
            }
            conn.execute("INSERT OR REPLACE INTO build_meta VALUES(?,?)", ("report", json.dumps(report, ensure_ascii=False)))
    finally:
        conn.close()
    return report


def main():
    parser = argparse.ArgumentParser(description="Build the local combined English dictionary SQLite database.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ecdict-csv", type=Path, default=DOWNLOADS / "ecdict" / "repo" / "ecdict.csv")
    parser.add_argument("--wordroot", type=Path, default=DOWNLOADS / "ecdict" / "repo" / "wordroot.txt")
    parser.add_argument("--resemble", type=Path, default=DOWNLOADS / "ecdict" / "repo" / "resemble.txt")
    parser.add_argument("--lemma", type=Path, default=DOWNLOADS / "ecdict" / "repo" / "lemma.en.txt")
    parser.add_argument("--wordnet-dir", type=Path, default=DOWNLOADS / "wordnet" / "dict")
    parser.add_argument("--learning-db", type=Path, default=ROOT / "data" / "learning.sqlite3")
    parser.add_argument("--report", type=Path, default=ROOT / "references" / "imports" / "2026-09-15-dictionary" / "report.json")
    args = parser.parse_args()
    report = build_dictionary(
        output=args.output,
        ecdict_csv=args.ecdict_csv,
        wordroot=args.wordroot,
        resemble=args.resemble,
        lemma=args.lemma,
        wordnet_dir=args.wordnet_dir,
        learning_db=args.learning_db,
    )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
