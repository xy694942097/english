#!/usr/bin/env python3
"""Local markdown book: nav.json 显式登记目录，只读查看器。

用法:
    python3 server.py [--port 4174]

路由:
    /api/catalog     返回 nav.json 登记的全部文档（含正文）
    /files/...       返回仓库内静态资源（markdown 里的相对路径图片等）
    其他             返回 public/ 下的静态文件
"""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).parent / 'public'
def read_nav(root=ROOT):
    path = root / 'nav.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'groups': []}


def read_aliases(root=ROOT):
    path = root / 'engineering/design/document-paths-2026-10-11.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def catalog(root=ROOT, nav=None):
    """只收录 nav.json 登记的文档；标题取自正文一级标题。"""
    nav = read_nav(root) if nav is None else nav
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
                                  'group': title, 'body': body})
                else:
                    walk(it['items'], title)
        walk(group['items'], group['title'])
    return items


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
    }

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
            if url.path in {'/api/catalog', '/catalog.json'}:
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
        return self.reply({'error': '站点只提供阅读，写入接口已移除'}, 405)


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
