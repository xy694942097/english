import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from learning_store import Store


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.sqlite3'
        self.s = Store(self.path)
        self.item = self.s.add({'kind':'phrase', 'title':'take issue with', 'meaning':'提出异议', 'body':'用法说明', 'source':'test'})
        self.t = datetime(2026, 9, 14, 12, tzinfo=timezone.utc)

    def tearDown(self):
        self.temp.cleanup()

    def test_learning_survives_restart_and_modes_are_separate(self):
        self.s.record(self.item['id'], 'understand', 'learn', 'one', at=self.t)
        item = Store(self.path).get(self.item['id'])
        self.assertEqual(len(item['progress']), 1)
        self.assertEqual(item['progress'][0]['mode'], 'understand')
        self.assertEqual(item['progress'][0]['due'], (self.t + timedelta(days=1)).isoformat())
        self.assertEqual(len(self.s.due(at=self.t)), 0)
        self.assertEqual(len(self.s.due(at=self.t+timedelta(days=1))), 1)

    def test_idempotency_and_undo_restore_previous_schedule(self):
        first = self.s.record(self.item['id'],'understand','learn','same',at=self.t)
        self.s.record(self.item['id'],'understand','learn','same',at=self.t)
        self.assertEqual(len(self.s.get(self.item['id'])['events']),1)
        review = self.s.record(self.item['id'],'understand','review','second',rating='forgot',answer='我忘了',at=self.t+timedelta(days=1))
        self.assertEqual(self.s.get(self.item['id'])['events'][0]['answer'],'我忘了')
        self.s.undo(review['event_id'])
        self.assertEqual(self.s.get(self.item['id'])['progress'][0]['due'],(self.t+timedelta(days=1)).isoformat())
        self.s.undo(first['event_id'])
        self.assertEqual(self.s.get(self.item['id'])['progress'],[])

    def test_undo_old_event_rejected_and_invalid_values_do_not_write(self):
        first=self.s.record(self.item['id'],'understand','learn','a',at=self.t)
        self.s.record(self.item['id'],'understand','review','b',rating='good',at=self.t)
        with self.assertRaises(ValueError): self.s.undo(first['event_id'])
        with self.assertRaises(ValueError): self.s.record(self.item['id'],'wrong','learn','c')
        with self.assertRaises(ValueError): self.s.record(self.item['id'],'understand','review','d',rating='wrong')

    def test_import_dedup_preserves_distinct_senses_and_backup(self):
        a=self.s.add({'kind':'word','title':'charge','meaning':'收费'})
        b=self.s.add({'kind':'word','title':'Charge','meaning':'收费'})
        c=self.s.add({'kind':'word','title':'charge','meaning':'指控'})
        self.assertEqual(a['id'],b['id']);self.assertNotEqual(a['id'],c['id'])
        preview=self.s.preview('charge\t收费\ncharge\t指控\nnew phrase\t新词组','word')
        self.assertEqual([x['exists'] for x in preview],[True,True,False])
        backup=self.s.backup()
        self.assertTrue(Path(backup).exists())
        self.assertEqual(len(Store(Path(backup)).list_items()),3)

    def test_sync_is_repeatable_and_does_not_reset_progress(self):
        docs=[{'id':'book/test.md','body':'# 测试\n\n## 1. assume：假定\n\n**常用搭配**：assume responsibility（承担责任）；assume control（接管）。\n\n**例句 1**：I assumed it was true.\n\n我以为这是真的。\n\n## 参考答案\n答案'}]
        self.s.sync(docs);before=self.s.list_items()
        self.s.sync(docs);self.assertEqual(len(before),len(self.s.list_items()))
        word=next(x for x in before if x['title']=='assume')
        self.s.record(word['id'],'understand','learn','seed')
        self.s.sync(docs)
        self.assertEqual(len(self.s.get(word['id'])['progress']),1)

    def test_concurrent_duplicate_submission_is_one_event(self):
        def submit(_):
            return self.s.record(self.item['id'],'understand','learn','concurrent',at=self.t)
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(submit,range(4)))
        self.assertEqual(len(self.s.get(self.item['id'])['events']),1)

    def test_invalid_import_is_atomic_and_backup_preserves_events(self):
        with self.assertRaises(ValueError):
            self.s.confirm([{'kind':'word','title':'valid'},{'kind':'bad','title':'invalid'}])
        self.assertEqual(len(self.s.list_items()),1)
        self.s.record(self.item['id'],'express','learn','backup-event',answer='My own answer',at=self.t)
        backup=Store(self.s.backup()).get(self.item['id'])
        self.assertEqual(backup['events'][0]['answer'],'My own answer')
        self.assertEqual(backup['progress'][0]['mode'],'express')


if __name__=='__main__':unittest.main()
