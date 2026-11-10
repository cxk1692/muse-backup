#!/usr/bin/env python3
# PromptBook — tiny single-user prompt notebook (stdlib only).
import hashlib, json, os, secrets, sqlite3, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

DB_PATH = "/var/lib/promptbook/notes.db"
SALT = os.environ.get("PB_SALT", "")
PW_HASH = os.environ.get("PB_HASH", "")
SESSIONS = {}
SESSION_TTL = 7 * 24 * 3600

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL DEFAULT '',
        body TEXT NOT NULL DEFAULT '',
        tags TEXT NOT NULL DEFAULT '',
        created INTEGER NOT NULL,
        updated INTEGER NOT NULL)""")
    n = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    if n == 0:
        now = int(time.time())
        conn.execute("INSERT INTO notes(title,body,tags,created,updated) VALUES(?,?,?,?,?)",
            ("示例：欢迎使用提示词笔记本",
             "这是一条示例，点「编辑」改它，或者删掉。\n\n用法：\n1. 点右下角 + 新建一条提示词\n2. 给它起个好找的标题，再打上标签（比如 生图 / 写文案 / 视频）\n3. 要用的时候点「复制」，粘贴到 AI 对话框就行\n\n所有内容都存在你自己的服务器上，手机、电脑打开同一个地址都能看。",
             "示例", now, now))
    conn.commit(); conn.close()

def pw_ok(pw):
    if not SALT or not PW_HASH:
        return False
    h = hashlib.sha256((SALT + pw).encode()).hexdigest()
    return secrets.compare_digest(h, PW_HASH)

LOGIN_HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>提示词笔记本 · 登录</title><style>
body{background:#0a0a0b;color:#f2f2f0;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}
.box{width:min(340px,88vw)}h1{font-size:26px;margin-bottom:8px}p{color:#9a9a94;font-size:14px;margin-bottom:22px}
input{width:100%;padding:13px 14px;border-radius:10px;border:1px solid #2a2a2c;background:#111112;color:#f2f2f0;font-size:16px;box-sizing:border-box}
button{width:100%;margin-top:14px;padding:13px;border:0;border-radius:10px;background:#e8ff47;color:#111;font-size:16px;font-weight:700}
.err{color:#ff7a72;font-size:14px;margin-top:12px;min-height:20px}
</style></head><body><div class="box"><h1>提示词笔记本</h1><p>输入密码打开你的笔记本</p>
<form method="post" action="login"><input type="password" name="password" placeholder="密码" autofocus>
<button type="submit">打开</button><div class="err">__ERR__</div></form></div></body></html>"""

