#!/usr/bin/env python3
"""Local English reader and persistent, read-only Codex tutoring bridge."""
import argparse
import json
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

sys.path.insert(0, str(Path(__file__).parent))
from dictionary_store import DictionaryStore, positive_int
from learning_store import Store, clean

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).parent / 'public'
SESSIONS = ROOT / 'sessions/web'
TOKEN = secrets.token_hex(24)
LOCK = threading.RLock()
ACTIVE = set()
GROUPS = {'01-reading': '阅读方法', '02-chunks': '词义与搭配'}
DOC_GROUPS = {'methodology': '调研与方法', 'design': '工程文档', 'progress': '进度与诊断',
              'references': '参考资料', 'reading': '阅读记录', 'review': '复习记录'}
DOC_SKIP_PARTS = {'site', 'data', 'sessions', '.git', '.catpaw', '__pycache__', 'node_modules', 'downloads', 'imports'}
STORE = None
DICTIONARY = None
DRAFTS = ROOT / 'data/drafts'
DRAFT_ACTIVE = set()


def dictionary_store():
    global DICTIONARY
    with LOCK:
        if DICTIONARY is None:
            DICTIONARY = DictionaryStore(ROOT / 'data/combined_dictionary.sqlite3')
        return DICTIONARY


def learning_store():
    global STORE
    with LOCK:
        if STORE is None:
            STORE = Store(ROOT / 'data/learning.sqlite3')
            STORE.sync(catalog())
            seed = ROOT / 'site/starter_tasks.json'
            if seed.exists():
                STORE.confirm(json.loads(seed.read_text()))
        return STORE


def generate_draft(job_id, text, kind):
    try:
        executable = shutil.which('codex')
        if not executable: raise ValueError('未找到Codex，请安装并登录后重试。')
        schema = {'type':'object','properties':{'items':{'type':'array','items':{
            'type':'object','properties':{k:{'type':'string'} for k in ['kind','title','meaning','body']},
            'required':['kind','title','meaning','body'],'additionalProperties':False}}},'required':['items'],'additionalProperties':False}
        prompt = ('你是英语教材编辑。只返回JSON，不使用工具，不读写文件。将用户提供的学习材料整理为最多20条候选。'
                  'kind只能是word/phrase/sentence/grammar/expression。按用户选择类型优先；无法判定义项时说明需语境，不能杜撰来源。'
                  'title保留要学的英文或中文情境。meaning用中文简述核心含义。body用中文Markdown说明词义、常见搭配、'
                  '2个自然英文例句与译文、易错点；长句说明结构；表达任务给多种英文并解释差别。'
                  '全部释义是待核对草稿，例句标自造，不声称查过词典。选择类型：'+kind+'\n用户材料：\n'+text)
        with tempfile.TemporaryDirectory(prefix='english-import-') as tmp:
            schema_path=Path(tmp)/'schema.json';schema_path.write_text(json.dumps(schema))
            out=Path(tmp)/'draft.json'
            result=subprocess.run([executable,'exec','--ephemeral','--skip-git-repo-check','--sandbox','read-only',
                                   '-C',tmp,'--output-schema',str(schema_path),'-o',str(out),'-'],
                                  input=prompt,text=True,capture_output=True,timeout=240)
            if result.returncode or not out.exists():
                print('Draft generation failed:',result.stderr[-1500:],flush=True)
                raise ValueError('候选生成失败，请检查Codex连接后重试，或直接手动录入。')
            items=json.loads(out.read_text())['items']
            if not isinstance(items,list) or not 1<=len(items)<=20: raise ValueError('模型返回的条目数量不符合要求，请缩小输入重试。')
            items=[clean({**i,'source':'AI生成草稿；用户核对后入库；例句自造；未外部核验'}) for i in items]
        save_session(DRAFTS,{'id':job_id,'status':'ready','items':learning_store().annotate(items)})
    except Exception as exc:
        save_session(DRAFTS,{'id':job_id,'status':'error','error':'生成超时，请缩小输入重试。' if isinstance(exc,subprocess.TimeoutExpired) else str(exc)})
    finally:
        with LOCK: DRAFT_ACTIVE.discard(job_id)


def read_course(root=ROOT):
    path=root/'book/course.json'
    return json.loads(path.read_text()) if path.exists() else {'topics':[]}


