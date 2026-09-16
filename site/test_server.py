import importlib.util
import json
import sqlite3
import tempfile
import unittest
import threading
import urllib.request
import urllib.error
from pathlib import Path

spec = importlib.util.spec_from_file_location('english_server', Path(__file__).with_name('server.py'))
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


def make_dictionary_db(path):
    with sqlite3.connect(path) as conn:
        conn.executescript("""
        CREATE TABLE entries(
          word TEXT PRIMARY KEY, sw TEXT NOT NULL, phonetic TEXT, definition TEXT,
          translation TEXT, pos TEXT, collins INTEGER, oxford INTEGER, tag TEXT,
          bnc INTEGER, frq INTEGER, exchange TEXT, detail TEXT, audio TEXT, source TEXT NOT NULL
        );
        CREATE INDEX entries_sw ON entries(sw, word COLLATE NOCASE);
        CREATE TABLE wordnet_senses(
          id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL, pos TEXT NOT NULL,
          offset TEXT NOT NULL, gloss TEXT NOT NULL, examples TEXT NOT NULL,
          synonyms TEXT NOT NULL, source TEXT NOT NULL, UNIQUE(word,pos,offset)
        );
        CREATE TABLE relations(word TEXT NOT NULL, relation TEXT NOT NULL, related_word TEXT NOT NULL, pos TEXT, source TEXT NOT NULL, UNIQUE(word,relation,related_word,pos,source));
        CREATE TABLE roots(word TEXT NOT NULL, root TEXT NOT NULL, root_class TEXT, meaning TEXT, note TEXT, source TEXT NOT NULL, UNIQUE(word,root,source));
        CREATE TABLE resemble_notes(word TEXT NOT NULL, group_key TEXT NOT NULL, note TEXT NOT NULL, source TEXT NOT NULL, UNIQUE(word,group_key,note));
        CREATE TABLE lemmas(form TEXT NOT NULL, lemma TEXT NOT NULL, source TEXT NOT NULL, UNIQUE(form,lemma));
        CREATE TABLE phrases(headword TEXT, phrase TEXT NOT NULL, meaning TEXT NOT NULL, source_collection TEXT, source TEXT NOT NULL, UNIQUE(headword,phrase,meaning,source_collection));
        CREATE TABLE examples(headword TEXT, english TEXT NOT NULL, chinese TEXT, source_collection TEXT, source TEXT NOT NULL, UNIQUE(headword,english,chinese,source_collection));
        CREATE TABLE sources(id TEXT PRIMARY KEY, path TEXT NOT NULL, sha256 TEXT, rows INTEGER, note TEXT NOT NULL);
        CREATE TABLE build_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """)
        conn.execute(
            "INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("resign", "resign", "ri'zain", "v. accept as inevitable",
             "vt. 辞职, 放弃, 使顺从\nvi. 辞职, 屈从", "v", None, None,
             "gk cet4 cet6", 2549, 3390, "p:resigned/d:resigned/i:resigning/3:resigns", None, None, "ecdict"))
        conn.execute("INSERT INTO lemmas VALUES (?,?,?)", ("resigned", "resign", "wordnet"))
        conn.execute("INSERT INTO roots VALUES (?,?,?,?,?,?)", ("resign", "re-", "prefix", "again; back", "", "ecdict_wordroot"))
        conn.execute("INSERT INTO wordnet_senses(word,pos,offset,gloss,examples,synonyms,source) VALUES (?,?,?,?,?,?,?)",
                     ("resign", "v", "00614057", "accept as inevitable", json.dumps(["He resigned himself to his fate"]), json.dumps(["reconcile", "submit"]), "wordnet"))
        conn.execute("INSERT INTO relations VALUES (?,?,?,?,?)", ("resign", "antonym", "take office", "v", "wordnet"))
        conn.execute("INSERT INTO resemble_notes VALUES (?,?,?,?)", ("resign", "resign", "resign / resignation / resigned 容易成组记忆", "ecdict_resemble"))
        conn.execute("INSERT INTO phrases VALUES (?,?,?,?,?)", ("resign", "resign oneself to", "使自己接受；听任", "CET4", "ecdict_detail"))
        conn.execute("INSERT INTO phrases VALUES (?,?,?,?,?)", ("resign", "resign oneself to", "使自己接受；听任", "CET6", "ecdict_detail"))
        conn.execute("INSERT INTO examples VALUES (?,?,?,?,?)", ("resign", "At sixteen, I resigned myself to the fact that I'd never be a dancer.", "十六岁时，我无奈接受自己永远不会成为舞者的事实。", "CET4", "ecdict_detail"))
        conn.execute("INSERT INTO examples VALUES (?,?,?,?,?)", ("resign", "At sixteen, I resigned myself to the fact that I'd never be a dancer.", "十六岁时，我无奈接受自己永远不会成为舞者的事实。", "CET6", "ecdict_detail"))
        conn.execute("INSERT INTO sources VALUES (?,?,?,?,?)", ("ecdict", "/tmp/ecdict.csv", "sha", 1, "test source"))
        conn.execute("INSERT INTO build_meta VALUES (?,?)", ("entries", "1"))


