#!/usr/bin/env python3
"""Local markdown book: nav.json 显式登记目录，浏览器可编辑已登记文档。

用法:
    python3 server.py [--port 4174]

路由:
    /api/catalog     返回 nav.json 登记的全部文档（含正文与保存校验值）
    POST /api/document 仅保存已登记的 Markdown 文档
    /files/...       返回仓库内静态资源（markdown 里的相对路径图片等）
    其他             返回 public/ 下的静态文件
"""
import argparse
import hashlib
import json
import os
import re
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).parent / 'public'
SAVE_LOCK = threading.Lock()
MAX_DOCUMENT_BYTES = 8 * 1024 * 1024


class SaveError(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_nav(root=ROOT):
    path = root / 'nav.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'groups': []}


def read_aliases(root=ROOT):
    path = root / 'engineering/design/document-paths-2026-10-11.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def catalog(root=ROOT):
    """只收录 nav.json 登记的文档；标题取自正文一级标题。"""
    nav = read_nav(root)
    items = []
    for group in nav['groups'] + nav.get('maintenance', []):
        def walk(items_list, title):
            for it in items_list:
                if isinstance(it, str):
                    p = root / it
                    data = p.read_bytes()
                    body = data.decode('utf-8')
                    match = re.search(r'^# (.+)$', body, re.M)
                    items.append({'id': it, 'title': match[1] if match else p.stem,
                                  'group': title, 'body': body, 'sha256': digest(data)})
                else:
                    walk(it['items'], title)
        walk(group['items'], group['title'])
    return items


def registered_documents(root=ROOT):
    paths = set()
    nav = read_nav(root)
    for group in nav['groups'] + nav.get('maintenance', []):
        def walk(entries):
            for entry in entries:
                if isinstance(entry, str):
                    paths.add(entry)
                else:
                    walk(entry['items'])
        walk(group['items'])
    return paths


def save_document(doc_id, body, expected_sha256, root=ROOT):
    """仅写入 nav 登记的现有 .md，旧版本校验失败时绝不覆盖。"""
    if not isinstance(doc_id, str) or doc_id not in registered_documents(root) or not doc_id.endswith('.md'):
        raise SaveError('只能编辑目录中登记的 Markdown 文档', 404)
    if not isinstance(body, str) or not isinstance(expected_sha256, str) or not re.fullmatch(r'[a-f0-9]{64}', expected_sha256):
        raise SaveError('保存请求格式不正确', 400)
    data = body.encode('utf-8')
    if len(data) > MAX_DOCUMENT_BYTES:
        raise SaveError('文档超过 8 MB 上限', 413)
    path = (root / doc_id).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise SaveError('文档不存在或路径无效', 404)
    with SAVE_LOCK:
        previous = path.read_bytes()
        if digest(previous) != expected_sha256:
            raise SaveError('文件已在别处修改；请复制当前编辑内容后刷新页面', 409)
        if data != previous:
            temp_name = None
            try:
                with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.english-edit-', delete=False) as temp:
                    temp_name = temp.name
                    temp.write(data)
                    temp.flush()
                    os.fsync(temp.fileno())
                os.chmod(temp_name, path.stat().st_mode)
                os.replace(temp_name, path)
            finally:
                if temp_name and os.path.exists(temp_name):
                    os.unlink(temp_name)
    match = re.search(r'^# (.+)$', body, re.M)
    return {'id': doc_id, 'body': body, 'sha256': digest(data),
            'title': match[1] if match else path.stem}


def resolve_inside_root(rel):
    """把相对路径安全地解析到 ROOT 内，越界返回 None。"""
    p = (ROOT / unquote(rel)).resolve()
    if p != ROOT and not p.is_relative_to(ROOT):
        return None
    return p


class Handler(BaseHTTPRequestHandler):
    STATIC_ROUTES = {
        '/': ('index.html', 'text/html'),
        '/app.js': ('app.js', 'text/javascript'),
        '/styles.css': ('styles.css', 'text/css'),
        '/vendor/marked.min.js': ('vendor/marked.min.js', 'text/javascript'),
        '/vendor/highlight.min.js': ('vendor/highlight.min.js', 'text/javascript'),
        '/vendor/github-dark.min.css': ('vendor/github-dark.min.css', 'text/css'),
        '/vendor/toastui/editor-bundle.js': ('vendor/toastui/editor-bundle.js', 'text/javascript'),
        '/vendor/toastui/toastui-editor.css': ('vendor/toastui/toastui-editor.css', 'text/css'),
        '/vendor/toastui/toastui-editor-dark.css': ('vendor/toastui/toastui-editor-dark.css', 'text/css'),
        '/vendor/toastui/zh-cn.js': ('vendor/toastui/zh-cn.js', 'text/javascript'),
    }

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; style-src-elem 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
        super().end_headers()

    def reply(self, value, status=200):
        data = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path, mime):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime + '; charset=utf-8')
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
                return self.reply({'items': catalog(), 'nav': read_nav(), 'aliases': read_aliases()})
            if url.path.startswith('/files/'):
                p = resolve_inside_root(url.path[len('/files/'):])
                if p is None or not p.is_file():
                    return self.reply({'error': '未找到文件'}, 404)
                return self.send_file(p, 'application/octet-stream')
            if url.path in self.STATIC_ROUTES:
                name, mime = self.STATIC_ROUTES[url.path]
                return self.send_file(STATIC / name, mime)
            return self.reply({'error': '未找到页面'}, 404)
        except (ValueError, FileNotFoundError):
            self.reply({'error': '未找到文件'}, 404)

    def do_POST(self):
        if not self.host_ok():
            return self.reply({'error': 'Invalid host'}, 403)
        origin = self.headers.get('Origin')
        allowed = {f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'}
        if origin not in allowed:
            return self.reply({'error': 'Invalid origin'}, 403)
        if urlsplit(self.path).path != '/api/document':
            return self.reply({'error': '未找到接口'}, 404)
        if self.headers.get('Content-Type', '').split(';', 1)[0].strip().lower() != 'application/json':
            return self.reply({'error': '请求必须是 JSON'}, 415)
        try:
            length = int(self.headers.get('Content-Length', ''))
        except ValueError:
            return self.reply({'error': '缺少请求长度'}, 400)
        if length < 0 or length > MAX_DOCUMENT_BYTES + 2048:
            return self.reply({'error': '请求过大'}, 413)
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('请求格式不正确')
            result = save_document(payload.get('id'), payload.get('body'), payload.get('expectedSha256'))
            return self.reply(result)
        except (UnicodeError, json.JSONDecodeError, ValueError):
            return self.reply({'error': '请求格式不正确'}, 400)
        except SaveError as error:
            return self.reply({'error': str(error)}, error.status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=4174)
    args = parser.parse_args()
    httpd = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'English Book: http://127.0.0.1:{args.port}', flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