APP_HTML = r"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>提示词笔记本</title><style>
:root{--bg:#0a0a0b;--fg:#f2f2f0;--dim:#9a9a94;--line:#232324;--card:#111112;--accent:#e8ff47}
*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;margin:0}
.wrap{max-width:760px;margin:0 auto;padding:26px 18px 110px}
header{display:flex;justify-content:space-between;align-items:baseline}
h1{font-size:24px}.sub{color:var(--dim);font-size:13px}
#search{width:100%;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--fg);font-size:15px;margin:16px 0 6px}
.tags{margin:6px 0 4px}.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 11px;font-size:12px;color:var(--dim);margin:0 6px 6px 0;cursor:pointer}
.tag.on{color:#111;background:var(--accent);border-color:var(--accent);font-weight:700}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-top:14px}
.card h3{margin:0 0 6px;font-size:17px}
.card pre{white-space:pre-wrap;word-break:break-word;font-family:inherit;font-size:14.5px;color:#d8d8d2;margin:0 0 10px;line-height:1.65}
.meta{font-size:12px;color:#5c5c58;margin-bottom:10px}
.btns button{background:#1b1b1c;color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:7px 14px;font-size:13px;margin-right:8px;cursor:pointer}
.btns .copy{background:var(--accent);color:#111;font-weight:700;border-color:var(--accent)}
#fab{position:fixed;right:22px;bottom:26px;width:58px;height:58px;border-radius:50%;border:0;background:var(--accent);color:#111;font-size:30px;font-weight:700;box-shadow:0 6px 22px rgba(0,0,0,.5);cursor:pointer}
#editor{position:fixed;inset:0;background:rgba(0,0,0,.72);display:none;align-items:flex-end;justify-content:center;z-index:9}
.sheet{background:#131314;border-radius:18px 18px 0 0;width:min(760px,100%);padding:20px 18px 28px;max-height:92vh;overflow:auto}
.sheet input,.sheet textarea{width:100%;background:var(--card);border:1px solid var(--line);border-radius:10px;color:var(--fg);padding:12px;font-size:15px;margin-bottom:12px;font-family:inherit}
.sheet textarea{min-height:220px;line-height:1.6}
.row{display:flex;gap:10px}.row button{flex:1;padding:13px;border-radius:10px;border:1px solid var(--line);background:#1b1b1c;color:var(--fg);font-size:15px}
.row .save{background:var(--accent);color:#111;font-weight:700;border-color:var(--accent)}
#toast{position:fixed;left:50%;bottom:100px;transform:translateX(-50%);background:#222;color:#fff;padding:9px 18px;border-radius:999px;font-size:14px;display:none;z-index:20}
.empty{color:var(--dim);text-align:center;margin-top:60px;font-size:15px}
.logout{color:var(--dim);font-size:13px;background:none;border:0;cursor:pointer}
</style></head><body><div class="wrap">
<header><div><h1>提示词笔记本</h1><div class="sub">存在你自己的服务器上 · 随时打开</div></div>
<form method="post" action="logout"><button class="logout">退出</button></form></header>
<input id="search" placeholder="搜索标题、正文或标签…">
<div class="tags" id="tags"></div>
<div id="list"></div>
</div>
<button id="fab">+</button>
<div id="editor"><div class="sheet">
<input id="f-title" placeholder="标题（比如：小红书爆款文案）">
<input id="f-tags" placeholder="标签，用空格分开（比如 写文案 常用）">
<textarea id="f-body" placeholder="把提示词粘贴在这里…"></textarea>
<div class="row"><button onclick="closeEditor()">取消</button><button class="save" onclick="saveNote()">保存</button></div>
</div></div>
<div id="toast"></div>
<script>
let notes=[], curTag='', editingId=null;
const $=s=>document.querySelector(s);
function toast(t){const e=$('#toast');e.textContent=t;e.style.display='block';setTimeout(()=>e.style.display='none',1600)}
async function load(){const q=encodeURIComponent($('#search').value.trim());const r=await fetch('api/notes?q='+q);notes=await r.json();renderTags();render()}
function allTags(){const s=new Set();notes.forEach(n=>n.tags.split(/\s+/).filter(Boolean).forEach(t=>s.add(t)));return [...s]}
function renderTags(){$('#tags').innerHTML=allTags().map(t=>'<span class="tag'+(t===curTag?' on':'')+'" onclick="pickTag(\''+t+'\')">'+t+'</span>').join('')}
function pickTag(t){curTag=(curTag===t?'':t);renderTags();render()}
function fmt(ts){const d=new Date(ts*1000);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')}
function render(){const L=$('#list');const arr=curTag?notes.filter(n=>n.tags.split(/\s+/).includes(curTag)):notes;
 if(!arr.length){L.innerHTML='<div class="empty">还没有内容，点右下角 + 写第一条</div>';return}
 L.innerHTML=arr.map(n=>'<div class="card"><h3>'+esc(n.title||'(无标题)')+'</h3><pre>'+esc(n.body)+'</pre><div class="meta">'+(n.tags?'标签：'+esc(n.tags)+' · ':'')+'更新于 '+fmt(n.updated)+'</div><div class="btns"><button class="copy" onclick="copyNote('+n.id+')">复制</button><button onclick="editNote('+n.id+')">编辑</button><button onclick="delNote('+n.id+')">删除</button></div></div>').join('')}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
async function copyNote(id){const n=notes.find(x=>x.id===id);try{await navigator.clipboard.writeText(n.body);toast('已复制，去粘贴吧')}catch(e){const ta=document.createElement('textarea');ta.value=n.body;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();toast('已复制，去粘贴吧')}}
function openEditor(){$('#editor').style.display='flex'}
function closeEditor(){$('#editor').style.display='none';editingId=null;$('#f-title').value='';$('#f-tags').value='';$('#f-body').value=''}
function editNote(id){const n=notes.find(x=>x.id===id);editingId=id;$('#f-title').value=n.title;$('#f-tags').value=n.tags;$('#f-body').value=n.body;openEditor()}
async function saveNote(){const payload={title:$('#f-title').value.trim(),tags:$('#f-tags').value.trim(),body:$('#f-body').value};
 const url=editingId?('api/notes/'+editingId):'api/notes';await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});closeEditor();toast('已保存');load()}
async function delNote(id){if(!confirm('确定删掉这条吗？'))return;await fetch('api/notes/'+id+'/delete',{method:'POST'});toast('已删除');load()}
$('#fab').onclick=()=>{editingId=null;openEditor()};
$('#search').addEventListener('input',()=>{clearTimeout(window._t);window._t=setTimeout(load,250)});
load();
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _authed(self):
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("pb_session="):
                tok = part[len("pb_session="):]
                exp = SESSIONS.get(tok, 0)
                if exp > time.time():
                    return True
        return False

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/" or path == "":
            if self._authed():
                self._send(200, APP_HTML)
            else:
                self._send(200, LOGIN_HTML.replace("__ERR__", ""))
            return
        if path == "/api/notes":
            if not self._authed():
                self._send(401, '{"error":"login required"}', "application/json")
                return
            q = parse_qs(urlparse(self.path).query).get("q", [""])[0].strip()
            conn = db()
            if q:
                like = f"%{q}%"
                rows = conn.execute(
                    "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? OR tags LIKE ? ORDER BY updated DESC",
                    (like, like, like)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM notes ORDER BY updated DESC").fetchall()
            conn.close()
            out = [dict(r) for r in rows]
            self._send(200, json.dumps(out, ensure_ascii=False), "application/json")
            return
        self._send(404, "not found")

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        if path == "/login":
            form = parse_qs(raw.decode(errors="replace"))
            pw = form.get("password", [""])[0]
            if pw_ok(pw):
                tok = secrets.token_urlsafe(32)
                SESSIONS[tok] = time.time() + SESSION_TTL
                self._send(302, "", extra={
                    "Location": "./",
                    "Set-Cookie": f"pb_session={tok}; HttpOnly; SameSite=Lax; Max-Age={SESSION_TTL}"})
            else:
                self._send(200, LOGIN_HTML.replace("__ERR__", "密码不对，再试一次"))
            return
        if path == "/logout":
            self._send(302, "", extra={"Location": "./", "Set-Cookie": "pb_session=; HttpOnly; Max-Age=0"})
            return
        if not self._authed():
            self._send(401, '{"error":"login required"}', "application/json")
            return
        if path == "/api/notes":
            try:
                data = json.loads(raw.decode() or "{}")
            except Exception:
                data = {}
            now = int(time.time())
            conn = db()
            conn.execute("INSERT INTO notes(title,body,tags,created,updated) VALUES(?,?,?,?,?)",
                         (data.get("title", ""), data.get("body", ""), data.get("tags", ""), now, now))
            conn.commit(); conn.close()
            self._send(200, '{"ok":true}', "application/json")
            return
        if path.startswith("/api/notes/"):
            rest = path[len("/api/notes/"):]
            conn = db()
            if rest.endswith("/delete"):
                nid = rest[: -len("/delete")]
                conn.execute("DELETE FROM notes WHERE id=?", (nid,))
                conn.commit(); conn.close()
                self._send(200, '{"ok":true}', "application/json")
                return
            try:
                data = json.loads(raw.decode() or "{}")
            except Exception:
                data = {}
            conn.execute("UPDATE notes SET title=?, body=?, tags=?, updated=? WHERE id=?",
                         (data.get("title", ""), data.get("body", ""), data.get("tags", ""), int(time.time()), rest))
            conn.commit(); conn.close()
            self._send(200, '{"ok":true}', "application/json")
            return
        self._send(404, "not found")

if __name__ == "__main__":
    init_db()
    srv = ThreadingHTTPServer(("127.0.0.1", 8077), H)
    print("PromptBook on 127.0.0.1:8077", flush=True)
    srv.serve_forever()
