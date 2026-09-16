import json
import re
import sqlite3
from pathlib import Path


def normalize_word(value):
    return re.sub(r'\s+', ' ', (value or '').strip()).lower()


def positive_int(value, default, maximum):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(1, min(parsed, maximum))


class DictionaryStore:
    def __init__(self, path):
        self.path = Path(path)

    def exists(self):
        return self.path.exists()

    def connect(self):
        if not self.exists():
            raise FileNotFoundError(f'词典数据库不存在：{self.path}')
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def lookup(self, word, limits=None):
        query = normalize_word(word)
        if not query:
            raise ValueError('请提供要查询的单词或词组')
        limits = limits or {}
        phrase_limit = positive_int(limits.get('phrases'), 20, 80)
        example_limit = positive_int(limits.get('examples'), 12, 50)
        sense_limit = positive_int(limits.get('senses'), 12, 50)
        relation_limit = positive_int(limits.get('relations'), 40, 120)
        note_limit = positive_int(limits.get('notes'), 10, 50)
        form_limit = positive_int(limits.get('forms'), 20, 80)

        with self.connect() as conn:
            resolved = self._resolve(conn, query)
            if not resolved:
                return {'query': query, 'found': False, 'resolved_word': None}
            word = resolved['word']
            entry = self._entry(conn, word)
            return {
                'query': query,
                'found': True,
                'resolved_word': word,
                'match': resolved,
                'entry': entry,
                'roots': self._rows(conn, 'SELECT root, root_class, meaning, note, source FROM roots WHERE word=? ORDER BY root LIMIT ?', [word, note_limit]),
                'resemble_notes': self._rows(conn, 'SELECT group_key, note, source FROM resemble_notes WHERE word=? ORDER BY group_key, note LIMIT ?', [word, note_limit]),
                'lemma_forms': self._rows(conn, 'SELECT form, lemma, source FROM lemmas WHERE lemma=? ORDER BY form LIMIT ?', [word, form_limit]),
                'senses': self._senses(conn, word, sense_limit),
                'relations': self._rows(conn, '''SELECT relation, related_word, pos, source FROM relations
                                                WHERE word=? ORDER BY relation, related_word LIMIT ?''', [word, relation_limit]),
                'phrases': self._grouped(conn, '''SELECT phrase, meaning, source,
                                                         group_concat(DISTINCT source_collection) AS source_collections
                                                  FROM phrases WHERE headword=?
                                                  GROUP BY phrase, meaning, source
                                                  ORDER BY phrase LIMIT ?''', [word, phrase_limit]),
                'examples': self._grouped(conn, '''SELECT english, chinese, source,
                                                          group_concat(DISTINCT source_collection) AS source_collections
                                                   FROM examples WHERE headword=?
                                                   GROUP BY english, chinese, source
                                                   ORDER BY english LIMIT ?''', [word, example_limit]),
            }

    def search(self, query, limit=20):
        query = normalize_word(query)
        if not query:
            return {'query': query, 'items': []}
        limit = positive_int(limit, 20, 50)
        with self.connect() as conn:
            rows = conn.execute('''SELECT word, phonetic, definition, translation, pos, tag, bnc, frq, source
                                   FROM entries
                                   WHERE word LIKE ? OR sw LIKE ?
                                   ORDER BY CASE WHEN word=? THEN 0 WHEN word LIKE ? THEN 1 ELSE 2 END,
                                            bnc IS NULL, bnc, frq IS NULL, frq, word
                                   LIMIT ?''',
                                [query + '%', query + '%', query, query + '%', limit]).fetchall()
            return {'query': query, 'items': [dict(row) for row in rows]}

    def stats(self):
        tables = ['entries', 'roots', 'lemmas', 'resemble_notes', 'wordnet_senses', 'relations', 'phrases', 'examples']
        with self.connect() as conn:
            counts = {table: conn.execute(f'SELECT count(*) FROM {table}').fetchone()[0] for table in tables}
            sources = [dict(row) for row in conn.execute('SELECT id, path, sha256, rows, note FROM sources ORDER BY id')]
            meta = {row['key']: row['value'] for row in conn.execute('SELECT key, value FROM build_meta ORDER BY key')}
            return {'path': str(self.path), 'tables': counts, 'sources': sources, 'build_meta': meta}

    def _resolve(self, conn, query):
        row = conn.execute('SELECT word FROM entries WHERE word=? COLLATE NOCASE', [query]).fetchone()
        if row:
            return {'type': 'entry', 'word': row['word']}
        row = conn.execute('SELECT word FROM entries WHERE sw=? LIMIT 1', [query]).fetchone()
        if row:
            return {'type': 'entry_sw', 'word': row['word']}
        row = conn.execute('''SELECT l.lemma AS word, l.form, l.source FROM lemmas l
                              JOIN entries e ON e.word=l.lemma
                              WHERE l.form=? COLLATE NOCASE
                              ORDER BY length(l.lemma), l.lemma LIMIT 1''', [query]).fetchone()
        if row:
            return {'type': 'lemma', 'word': row['word'], 'form': row['form'], 'source': row['source']}
        return None

    def _entry(self, conn, word):
        row = conn.execute('SELECT * FROM entries WHERE word=?', [word]).fetchone()
        return dict(row) if row else None

    def _rows(self, conn, sql, params):
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def _grouped(self, conn, sql, params):
        rows = []
        for row in conn.execute(sql, params).fetchall():
            item = dict(row)
            item['source_collections'] = [v for v in (item.get('source_collections') or '').split(',') if v]
            rows.append(item)
        return rows

    def _senses(self, conn, word, limit):
        rows = []
        for row in conn.execute('''SELECT pos, offset, gloss, examples, synonyms, source
                                   FROM wordnet_senses WHERE word=?
                                   ORDER BY pos, offset LIMIT ?''', [word, limit]).fetchall():
            item = dict(row)
            item['examples'] = json.loads(item['examples'] or '[]')
            item['synonyms'] = json.loads(item['synonyms'] or '[]')
            rows.append(item)
        return rows
