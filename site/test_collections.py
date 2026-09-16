import tempfile
import unittest
from pathlib import Path
from learning_store import Store

class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.s=Store(Path(self.tmp.name)/'learning.sqlite3')
    def tearDown(self):self.tmp.cleanup()
    def test_overlap_keeps_one_headword_and_preserves_learning(self):
        a={'kind':'word','title':'assume','meaning':'假定','body':'原有讲解','source':'Book教学材料'}
        item=self.s.add(a);self.s.record(item['id'],'understand','learn','original')
        before=self.s.get(item['id'])
        self.s.import_collection({'id':'cet4','title':'四级','source_url':'https://example.org/one'},[dict(a,meaning='假设；承担',body='词典资料')])
        self.s.import_collection({'id':'cet6','title':'六级'},[dict(a,meaning='认为；承担',body='另一个来源')])
        self.assertEqual(self.s.stats()['items'],1)
        after=self.s.get(item['id']);self.assertEqual(before['progress'],after['progress']);self.assertEqual(after['body'],'原有讲解')
        self.assertEqual(len(after['collections']),2)
        self.assertEqual(self.s.browse(collection='cet6')['total'],1)
    def test_pagination_search_and_repeat_import(self):
        meta={'id':'source','title':'词表'}
        rows=[{'kind':'word','title':f'word {i:03}','meaning':'测试'} for i in range(125)]
        self.s.import_collection(meta,rows);self.s.import_collection(meta,rows)
        self.assertEqual(self.s.stats()['items'],125)
        a=self.s.browse(collection='source',offset=0,limit=100)
        b=self.s.browse(collection='source',offset=100,limit=100)
        self.assertEqual((len(a['items']),len(b['items'])),(100,25))
        self.assertFalse(set(x['id'] for x in a['items'])&set(x['id'] for x in b['items']))
        self.assertNotIn('body',a['items'][0])
        self.assertEqual(self.s.browse(q='word 124')['total'],1)
        self.assertEqual(len(self.s.export()['collection_items']),125)
    def test_phrase_senses_stay_distinct(self):
        self.s.import_collection({'id':'a','title':'A'},[{'kind':'phrase','title':'account for','meaning':'解释'}])
        self.s.import_collection({'id':'b','title':'B'},[{'kind':'phrase','title':'account for','meaning':'占比'}])
        self.assertEqual(self.s.stats()['items'],2)

if __name__=='__main__':unittest.main()
