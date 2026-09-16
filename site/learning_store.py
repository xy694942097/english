"""Durable knowledge, evidence and review scheduling. No model-generated SQL."""
import hashlib
import json
import re
import sqlite3
import unicodedata
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

KINDS = {'word', 'phrase', 'sentence', 'grammar', 'expression'}
MODES = {'understand', 'express'}
GAPS = [1, 3, 7, 14, 30, 60]


def utcnow():
    return datetime.now(timezone.utc)


def normal(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split()).strip(' .。')


def clean(payload):
    if not isinstance(payload, dict):
        raise ValueError('条目格式错误')
    result = {}
    for field, limit in [('title', 1000), ('meaning', 3000), ('body', 18000), ('source', 2000)]:
        value = payload.get(field, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f'{field} 内容过长或格式错误')
        result[field] = value.strip()
    result['kind'] = payload.get('kind', 'phrase')
    if result['kind'] not in KINDS or not result['title']:
        raise ValueError('请选择有效类型并填写学习内容')
    key = '|'.join([result['kind'], normal(result['title']), normal(result['meaning'])])
    result['id'] = hashlib.sha256(key.encode()).hexdigest()[:24]
    return result


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.db() as c:
            version=c.execute('PRAGMA user_version').fetchone()[0]
            if version>2:
                raise ValueError('数据库版本比当前程序新，请使用较新的程序打开。')
            if version==1:self.backup()
            c.executescript('''
              CREATE TABLE IF NOT EXISTS items(
                id TEXT PRIMARY KEY,kind TEXT NOT NULL,title TEXT NOT NULL,
                meaning TEXT NOT NULL,body TEXT NOT NULL,source TEXT NOT NULL,created TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS links(item_id TEXT REFERENCES items(id),chapter TEXT,
                PRIMARY KEY(item_id,chapter));
              CREATE TABLE IF NOT EXISTS progress(
                item_id TEXT REFERENCES items(id),mode TEXT,stage INTEGER,due TEXT,updated TEXT,
                PRIMARY KEY(item_id,mode));
              CREATE TABLE IF NOT EXISTS events(
                id TEXT PRIMARY KEY,item_id TEXT REFERENCES items(id),mode TEXT,action TEXT,
                rating TEXT,answer TEXT,assistance TEXT,minutes INTEGER,at TEXT,
                previous TEXT,current TEXT,undone INTEGER DEFAULT 0);
              CREATE INDEX IF NOT EXISTS due_index ON progress(due);
              CREATE INDEX IF NOT EXISTS events_item ON events(item_id,at);
              CREATE TABLE IF NOT EXISTS collections(id TEXT PRIMARY KEY,title TEXT NOT NULL,metadata TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS collection_items(
                collection_id TEXT REFERENCES collections(id),item_id TEXT REFERENCES items(id),
                position INTEGER,body TEXT,PRIMARY KEY(collection_id,item_id));
              CREATE INDEX IF NOT EXISTS collection_item_lookup ON collection_items(item_id);
              CREATE TABLE IF NOT EXISTS catalog_heads(title_key TEXT PRIMARY KEY,item_id TEXT REFERENCES items(id));
              PRAGMA user_version=2;
            ''')

    @contextmanager
    def db(self):
        c = sqlite3.connect(self.path, timeout=15)
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON')
        try:
            with c:
                yield c
        finally:
            c.close()

    def _add(self, c, p, chapter=None, refresh=False):
        c.execute('INSERT OR IGNORE INTO items VALUES(?,?,?,?,?,?,?)',
                  (p['id'],p['kind'],p['title'],p['meaning'],p['body'],p['source'],utcnow().isoformat()))
        if refresh:
            c.execute('UPDATE items SET body=?,source=? WHERE id=?', (p['body'],p['source'],p['id']))
        if chapter:
            c.execute('INSERT OR IGNORE INTO links VALUES(?,?)', (p['id'],chapter))
        return p['id']

    def add(self, payload):
        p = clean(payload)
        with self.db() as c:
            self._add(c,p)
        return self.get(p['id'])

    def get(self, item_id):
        with self.db() as c:
            row=c.execute('SELECT * FROM items WHERE id=?',(item_id,)).fetchone()
            if not row: raise ValueError('知识点不存在')
            result=dict(row)
            result['chapters']=[r[0] for r in c.execute('SELECT chapter FROM links WHERE item_id=?',(item_id,))]
            result['progress']=[dict(r) for r in c.execute('SELECT * FROM progress WHERE item_id=?',(item_id,))]
            result['events']=[dict(r) for r in c.execute('SELECT rowid,* FROM events WHERE item_id=? ORDER BY rowid DESC LIMIT 100',(item_id,))]
            result['collections']=[dict(r) for r in c.execute('SELECT c.id,c.title,c.metadata,m.body FROM collections c JOIN collection_items m ON m.collection_id=c.id WHERE m.item_id=?',(item_id,))]
            return result

    def collections(self):
        with self.db() as c:
            return [dict(r) for r in c.execute('SELECT c.id,c.title,c.metadata,count(m.item_id) AS count FROM collections c LEFT JOIN collection_items m ON c.id=m.collection_id GROUP BY c.id ORDER BY c.id')]

    def browse(self, q='', kind='', collection='', state='', offset=0, limit=100):
        offset=max(0,int(offset));limit=min(100,max(1,int(limit)))
        clauses=[];params=[]
        if q:
            clauses.append('(i.title LIKE ? ESCAPE \'\\\' OR i.meaning LIKE ? ESCAPE \'\\\')')
            term=q.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')
            params+=['%'+term+'%']*2
        if kind:clauses.append('i.kind=?');params.append(kind)
        if collection:
            clauses.append('EXISTS(SELECT 1 FROM collection_items m WHERE m.item_id=i.id AND m.collection_id=?)');params.append(collection)
        if state=='new':clauses.append('NOT EXISTS(SELECT 1 FROM progress p WHERE p.item_id=i.id)')
        elif state=='studied':clauses.append('EXISTS(SELECT 1 FROM progress p WHERE p.item_id=i.id)')
        where=' WHERE '+' AND '.join(clauses) if clauses else ''
        with self.db() as c:
            total=c.execute('SELECT count(*) FROM items i'+where,params).fetchone()[0]
            rows=[dict(r) for r in c.execute('SELECT i.id,i.kind,i.title,i.meaning,i.source,(SELECT count(*) FROM progress p WHERE p.item_id=i.id) AS learned_modes FROM items i'+where+' ORDER BY i.title COLLATE NOCASE,i.id LIMIT ? OFFSET ?',params+[limit,offset])]
        return {'total':total,'items':rows,'offset':offset,'limit':limit}

    def import_collection(self, metadata, rows):
        cid=metadata.get('id','')
        if not re.fullmatch(r'[a-z0-9-]{1,80}',cid) or not metadata.get('title'):
            raise ValueError('无效的词表标识')
        prepared=[clean(r) for r in rows]
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            before=c.execute('SELECT count(*) FROM items').fetchone()[0]
            c.execute('INSERT INTO collections VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,metadata=excluded.metadata',
                      (cid,metadata['title'],json.dumps(metadata,ensure_ascii=False)))
            heads={r['title_key']:r['item_id'] for r in c.execute('SELECT * FROM catalog_heads')}
            book_heads={normal(r['title']):r['id'] for r in c.execute("SELECT id,title FROM items WHERE kind='word' AND source LIKE 'Book教学材料%'")}
            for position,p in enumerate(prepared,1):
                target=None
                if p['kind']=='word':
                    key=normal(p['title'])
                    target=heads.get(key) or book_heads.get(key)
                if not target:target=self._add(c,p)
                if p['kind']=='word':
                    heads[key]=target
                    c.execute('INSERT OR IGNORE INTO catalog_heads VALUES(?,?)',(key,target))
                c.execute('INSERT INTO collection_items VALUES(?,?,?,?) ON CONFLICT(collection_id,item_id) DO UPDATE SET body=excluded.body,position=excluded.position',
                          (cid,target,position,p['body']))
            after=c.execute('SELECT count(*) FROM items').fetchone()[0]
            count=c.execute('SELECT count(*) FROM collection_items WHERE collection_id=?',(cid,)).fetchone()[0]
        return {'collection':cid,'input':len(prepared),'members':count,'added':after-before}

    def list_items(self, q='', kind='', chapter=''):
        with self.db() as c:
            sql='SELECT i.*, (SELECT count(*) FROM progress p WHERE p.item_id=i.id) AS learned_modes FROM items i WHERE 1=1'
            params=[]
            if q:
                sql+=' AND (i.title LIKE ? OR i.meaning LIKE ?)';params += ['%'+q+'%']*2
            if kind:
                sql+=' AND i.kind=?';params.append(kind)
            if chapter:
                sql+=' AND EXISTS(SELECT 1 FROM links l WHERE l.item_id=i.id AND l.chapter=?)';params.append(chapter)
            return [dict(r) for r in c.execute(sql+' ORDER BY i.title COLLATE NOCASE,i.meaning',params)]

    def due(self, at=None):
        stamp=(at or utcnow()).isoformat()
        with self.db() as c:
            return [dict(r) for r in c.execute('SELECT i.*,p.mode,p.stage,p.due FROM progress p JOIN items i ON i.id=p.item_id WHERE p.due<=? ORDER BY p.due,i.title',(stamp,))]

    def stats(self):
        with self.db() as c:
            return {'items':c.execute('SELECT count(*) FROM items').fetchone()[0],
                    'studied':c.execute('SELECT count(DISTINCT item_id) FROM progress').fetchone()[0],
                    'due':c.execute('SELECT count(*) FROM progress WHERE due<=?',(utcnow().isoformat(),)).fetchone()[0],
                    'minutes':c.execute('SELECT coalesce(sum(minutes),0) FROM events WHERE undone=0').fetchone()[0]}

    def record(self, item_id, mode, action, request_id, rating='', answer='', assistance='independent', minutes=0, at=None):
        if mode not in MODES or action not in {'learn','review'}:
            raise ValueError('无效的学习操作')
        if action=='review' and rating not in {'forgot','hard','good'}:
            raise ValueError('请选择忘了、费力或顺利')
        if not isinstance(request_id,str) or not 1<=len(request_id)<=100:
            raise ValueError('缺少操作编号')
        if not isinstance(answer,str) or len(answer)>12000 or assistance not in {'independent','hint','lookup'}:
            raise ValueError('回答或提示类型无效')
        if not isinstance(minutes,int) or isinstance(minutes,bool) or not 0<=minutes<=240:
            raise ValueError('学习分钟数应为0到240')
        time=(at or utcnow());stamp=time.isoformat()
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            existing=c.execute('SELECT * FROM events WHERE id=?',(request_id,)).fetchone()
            if existing:
                if (existing['item_id'],existing['mode'],existing['action'])!=(item_id,mode,action):
                    raise ValueError('操作编号已用于另一请求')
                return {'event_id':existing['id'],'duplicate':True}
            if not c.execute('SELECT id FROM items WHERE id=?',(item_id,)).fetchone():
                raise ValueError('知识点不存在')
            prev=c.execute('SELECT * FROM progress WHERE item_id=? AND mode=?',(item_id,mode)).fetchone()
            prev=dict(prev) if prev else None
            if action=='learn' and prev: raise ValueError('这个方向已学习，请进入复习或撤销上次记录')
            if action=='review' and not prev: raise ValueError('请先完成首次学习')
            stage=prev['stage'] if prev else 0
            if action=='learn': delta=timedelta(days=1)
            elif rating=='forgot': stage=-1;delta=timedelta(minutes=10)
            elif rating=='hard': delta=timedelta(days=max(1,GAPS[max(stage,0)]/2))
            else: stage=min(stage+1,len(GAPS)-1);delta=timedelta(days=GAPS[stage])
            curr={'item_id':item_id,'mode':mode,'stage':stage,'due':(time+delta).isoformat(),'updated':stamp}
            c.execute('INSERT OR REPLACE INTO progress VALUES(?,?,?,?,?)',tuple(curr.values()))
            c.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?,?,?,?,?,0)',
                      (request_id,item_id,mode,action,rating,answer,assistance,minutes,stamp,json.dumps(prev),json.dumps(curr)))
            return {'event_id':request_id,'progress':curr}

    def undo(self, event_id):
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            event=c.execute('SELECT rowid,* FROM events WHERE id=?',(event_id,)).fetchone()
            if not event: raise ValueError('记录不存在')
            if event['undone']: return {'undone':True}
            newer=c.execute('SELECT id FROM events WHERE item_id=? AND mode=? AND rowid>? AND undone=0',
                            (event['item_id'],event['mode'],event['rowid'])).fetchone()
            if newer: raise ValueError('请先撤销这个学习方向更晚的记录')
            previous=json.loads(event['previous'])
            c.execute('DELETE FROM progress WHERE item_id=? AND mode=?',(event['item_id'],event['mode']))
            if previous:
                c.execute('INSERT INTO progress VALUES(?,?,?,?,?)',tuple(previous[k] for k in ['item_id','mode','stage','due','updated']))
            c.execute('UPDATE events SET undone=1 WHERE id=?',(event_id,))
            return {'undone':True}

    def preview(self, text, kind):
        if not isinstance(text,str) or len(text)>30000 or kind not in KINDS:
            raise ValueError('请输入不超过30000字的内容并选择类型')
        lines=[s.strip() for s in text.splitlines() if s.strip()]
        if not lines or len(lines)>100: raise ValueError('每次请录入1到100行')
        candidates=[];seen=set()
        with self.db() as c:
            for line in lines:
                line=re.sub(r'^\s*(?:[-*•]|\d+[.)、])\s*','',line)
                parts=re.split(r'\t|\s+—\s+|\s*＝\s*',line,maxsplit=1)
                p=clean({'kind':kind,'title':parts[0],'meaning':parts[1] if len(parts)>1 else '', 'source':'用户录入，未外部核验'})
                if p['id'] in seen: continue
                seen.add(p['id'])
                p['exists']=bool(c.execute('SELECT id FROM items WHERE id=?',(p['id'],)).fetchone())
                p['related']=[dict(r) for r in c.execute('SELECT id,title,meaning,kind FROM items WHERE lower(title)=lower(?) LIMIT 6',(p['title'],))]
                candidates.append(p)
        return candidates

    def annotate(self, rows):
        candidates=[clean(r) for r in rows]
        with self.db() as c:
            for p in candidates:
                p['exists']=bool(c.execute('SELECT id FROM items WHERE id=?',(p['id'],)).fetchone())
                p['related']=[dict(r) for r in c.execute('SELECT id,title,meaning,kind FROM items WHERE lower(title)=lower(?) LIMIT 6',(p['title'],))]
        return candidates

    def confirm(self, rows):
        if not isinstance(rows,list) or not 1<=len(rows)<=100: raise ValueError('请选择1到100条候选')
        prepared=[clean(r) for r in rows]
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            before=c.execute('SELECT count(*) FROM items').fetchone()[0]
            ids=[self._add(c,p) for p in prepared]
            added=c.execute('SELECT count(*) FROM items').fetchone()[0]-before
        return {'ids':ids,'added':added,'existing':len(ids)-added}

    def sync(self, docs):
        with self.db() as c:
            for doc in docs:
                if not doc['id'].startswith('book/'): continue
                sections=re.split(r'^## ',doc['body'],flags=re.M)
                for section in sections[1:]:
                    heading,_,body=section.partition('\n')
                    match=re.match(r'(?:\d+\.\s*)?([A-Za-z][A-Za-z /.-]*?)[：·]',heading)
                    if not match: continue
                    title=match[1].strip();kind='phrase' if ' ' in title else 'word'
                    kind=doc.get('unit_kinds',{}).get(title,kind)
                    meaning=re.split(r'[：·]',heading,maxsplit=1)[1].strip()
                    p=clean({'kind':kind,'title':title,'meaning':meaning,'body':body.strip(), 'source':'Book教学材料；例句自造；'+doc['id']})
                    self._add(c,p,doc['id'],refresh=True)
                    for line in re.findall(r'^\*\*常用搭配\*\*：(.+)$',body,re.M):
                        for chunk in line.split('；'):
                            m=re.match(r'(.+?)（(.+?)）',chunk)
                            if not m: continue
                            phrase=clean({'kind':'phrase','title':m[1].strip(),'meaning':m[2],
                                          'body':f'来自词条 {title}。\n\n'+body.strip(),'source':p['source']})
                            self._add(c,phrase,doc['id'],refresh=True)

    def export(self):
        with self.db() as c:
            return {'schema':2,'exported':utcnow().isoformat(),**{t:[dict(r) for r in c.execute('SELECT * FROM '+t)] for t in ['items','links','progress','events','collections','collection_items','catalog_heads']}}

    def backup(self):
        folder=self.path.parent/'backups';folder.mkdir(exist_ok=True)
        path=folder/(utcnow().strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.sqlite3')
        with sqlite3.connect(self.path) as src, sqlite3.connect(path) as dst:
            src.backup(dst)
        return str(path)