class LearningSiteTests(unittest.TestCase):
    def test_http_rejects_unauthenticated_write_and_file_traversal(self):
        httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        base = 'http://127.0.0.1:' + str(httpd.server_port)
        try:
            request = urllib.request.Request(base + '/api/chat', data=b'{}', headers={'Content-Type': 'application/json'})
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(request)
            self.assertEqual(error.exception.code, 403)
            error.exception.close()
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(base + '/api/session?id=../LEARNER')
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(base + '/../LEARNER.md')
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_new_chapter_is_discovered_without_frontend_edit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'book/new-topic').mkdir(parents=True)
            (root / 'book/new-topic/lesson.md').write_text('# 新章节\n\n真实正文', encoding='utf-8')
            items = server.catalog(root)
            self.assertEqual(items[0]['id'], 'book/new-topic/lesson.md')
            self.assertEqual(items[0]['title'], '新章节')
            self.assertIn('真实正文', items[0]['body'])

    def test_repository_docs_are_discovered_with_groups(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for rel in ['engineering/agents/conventions.md', 'engineering/design/plan.md',
                        'engineering/methodology/sla.md', 'engineering/archive/old-plan.md',
                        'AGENTS.md', 'README.md',
                        'progress/diagnosis.md', 'references/README.md',
                        'book/BACKLOG.md', 'book/TEMPLATE.md', 'book/README.md',
                        'vocabulary/old-lesson.md', 'book/08-frames/extra.md']:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('# ' + path.stem + '\n文档', encoding='utf-8')
            items = server.catalog(root)
            by_id = {i['id']: i for i in items}
            expect = [
                ('AGENTS.md', 'engineering', 'Agent 文档', False),
                ('engineering/agents/conventions.md', 'engineering', 'Agent 文档', False),
                ('engineering/design/plan.md', 'engineering', '设计', False),
                ('engineering/methodology/sla.md', 'engineering', '调研与方法', False),
                ('engineering/archive/old-plan.md', 'engineering', '历史归档', False),
                ('progress/diagnosis.md', 'progress', '进度与诊断', False),
                ('references/README.md', 'reference', '参考资料', False),
                ('book/BACKLOG.md', 'engineering', 'Agent 文档', False),
                ('book/TEMPLATE.md', 'engineering', 'Agent 文档', False),
                ('vocabulary/old-lesson.md', 'history', '历史课堂', False),
                ('book/08-frames/extra.md', 'book-extra', '句式框架', False),
            ]
            for rel, section, group, hidden in expect:
                item = by_id[rel]
                self.assertEqual(item['section'], section, rel)
                self.assertEqual(item['group'], group, rel)
                self.assertEqual(bool(item.get('hidden')), hidden, rel)
            for rel in ['references/imports/2026-09-14/report.json', 'site/public/app.js',
                        'data/learning.sqlite3']:
                self.assertNotIn(rel, by_id)
            self.assertTrue(by_id['README.md'].get('hidden'))
            self.assertTrue(by_id['book/README.md'].get('hidden'))

    def test_materials_index_is_discovered_and_vendor_docs_are_skipped(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for rel in ['materials/README.md', 'materials/vocabulary/notes.md',
                        'materials/dictionaries/ecdict/repo/README.md']:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('# 学习资料\n\n索引', encoding='utf-8')
            items = server.catalog(root)
            by_id = {i['id']: i for i in items}
            self.assertIn('materials/README.md', by_id)
            self.assertEqual(by_id['materials/README.md']['section'], 'reference')
            self.assertEqual(by_id['materials/README.md']['group'], '学习资料')
            self.assertNotIn('materials/vocabulary/notes.md', by_id)
            self.assertNotIn('materials/dictionaries/ecdict/repo/README.md', by_id)

    def test_prompt_includes_profile_chapter_and_actual_history(self):
        prompt = server.teaching_prompt(
            [{'role': 'user', 'content': '我的原始回答'}],
            {'id': 'book/x.md', 'body': 'gain traction = 获得支持'},
            '高考138；听力暂缓', '已讲解不等于掌握')
        for value in ['我的原始回答', 'gain traction', '高考138', '已讲解不等于掌握']:
            self.assertIn(value, prompt)

    def test_session_persistence_and_path_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = {'id': 'a' * 32, 'messages': [{'role': 'user', 'content': '我不知道'}]}
            server.save_session(root, session)
            self.assertEqual(server.load_session(root, session['id']), session)
            with self.assertRaises(ValueError):
                server.load_session(root, '../LEARNER')

    def test_dictionary_lookup_resolves_inflected_forms_and_deduplicates_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            server.DICTIONARY = server.DictionaryStore(Path(temp) / 'dictionary.sqlite3')
            make_dictionary_db(server.DICTIONARY.path)
            result = server.dictionary_store().lookup('resigned')
            self.assertEqual(result['query'], 'resigned')
            self.assertEqual(result['resolved_word'], 'resign')
            self.assertEqual(result['entry']['definition'], 'v. accept as inevitable')
            self.assertEqual(result['entry']['translation'], 'vt. 辞职, 放弃, 使顺从\nvi. 辞职, 屈从')
            self.assertEqual(result['roots'][0]['root'], 're-')
            self.assertEqual(result['senses'][0]['examples'], ["He resigned himself to his fate"])
            self.assertEqual(result['phrases'][0]['source_collections'], ['CET4', 'CET6'])
            self.assertEqual(result['examples'][0]['source_collections'], ['CET4', 'CET6'])
            server.DICTIONARY = None

    def test_dictionary_http_search_and_stats(self):
        with tempfile.TemporaryDirectory() as temp:
            server.DICTIONARY = server.DictionaryStore(Path(temp) / 'dictionary.sqlite3')
            make_dictionary_db(server.DICTIONARY.path)
            httpd = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            base = 'http://127.0.0.1:' + str(httpd.server_port)
            try:
                with urllib.request.urlopen(base + '/api/dictionary/search?q=resig&limit=5') as response:
                    payload = json.loads(response.read())
                self.assertEqual(payload['items'][0]['word'], 'resign')
                with urllib.request.urlopen(base + '/api/dictionary/stats') as response:
                    stats = json.loads(response.read())
                self.assertEqual(stats['tables']['entries'], 1)
                self.assertEqual(stats['sources'][0]['id'], 'ecdict')
            finally:
                httpd.shutdown()
                httpd.server_close()
                server.DICTIONARY = None


if __name__ == '__main__':
    unittest.main()
