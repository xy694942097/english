import json
import tempfile
import unittest
from pathlib import Path
import server


class ViewerTests(unittest.TestCase):
    def test_reader_has_no_editing_components(self):
        html = (server.STATIC / 'index.html').read_text()
        js = (server.STATIC / 'app.js').read_text()
        self.assertNotIn('edit-document', html)
        self.assertNotIn('contentEditable', js)
        self.assertFalse(hasattr(server, 'save_document'))

    def test_static_publication_uses_explicit_document_list(self):
        import build_static
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'english'
            count = build_static.build(output, server.ROOT / 'site/publish-nav.json')
            data = json.loads((output / 'catalog.json').read_text())
            publish_nav = json.loads((server.ROOT / 'site/publish-nav.json').read_text())
            def paths(entries):
                for entry in entries:
                    if isinstance(entry, str):
                        yield entry
                    else:
                        yield from paths(entry['items'])
            expected = {p for group in publish_nav['groups'] + publish_nav.get('maintenance', [])
                        for p in paths(group['items'])}
            self.assertEqual(count, len(expected))
            self.assertEqual({item['id'] for item in data['items']}, expected)
            self.assertIn('course/词汇/生词与熟词新义.md', {item['id'] for item in data['items']})
            self.assertIn('course/Chunks 收集/精选 Chunks.md', {item['id'] for item in data['items']})
            self.assertIn('course/表达练习/Better Call Saul S01 中译英练习.md', {item['id'] for item in data['items']})
            self.assertFalse(any('/我的学习/' in item['id'] for item in data['items']))
            self.assertTrue(any('/编纂与维护/Skills/' in item['id'] for item in data['items']))
            self.assertIn('course/编纂与维护/Skills/根据 Chunks 编写中译英练习.md',
                          {item['id'] for item in data['items']})
            self.assertIn('原文与参考资料', {group['title'] for group in data['nav']['groups']})
            self.assertEqual(sum(item.get('referenceOnly', False) for item in data['items']), 8)
            self.assertFalse((output / 'materials').exists())
            self.assertFalse((output / 'vendor/toastui').exists())
            self.assertTrue((output / '.nojekyll').is_file())
            self.assertIn('src="./app.js"', (output / 'index.html').read_text())

    def test_catalog_lists_only_registered_docs_with_md_titles(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'nav.json').write_text(json.dumps({'groups': [
                {'title': '第一组', 'items': [
                    'a.md',
                    {'sub': '小标签', 'items': ['sub/b.md']},
                ]},
                {'title': '档案', 'items': ['LEARNER.md']},
            ]}, ensure_ascii=False), encoding='utf-8')
            for rel, body in [('a.md', '# 甲章\n正文'), ('sub/b.md', '# 乙章\n正文'),
                              ('LEARNER.md', '# 学习者\n正文'), ('not-listed.md', '# 未登记\n不应出现')]:
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding='utf-8')
            items = server.catalog(root)
            by_id = {i['id']: i for i in items}
            # 登记的（含嵌套小标签下的）：进目录，标题取自正文一级标题，组名正确
            self.assertEqual(by_id['a.md']['title'], '甲章')
            self.assertEqual(by_id['a.md']['group'], '第一组')
            self.assertEqual(by_id['sub/b.md']['group'], '第一组')
            self.assertEqual(by_id['LEARNER.md']['group'], '档案')
            # 未登记的：不进目录
            self.assertNotIn('not-listed.md', by_id)

    def test_no_title_falls_back_to_stem(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'nav.json').write_text(json.dumps({'groups': [
                {'title': '组', 'items': ['x.md']}]}), encoding='utf-8')
            (root / 'x.md').write_text('没有一级标题的正文', encoding='utf-8')
            items = server.catalog(root)
            self.assertEqual(items[0]['title'], 'x')

    def test_maintenance_docs_remain_searchable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'tools.md').write_text('# 维护工具\n工具正文')
            (root / 'nav.json').write_text(json.dumps({'groups': [], 'maintenance': [
                {'title': '编纂与维护', 'items': ['tools.md']},
            ]}, ensure_ascii=False))
            items = server.catalog(root)
            self.assertEqual(items[0]['id'], 'tools.md')
            self.assertEqual(items[0]['group'], '编纂与维护')

    def test_project_navigation_matches_filesystem(self):
        nav = server.read_nav()
        self.assertEqual([g['title'] for g in nav['groups'][:3]], ['词汇', 'Chunks 收集', '表达练习'])
        for group in nav['groups'] + nav.get('maintenance', []):
            for item in group['items']:
                parent = Path('course') / group['title']
                paths = [item] if isinstance(item, str) else item['items']
                if isinstance(item, dict):
                    parent /= item['sub']
                for path in paths:
                    self.assertEqual(Path(path).parent, parent)
                    self.assertTrue((server.ROOT / path).is_file())

    def test_old_document_aliases_resolve_directly_to_course(self):
        aliases = server.read_aliases()
        documents = {item['id'] for item in server.catalog()}
        old = '学习章节/句式与结构/nothing but：几个小词，意思为什么差这么多.md'
        self.assertEqual(aliases[old], 'course/Chunks 收集/精选 Chunks.md')
        self.assertEqual(aliases['book/05-patterns/01-nothing-but.md'], 'course/Chunks 收集/精选 Chunks.md')
        self.assertEqual(aliases['book/01-reading/02-resigned.md'], 'course/词汇/生词与熟词新义.md')
        for target in aliases.values():
            self.assertTrue((server.ROOT / target).is_file(), target)
        self.assertIn(aliases[old], documents)

    def test_missing_registered_doc_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'nav.json').write_text(json.dumps({'groups': [
                {'title': '组', 'items': ['gone.md']}]}), encoding='utf-8')
            with self.assertRaises(FileNotFoundError):
                server.catalog(root)

    def test_resolve_inside_root_blocks_traversal(self):
        self.assertIsNotNone(server.resolve_inside_root('book/x.md'))
        self.assertIsNone(server.resolve_inside_root('../outside.md'))
        self.assertIsNone(server.resolve_inside_root('book/../../etc/passwd'))


if __name__ == '__main__':
    unittest.main()
