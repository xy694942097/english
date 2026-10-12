import json
import tempfile
import unittest
from pathlib import Path
import server


class ViewerTests(unittest.TestCase):
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
        for group in nav['groups'] + nav.get('maintenance', []):
            for item in group['items']:
                parent = Path(group['title'])
                paths = [item] if isinstance(item, str) else item['items']
                if isinstance(item, dict):
                    parent /= item['sub']
                for path in paths:
                    self.assertEqual(Path(path).parent, parent)
                    self.assertTrue((server.ROOT / path).is_file())

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
