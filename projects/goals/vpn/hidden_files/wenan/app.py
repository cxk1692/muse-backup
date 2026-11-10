#!/usr/bin/env python3
"""文案库 Wenan — 管理页 + 读写 API（仅 Python 标准库）。
路由（Nginx 已剥掉 /wenan 前缀）:
  GET  /                 管理页（需登录）
  GET|POST /login        登录
  POST /logout
  POST /ui/items         网页端新增/编辑（表单）
  POST /ui/items/<id>/delete
  --- API（需 X-API-Key 或 Authorization: Bearer <key>）---
  GET    /api/items?q=&tag=&page=&size=
  GET    /api/items/<id>
  GET    /api/random?tag=
  POST   /api/items      {title, content, tags}
  PUT    /api/items/<id> {title, content, tags}
  DELETE /api/items/<id>
  GET    /healthz
"""
import hashlib
import hmac
import html
import json
import os
import secrets
import sqlite3
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8078"))
DATA_DIR = os.environ.get("DATA_DIR", "/opt/wenan/data")
DB_PATH = os.path.join(DATA_DIR, "wenan.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
API_KEY = os.environ.get("API_KEY", "")
SESSION_SECRET = (os.environ.get("SESSION_SECRET") or secrets.token_hex(32)).encode()
TOKEN_TTL = 30 * 86400
MAX_BODY = 256 * 1024

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL DEFAULT '',
  content TEXT NOT NULL DEFAULT '',
  tags TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at);
"""

LOGIN_ATTEMPTS = {}


def db():
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA busy_timeout=5000")
    return c


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    c = db()
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript(SCHEMA)
    c.commit()
    c.close()


def make_token():
    exp = str(int(time.time()) + TOKEN_TTL)
    sig = hmac.new(SESSION_SECRET, exp.encode(), hashlib.sha256).hexdigest()
    return exp + "." + sig


def check_token(tok):
    if not tok or "." not in tok:
        return False
    exp, sig = tok.split(".", 1)
    good = hmac.new(SESSION_SECRET, exp.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, good) and exp.isdigit() and int(exp) > time.time()


def row_out(r):
    return {"id": r["id"], "title": r["title"], "content": r["content"],
            "tags": r["tags"], "created_at": r["created_at"], "updated_at": r["updated_at"]}


LOGIN_HTML = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>文案库 · 登录</title>
<style>body{background:#0b0b0f;color:#e8e8ec;font-family:system-ui;max-width:420px;margin:12vh auto;padding:0 20px}
input,button{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #333;background:#17171d;color:#eee;font-size:16px}
button{background:#e8e8ec;color:#111;border:0;font-weight:600}</style></head><body>
<h2>文案库</h2><p style="color:#999">输入管理密码进入</p>
<form method="post" action="login"><input type="password" name="password" placeholder="密码" autofocus>
<button>登录</button></form></body></html>"""

