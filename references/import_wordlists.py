#!/usr/bin/env python3
"""Reproducible local import from downloaded, hashed vocabulary snapshots."""
import argparse
from collections import OrderedDict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'site'))
from learning_store import Store, normal

DOWNLOADS=ROOT/'references/downloads'
SPECS=[('cet4','四级词汇','CET4-rich.jsonl','四级'),('cet6','六级词汇','CET6-rich.jsonl','六级'),('tem8','专八词汇','TEM8-rich.jsonl','专八')]

def unique(values):return list(dict.fromkeys(x.strip() for x in values if isinstance(x,str) and x.strip()))

def text(value):return str(value or '').strip()

def build():
    ngsl=json.loads((DOWNLOADS/'NGSL-1.2-community.json').read_text())
    core={normal(r['name']) for r in ngsl}
    assert len(core)==2809, 'NGSL snapshot has unexpected unique count'
    batches=[];report={};manifest=[]
    for cid,label,filename,chinese in SPECS:
        path=DOWNLOADS/filename
        rows=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        source='https://github.com/KyleBing/english-vocabulary/blob/master/full_line_jsonl/sentence/正序/'+chinese+'.jsonl'
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        meta={'id':cid,'title':label+' · 社区整理','source_url':source,'sha256':digest,'file':str(path.relative_to(ROOT)),
              'download_url':'https://cdn.jsdelivr.net/gh/KyleBing/english-vocabulary@master/full_line_jsonl/sentence/正序/'+chinese+'.jsonl',
              'description':'上游合并了多个词书，非最新版官方大纲逐词核验。资料释义与例句未经逐条教学审校。按字母浏览，源顺序不是频率排名。',
              'license':'上游未列独立数据许可；保留原出处，不宣称拥有再分发授权。当前仅本机使用。',
              'downloaded_at':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat()}
        groups=OrderedDict();phrases=OrderedDict();raw_phrase_count=0;dropped_examples=0
        for row in rows:
            head=text(row.get('word'))
            if not head or len(head)>200:continue
            group=groups.setdefault(normal(head),{'title':head,'translations':[],'sentences':[],'phrases':[]})
            for tr in row.get('translations',[]):
                gloss=text(tr.get('translation'));pos=text(tr.get('type'))
                if gloss:group['translations'].append((pos+'. ' if pos else '')+gloss)
            for sentence in row.get('sentences',[]):
                en=text(sentence.get('sentence'));zh=text(sentence.get('translation'))
                if en.startswith(('...','…')) or zh.startswith(('...','…')) or len(en)>700:
                    dropped_examples+=1;continue
                if en:group['sentences'].append((en,zh))
            for phrase in row.get('phrases',[]):
                raw_phrase_count+=1;en=text(phrase.get('phrase'));zh=text(phrase.get('translation'))
                if not en or not zh:continue
                group['phrases'].append((en,zh))
                tokens=re.findall(r"[a-z]+(?:'[a-z]+)?",en.lower())
                # Select readable multiword material, not a fabricated frequency ranking.
                if not 2<=len(tokens)<=6 or not re.fullmatch(r"[A-Za-z][A-Za-z '\-’]+",en):continue
                if sum(t not in core for t in tokens)>1:continue
                key=(normal(en),normal(zh))
                p=phrases.setdefault(key,{'title':en,'meaning':zh,'parents':[]})
                p['parents'].append(head)
        records=[];example_count=0
        for group in groups.values():
            translations=unique(group['translations']);meaning='；'.join(translations)
            if not meaning:meaning='原资料未提供释义，待核对'
            examples=list(dict.fromkeys(group['sentences']))[:3];example_count+=len(examples)
            pairings=list(dict.fromkeys(group['phrases']))[:8]
            body='## 资料释义\n\n'+'\n\n'.join(translations)+'\n\n## 来源与范围\n\n'+meta['description']
            if normal(group['title'])=='internship':
                meaning='n. 实习；实习期；实习职位'
                body+='\n\n## 校订提示\n\n上游将internship译为“实习医师”，有把职位/经历与人混淆的风险。此处按Oxford释义校订；原文保留在上方。\n\n参考：https://www.oxfordlearnersdictionaries.com/definition/english/internship'
            if examples:
                body+='\n\n## 资料例句（未逐句审校）\n\n'+'\n\n'.join('> '+a+'\n\n'+b for a,b in examples)
            if pairings:
                body+='\n\n## 关联搭配（不等于必考词组）\n\n'+'\n'.join('- '+a+'：'+b for a,b in pairings)
            body+='\n\n出处：'+source
            records.append({'kind':'word','title':group['title'],'meaning':meaning,'body':body,'source':label+'社区资料；释义待结合语境核对'})
        batches.append((meta,records))
        phrase_meta={**meta,'id':cid+'-phrases','title':label.replace('词汇','')+'关联词组 · 筛选资料',
                     'description':'从该考试词目附带搭配中筛选2–6个词、至多1个词不在NGSL集合的条目。此规则筛阅读难度，不是词频排名，也不是官方必考词组。'}
        phrase_rows=[{'kind':'phrase','title':p['title'],'meaning':p['meaning'],
                      'body':'## 资料含义\n\n'+p['meaning']+'\n\n来自词目：'+', '.join(unique(p['parents']))+'\n\n'+phrase_meta['description']+'\n\n原资料没有该词组的独立例句；可请老师结合语境讲解，不自动套用母词例句。',
                      'source':phrase_meta['title']+'；未逐项审校'} for p in phrases.values()]
        batches.append((phrase_meta,phrase_rows))
        report[cid]={'raw_rows':len(rows),'unique_words':len(records),'raw_phrase_mentions':raw_phrase_count,
                     'selected_phrase_senses':len(phrase_rows),'kept_examples':example_count,'omitted_fragment_examples':dropped_examples}
        manifest.append(meta)
    path=DOWNLOADS/'NGSL-1.2-community.json'
    meta={'id':'ngsl-core','title':'NGSL 1.2 · 高频核心词','source_url':'https://github.com/zhghx/qwerty-learner/blob/0b29037/public/dicts/NGSL_1.2.json',
          'download_url':'https://cdn.jsdelivr.net/gh/zhghx/qwerty-learner@0b29037/public/dicts/NGSL_1.2.json',
          'official_url':'https://www.newgeneralservicelist.com/new-general-service-list',
          'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
          'description':'2809词社区镜像；原词表官方发布CC BY-SA 4.0。镜像加入了中英文解释，尚未与官方CSV逐项比对。顺序不是已核实词频，不能把前1000项称为频率前1000。',
          'license':'NGSL原词表：Browne/Culligan/Phillips，CC BY-SA 4.0；镜像释义来自社区，保留上游GPL与出处，不将原表许可自动扩展到所有解释。'}
    rows=[]
    for r in ngsl:
        glosses=unique(r.get('trans',[]));cn=[g for g in glosses if re.search(r'[\u4e00-\u9fff]',g)]
        meaning='；'.join(cn or glosses)
        rows.append({'kind':'word','title':r['name'],'meaning':meaning,'body':'## 社区镜像释义\n\n'+'\n\n'.join(glosses)+'\n\n'+meta['description']+'\n\n原词表作者：Browne, Culligan and Phillips。词次覆盖不等于理解率。','source':'NGSL 1.2社区镜像；不是AI本轮生成；释义待核对'})
    batches.append((meta,rows));manifest.append(meta);report['ngsl-core']={'unique_words':len(rows)}
    return batches,report,manifest