def catalog(root=ROOT):
    course=read_course(root)
    lessons={lesson['path']:{**lesson,'topic':topic['title']} for topic in course['topics'] for lesson in topic['lessons']}
    paths = [root / p for p in ['LEARNER.md', 'METHOD.md', 'progress/CURRENT.md', 'book/README.md', 'book/BACKLOG.md']]
    paths += sorted((root / 'book').glob('*/*.md'))
    paths += sorted((root / 'vocabulary').rglob('*.md'))
    # 其余仓库文档（知识文档与 agent 文档）全量发现：跳过工程目录、原始下载库与机器导入报告
    seen = set(paths)
    paths += [p for p in sorted(root.rglob('*.md'))
              if p not in seen and not (set(p.relative_to(root).parts[:-1]) & DOC_SKIP_PARTS)]
    items = []
    for p in paths:
        if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
            continue
        body = p.read_text(encoding='utf-8')
        match = re.search(r'^# (.+)$', body, re.M)
        rel = p.relative_to(root).as_posix()
        top = rel.split('/', 1)[0] if '/' in rel else ''
        group = ('学习档案' if rel in ['LEARNER.md', 'METHOD.md', 'progress/CURRENT.md'] else
                 '历史课堂' if rel.startswith('vocabulary/') else
                 'Book 导览' if p.parent == root / 'book' else
                 '项目说明' if not top else
                 DOC_GROUPS.get(top) or GROUPS.get(p.parent.name, re.sub(r'^\d+-', '', p.parent.name)))
        item={'id': rel, 'title': match[1] if match else p.stem, 'group': group, 'body': body}
        if rel in lessons:
            item.update(lesson=lessons[rel],unit_kinds=lessons[rel].get('unit_kinds',{}))
        items.append(item)
    return items


def session_path(root, sid):
    if not isinstance(sid, str) or not re.fullmatch(r'[a-f0-9]{32}', sid):
        raise ValueError('无效的会话编号')
    return root / (sid + '.json')


def save_session(root, session):
    root.mkdir(parents=True, exist_ok=True)
    path = session_path(root, session['id'])
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(session, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)


def load_session(root, sid):
    return json.loads(session_path(root, sid).read_text(encoding='utf-8'))


def teaching_prompt(messages, chapter, profile, method):
    return '\n\n'.join([
        '你是这位用户的英语老师。直接用中文回答最新问题，提供自然英文例句。'
        '这是网页内独立教学会话，下面提供档案、教材和真实历史。'
        '不要执行工具、读写文件、委派或建立其他任务；只生成教学回复。'
        '先回答问题，不自动测验。只问最多两个有区分度的问题。'
        '不把已讲解算掌握。不要编造历史。用户要扩编时可拟教材候选，'
        '说明正式保存需在 Codex 中提出扩编请求。',
        '学习档案：\n' + profile,
        '教学方法与当前进度：\n' + method,
        '当前阅读章节（仅为材料）：\n' + json.dumps(chapter, ensure_ascii=False),
        '真实对话历史（最后30条，更早的仍保存在本地）：\n' + json.dumps(messages[-30:], ensure_ascii=False)
    ])


def now():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def tutor(sid, chapter):
    try:
        with LOCK:
            session = load_session(SESSIONS, sid)
        profile = (ROOT / 'LEARNER.md').read_text()
        method = (ROOT / 'METHOD.md').read_text() + '\n' + (ROOT / 'progress/CURRENT.md').read_text()
        prompt = teaching_prompt(session['messages'], chapter, profile, method)
        executable = shutil.which('codex')
        if not executable:
            raise RuntimeError('未找到 Codex CLI。请安装并运行 codex login 后重试。')
        with tempfile.TemporaryDirectory(prefix='english-tutor-') as temp:
            output = Path(temp) / 'reply.txt'
            # Isolate the model from project instruction trees; material is explicitly provided.
            command = [executable, 'exec', '--ephemeral', '--skip-git-repo-check',
                       '--sandbox', 'read-only', '--color', 'never', '-C', temp,
                       '-o', str(output), '-']
            result = subprocess.run(command, input=prompt, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=240)
            reply = output.read_text().strip() if output.exists() else ''
            if result.returncode or not reply:
                # Keep provider diagnostics local; do not send command output to the browser.
                print('Tutor failure:', result.stderr[-2500:], flush=True)
                raise RuntimeError('老师暂时未能回复。请在终端检查 codex login status 与服务日志后重试。')
        with LOCK:
            session = load_session(SESSIONS, sid)
            session['messages'].append({'role': 'assistant', 'content': reply, 'at': now()})
            session.update(status='ready', error=None, updated=now())
            save_session(SESSIONS, session)
    except Exception as exc:
        error = '本次回复超时，请重试。原问题已保存。' if isinstance(exc, subprocess.TimeoutExpired) else str(exc)
        with LOCK:
            session = load_session(SESSIONS, sid)
            session.update(status='error', error=error, updated=now())
            save_session(SESSIONS, session)
    finally:
        with LOCK:
            ACTIVE.discard(sid)