UI_HTML = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>文案库</title>
<style>body{background:#0b0b0f;color:#e8e8ec;font-family:system-ui;max-width:860px;margin:0 auto;padding:18px}
input,textarea,button{border-radius:10px;border:1px solid #333;background:#17171d;color:#eee;font-size:15px;padding:10px}
button{background:#e8e8ec;color:#111;border:0;font-weight:600;padding:10px 16px}
.card{border:1px solid #26262e;border-radius:12px;padding:14px;margin:10px 0;background:#121218}
.tag{color:#8ab4ff;font-size:12px}.muted{color:#888;font-size:12px}pre{white-space:pre-wrap;word-break:break-word;font-family:inherit}
.row{display:flex;gap:8px}.row>*{flex:1}</style></head><body>
<h2>文案库 <span class="muted" id="cnt"></span></h2>
<div class="row"><input id="q" placeholder="搜索标题/正文/标签"><button style="flex:0 0 auto" onclick="load()">搜索</button>
<button style="flex:0 0 auto" onclick="logout()">退出</button></div>
<div class="card"><b>新增文案</b>
<input id="ntitle" placeholder="标题（可空）" style="width:97%;margin-top:8px">
<textarea id="ncontent" rows="4" placeholder="文案正文" style="width:97%;margin-top:8px"></textarea>
<input id="ntags" placeholder="标签，逗号分隔（如：互动帖,段子）" style="width:97%;margin-top:8px">
<div style="margin-top:8px"><button onclick="add()">保存</button></div></div>
<div id="list"></div>
<script>
async function api(p,opt){const r=await fetch(p,opt);if(r.status===401){location='login';throw 0}return r.json()}
async function load(){const q=document.getElementById('q').value;const d=await api('api/items?size=50&q='+encodeURIComponent(q));
document.getElementById('cnt').textContent='共 '+d.total+' 条';
document.getElementById('list').innerHTML=d.items.map(i=>`<div class="card"><div class="tag">${esc(i.tags)}</div>
<b>${esc(i.title||'(无标题)')}</b><pre>${esc(i.content)}</pre>
<button onclick="del(${i.id})">删除</button></div>`).join('')||'<p class="muted">还没有文案，先加一条吧。</p>'}
async function add(){const body={title:document.getElementById('ntitle').value,content:document.getElementById('ncontent').value,tags:document.getElementById('ntags').value};
if(!body.content.trim()){alert('正文不能为空');return}
await api('api/items',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
document.getElementById('ntitle').value=document.getElementById('ncontent').value=document.getElementById('ntags').value='';load()}
async function del(id){if(!confirm('确认删除这条？'))return;await api('api/items/'+id,{method:'DELETE'});load()}
async function logout(){await fetch('logout',{method:'POST'});location='login'}
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
load();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "wenan"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    timeout = 20

    def log_message(self, fmt, *args):
        pass

    def send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode()
        elif isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def err(self, code, msg):
        self.send(code, {"code": code, "msg": msg})

    def read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            raise ValueError("too large")
        raw = self.rfile.read(n) if n > 0 else b""
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def read_form(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n > 0 else b""
        return dict(urllib.parse.parse_qsl(raw.decode("utf-8", "replace")))

    def session_ok(self):
        ck = self.headers.get("Cookie") or ""
        for part in ck.split(";"):
            part = part.strip()
            if part.startswith("wenan_admin="):
                return check_token(urllib.parse.unquote(part[len("wenan_admin="):]))
        return False

    def api_key_ok(self):
        k = self.headers.get("X-API-Key") or ""
        if not k:
            auth = self.headers.get("Authorization") or ""
            if auth.startswith("Bearer "):
                k = auth[7:]
        return bool(API_KEY) and hmac.compare_digest(k, API_KEY)

    def do_GET(self):
        self.route()

    def do_POST(self):
        self.route()

    def do_PUT(self):
        self.route()

    def do_DELETE(self):
        self.route()

    def do_HEAD(self):
        self.route()

    def route(self):
        try:
            u = urllib.parse.urlsplit(self.path)
            path = u.path
            q = dict(urllib.parse.parse_qsl(u.query))
            m = self.command
            if path == "/healthz":
                return self.send(200, {"ok": True})
            if path == "/login":
                if m == "GET":
                    return self.send(200, LOGIN_HTML, "text/html; charset=utf-8")
                return self.do_login()
            if path == "/logout" and m == "POST":
                return self.send(200, {"code": 200}, extra={"Set-Cookie": "wenan_admin=; Max-Age=0; Path=/"})
            if path.startswith("/api/"):
                return self.api(path, q)
            if path in ("/", "/index.html") and m in ("GET", "HEAD"):
                if not self.session_ok():
                    return self.send(302, b"", extra={"Location": "login"})
                return self.send(200, UI_HTML, "text/html; charset=utf-8")
            return self.err(404, "未找到")
        except ValueError:
            return self.err(400, "请求格式错误")
        except Exception:
            return self.err(500, "服务器内部错误")

    def do_login(self):
        ip = self.client_address[0]
        now = time.time()
        att = [t for t in LOGIN_ATTEMPTS.get(ip, []) if now - t < 60]
        if len(att) >= 5:
            return self.err(429, "尝试过多，请稍后再试")
        form = self.read_form()
        pw = form.get("password") or ""
        ok = bool(ADMIN_PASSWORD) and hmac.compare_digest(pw.encode(), ADMIN_PASSWORD.encode())
        if not ok:
            att.append(now)
            LOGIN_ATTEMPTS[ip] = att
            return self.send(401, LOGIN_HTML.replace("</form>", "<p style='color:#f66'>密码不正确</p></form>"), "text/html; charset=utf-8")
        tok = make_token()
        return self.send(302, b"", extra={"Location": "./",
                                          "Set-Cookie": "wenan_admin=%s; Max-Age=%d; HttpOnly; SameSite=Strict; Path=/" % (tok, TOKEN_TTL)})

    # ---------------- API ----------------
    def api(self, path, q):
        if not (self.api_key_ok() or self.session_ok()):
            return self.err(401, "需要 API 密钥")
        m = self.command
        if path == "/api/items" and m == "GET":
            return self.api_list(q)
        if path == "/api/items" and m == "POST":
            return self.api_create()
        if path == "/api/random" and m == "GET":
            return self.api_random(q)
        if path.startswith("/api/items/"):
            try:
                iid = int(path.split("/")[3])
            except (IndexError, ValueError):
                return self.err(400, "参数错误")
            if m == "GET":
                return self.api_get(iid)
            if m == "PUT":
                return self.api_update(iid)
            if m == "DELETE":
                return self.api_delete(iid)
        return self.err(404, "未找到")

    def _where(self, q):
        where, args = [], []
        kw = (q.get("q") or "").strip()[:100]
        if kw:
            like = "%" + kw.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
            where.append("(title LIKE ? ESCAPE '\\' OR content LIKE ? ESCAPE '\\' OR tags LIKE ? ESCAPE '\\')")
            args += [like, like, like]
        tag = (q.get("tag") or "").strip()[:50]
        if tag:
            where.append("(',' || tags || ',') LIKE ?")
            args.append("%," + tag + ",%")
        return (" WHERE " + " AND ".join(where)) if where else "", args

    def api_list(self, q):
        try:
            page = max(1, int(q.get("page") or 1))
            size = max(1, min(200, int(q.get("size") or 20)))
        except ValueError:
            return self.err(400, "参数错误")
        where, args = self._where(q)
        c = db()
        try:
            total = c.execute("SELECT COUNT(*) FROM items" + where, args).fetchone()[0]
            rows = c.execute("SELECT * FROM items" + where + " ORDER BY id DESC LIMIT ? OFFSET ?",
                             args + [size, (page - 1) * size]).fetchall()
        finally:
            c.close()
        return self.send(200, {"code": 200, "total": total, "page": page, "size": size,
                               "items": [row_out(r) for r in rows]})

    def api_random(self, q):
        where, args = self._where(q)
        c = db()
        try:
            r = c.execute("SELECT * FROM items" + where + " ORDER BY RANDOM() LIMIT 1", args).fetchone()
        finally:
            c.close()
        if not r:
            return self.err(404, "没有符合条件的文案")
        return self.send(200, {"code": 200, "item": row_out(r)})

    def api_get(self, iid):
        c = db()
        try:
            r = c.execute("SELECT * FROM items WHERE id=?", (iid,)).fetchone()
        finally:
            c.close()
        if not r:
            return self.err(404, "记录不存在")
        return self.send(200, {"code": 200, "item": row_out(r)})

    def api_create(self):
        j = self.read_json()
        title = str(j.get("title") or "")[:200]
        content = str(j.get("content") or "")[:20000]
        tags = str(j.get("tags") or "")[:200]
        if not content.strip():
            return self.err(400, "content 不能为空")
        now = int(time.time())
        c = db()
        try:
            cur = c.execute("INSERT INTO items(title,content,tags,created_at,updated_at) VALUES(?,?,?,?,?)",
                            (title, content, tags, now, now))
            c.commit()
            iid = cur.lastrowid
        finally:
            c.close()
        return self.send(200, {"code": 200, "id": iid})

    def api_update(self, iid):
        j = self.read_json()
        c = db()
        try:
            r = c.execute("SELECT * FROM items WHERE id=?", (iid,)).fetchone()
            if not r:
                return self.err(404, "记录不存在")
            title = str(j.get("title", r["title"]))[:200]
            content = str(j.get("content", r["content"]))[:20000]
            tags = str(j.get("tags", r["tags"]))[:200]
            c.execute("UPDATE items SET title=?,content=?,tags=?,updated_at=? WHERE id=?",
                      (title, content, tags, int(time.time()), iid))
            c.commit()
        finally:
            c.close()
        return self.send(200, {"code": 200})

    def api_delete(self, iid):
        c = db()
        try:
            n = c.execute("DELETE FROM items WHERE id=?", (iid,)).rowcount
            c.commit()
        finally:
            c.close()
        return self.send(200, {"code": 200, "deleted": n}) if n else self.err(404, "记录不存在")


class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 32


def main():
    init_db()
    srv = Server((HOST, PORT), Handler)
    print("wenan listening on http://%s:%d db=%s" % (HOST, PORT, DB_PATH), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