def main():
    p=argparse.ArgumentParser();p.add_argument('--database',type=Path,required=True);p.add_argument('--report-dir',type=Path,required=True);p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    batches,report,manifest=build();a.report_dir.mkdir(parents=True,exist_ok=True)
    # Validate every row before any write to the selected database.
    from learning_store import clean
    for meta,rows in batches:
        for row in rows:clean(row)
    result={'sources':report,'files':manifest,'dry_run':a.dry_run}
    if not a.dry_run:
        store=Store(a.database);result['backup']=store.backup();result['before']=store.stats()
        with store.db() as c:
            evidence_before={t:[tuple(r) for r in c.execute('SELECT * FROM '+t+' ORDER BY rowid')] for t in ['progress','events']}
        result['imports']=[store.import_collection(meta,rows) for meta,rows in batches]
        with store.db() as c:
            evidence_after={t:[tuple(r) for r in c.execute('SELECT * FROM '+t+' ORDER BY rowid')] for t in ['progress','events']}
            result['integrity']=c.execute('PRAGMA integrity_check').fetchone()[0]
        result['evidence_unchanged']=evidence_before==evidence_after
        result['after']=store.stats()
        result['collections']=store.collections()
        if not result['evidence_unchanged']:raise RuntimeError('学习记录在导入期间变化，请核查是否有同时发生的用户操作。')
    (a.report_dir/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k in ['sources','before','after','imports','integrity','evidence_unchanged']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