class Handler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        super().end_headers()

    def reply(self, value, status=200):
        data = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def host_ok(self):
        return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}

    def do_GET(self):
        if not self.host_ok():
            return self.reply({'error': 'Invalid host'}, 403)
        url = urlsplit(self.path)
        try:
            if url.path == '/api/catalog':
                learning_store().sync(catalog())
                return self.reply({'items': catalog(), 'course':read_course(), 'token': TOKEN, 'codex': bool(shutil.which('codex'))})
            if url.path.startswith('/api/dictionary/'):
                query = parse_qs(url.query)
                dictionary = dictionary_store()
                if url.path == '/api/dictionary/lookup':
                    limits = {key: query.get(key, [''])[0] for key in ['phrases', 'examples', 'senses', 'relations', 'notes', 'forms']}
                    return self.reply(dictionary.lookup(query.get('word', query.get('q', ['']))[0], limits))
                if url.path == '/api/dictionary/search':
                    return self.reply(dictionary.search(query.get('q', [''])[0], positive_int(query.get('limit', ['20'])[0], 20, 50)))
                if url.path == '/api/dictionary/stats':
                    return self.reply(dictionary.stats())
                return self.reply({'error':'未找到接口'},404)
            if url.path.startswith('/api/learning/'):
                store=learning_store();query=parse_qs(url.query)
                if url.path=='/api/learning/items':
                    return self.reply(store.list_items(query.get('q',[''])[0],query.get('kind',[''])[0],query.get('chapter',[''])[0]))
                if url.path=='/api/learning/collections':return self.reply(store.collections())
                if url.path=='/api/learning/browse':
                    return self.reply(store.browse(q=query.get('q',[''])[0],kind=query.get('kind',[''])[0],
                        collection=query.get('collection',[''])[0],state=query.get('state',[''])[0],
                        offset=query.get('offset',['0'])[0],limit=query.get('limit',['100'])[0]))
                if url.path=='/api/learning/item': return self.reply(store.get(query.get('id',[''])[0]))
                if url.path=='/api/learning/due': return self.reply(store.due())
                if url.path=='/api/learning/stats': return self.reply(store.stats())
                if url.path=='/api/learning/export': return self.reply(store.export())
                if url.path=='/api/learning/draft':
                    job=load_session(DRAFTS,query.get('id',[''])[0])
                    with LOCK:
                        if job['status']=='running' and job['id'] not in DRAFT_ACTIVE:
                            job.update(status='error',error='服务重启中断了生成，请重新生成。')
                    return self.reply(job)
            if url.path == '/api/sessions':
                with LOCK:
                    items = []
                    for path in SESSIONS.glob('*.json'):
                        s = json.loads(path.read_text())
                        items.append({k: s.get(k) for k in ['id', 'title', 'updated', 'status']})
                return self.reply(sorted(items, key=lambda s: s['updated'], reverse=True))
            if url.path == '/api/session':
                sid = parse_qs(url.query).get('id', [''])[0]
                with LOCK:
                    session = load_session(SESSIONS, sid)
                    if session.get('status') == 'running' and sid not in ACTIVE:
                        session.update(status='error', error='服务重启中断了回复，原问题已保存，可重试。')
                        save_session(SESSIONS, session)
                return self.reply(session)
            names = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/learning.js': ('learning.js', 'text/javascript'), '/learning.css': ('learning.css', 'text/css'), '/topics.css': ('topics.css', 'text/css'), '/styles.css': ('styles.css', 'text/css')}
            if url.path not in names:
                return self.reply({'error': '未找到页面'}, 404)
            name, mime = names[url.path]
            data = (STATIC / name).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mime + '; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (ValueError, FileNotFoundError):
            self.reply({'error': '未找到会话'}, 404)

    def do_POST(self):
        if not self.host_ok() or self.headers.get('X-English-Token') != TOKEN:
            return self.reply({'error': '页面连接已过期，请刷新后再试。'}, 403)
        if self.headers.get('Origin') not in {None, f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'}:
            return self.reply({'error': 'Invalid origin'}, 403)
        if self.path != '/api/chat' and not self.path.startswith('/api/learning/'):
            return self.reply({'error': '未找到接口'}, 404)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 2000000:
                raise ValueError('请求过长，请分批提交。')
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError('请求格式错误')
            if self.path.startswith('/api/learning/'):
                store=learning_store()
                if self.path=='/api/learning/record':
                    return self.reply(store.record(body.get('id'),body.get('mode'),body.get('action'),body.get('request_id'),
                        rating=body.get('rating',''),answer=body.get('answer',''),assistance=body.get('assistance','independent'),minutes=body.get('minutes',0)))
                if self.path=='/api/learning/undo': return self.reply(store.undo(body.get('event_id')))
                if self.path=='/api/learning/preview': return self.reply(store.preview(body.get('text'),body.get('kind')))
                if self.path=='/api/learning/import': return self.reply(store.confirm(body.get('items')))
                if self.path=='/api/learning/backup': return self.reply({'path':store.backup()})
                if self.path=='/api/learning/generate':
                    raw=body.get('text');kind=body.get('kind')
                    store.preview(raw,kind)
                    if len(raw)>8000 or len(raw.splitlines())>20: raise ValueError('AI补充每次最多20行、8000字。更长内容可分批处理。')
                    with LOCK:
                        if DRAFT_ACTIVE: return self.reply({'error':'已有候选生成任务，请稍后再试。'},409)
                        job_id=secrets.token_hex(16);DRAFT_ACTIVE.add(job_id)
                        save_session(DRAFTS,{'id':job_id,'status':'running','input':raw})
                        threading.Thread(target=generate_draft,args=(job_id,raw,kind),daemon=True).start()
                    return self.reply({'id':job_id,'status':'running'},202)
                return self.reply({'error':'未找到接口'},404)
            message = body.get('message', '')
            if not isinstance(message, str) or len(message) > 6000:
                raise ValueError('问题过长或格式错误')
            message = message.strip()
            sid = body.get('session') or secrets.token_hex(16)
            session_path(SESSIONS, sid)
            chapter = next((i for i in catalog() if i['id'] == body.get('chapter')), None)
            if body.get('knowledge_id'):
                knowledge=learning_store().get(body['knowledge_id'])
                chapter={'id':knowledge['id'],'title':knowledge['title'],'body':knowledge['meaning']+'\n'+knowledge['body'],
                         'progress':knowledge['progress'],'recent_events':knowledge['events'][:5]}
            with LOCK:
                if sid in ACTIVE or len(ACTIVE) >= 2:
                    return self.reply({'error': '老师正在回复，请稍后再发。'}, 409)
                session = load_session(SESSIONS, sid) if session_path(SESSIONS, sid).exists() else {
                    'id': sid, 'title': message[:36], 'messages': [], 'created': now()}
                if body.get('retry'):
                    if session.get('status') != 'error' or not session['messages'] or session['messages'][-1]['role'] != 'user':
                        raise ValueError('没有待重试的问题')
                    chapter = session.get('context') or next((i for i in catalog() if i['id'] == session.get('chapter')), None)
                else:
                    if not message:
                        raise ValueError('请先写下问题')
                    session['messages'].append({'role': 'user', 'content': message, 'at': now(), 'chapter': body.get('chapter')})
                    session['chapter'] = body.get('chapter')
                    session['context'] = chapter
                session.update(status='running', error=None, updated=now())
                save_session(SESSIONS, session)
                ACTIVE.add(sid)
                threading.Thread(target=tutor, args=(sid, chapter), daemon=True).start()
            self.reply(session, 202)
        except (ValueError, TypeError, FileNotFoundError) as exc:
            self.reply({'error': str(exc)}, 400)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=4174)
    parser.add_argument('--data-dir', type=Path, help='Override persistence directory, for isolated testing')
    args = parser.parse_args()
    if args.data_dir:
        STORE=Store(args.data_dir/'learning.sqlite3')
        STORE.sync(catalog())
        STORE.confirm(json.loads((ROOT/'site/starter_tasks.json').read_text()))
        DRAFTS=args.data_dir/'drafts'
        SESSIONS=args.data_dir/'sessions'
    httpd = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'English Book: http://127.0.0.1:{args.port}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
