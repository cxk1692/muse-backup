#!/usr/bin/env python3
import json, urllib.request, http.cookiejar, sys

BASE = "http://127.0.0.1:2053/617d705d6b50a140"
USER = "kuai-panel"
PASS = "5ccc4c561fe61b0c8101fd69"

UUID = "11aaa861-aef4-426e-888f-067d0e209795"
PRIV = "MAJab7GVZbBWZIT_Fk7jxNGOSo9nC17Qc572YLKeg20"
PUB = "k1jQx1-NuC-9Tunn1gyC5krzkHQr8tnF6oYoPd6QdGw"
SHORTID = "5e9cca74"
NODE_PORT = 38147
XHTTP_PATH = "/k9x2m7"
SNI = "www.microsoft.com"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch_csrf():
    import re
    with opener.open(BASE + "/", timeout=20) as r:
        html = r.read().decode(errors="replace")
    m = re.search(r'name="csrf-token" content="([^"]+)"', html)
    return m.group(1) if m else ""

CSRF = fetch_csrf()
print("CSRF fetched:", bool(CSRF))

def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json", "X-CSRF-Token": CSRF})
    try:
        with opener.open(req, timeout=20) as r:
            body = r.read().decode(errors="replace")
            return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:
        return -1, f"ERR {e!r}"

def get(path):
    try:
        with opener.open(BASE + path, timeout=20) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:
        return -1, f"ERR {e!r}"

st, body = post("/login", {"username": USER, "password": PASS})
print("LOGIN:", st, body[:300])
if st != 200 or '"success":true' not in body.replace(" ", ""):
    print("LOGIN_FAILED_STOP")
    sys.exit(1)

settings = {
    "clients": [{
        "id": UUID, "flow": "", "email": "kuai", "limitIp": 0,
        "totalGB": 0, "expiryTime": 0, "enable": True,
        "tgId": "", "subId": "kuai7syd", "reset": 0
    }],
    "decryption": "none",
    "fallbacks": []
}
stream = {
    "network": "xhttp",
    "security": "reality",
    "externalProxy": [],
    "xhttpSettings": {"path": XHTTP_PATH, "host": "", "headers": {}, "mode": "auto"},
    "realitySettings": {
        "show": False, "xver": 0,
        "dest": SNI + ":443",
        "serverNames": [SNI],
        "privateKey": PRIV,
        "minClientVer": "", "maxClientVer": "", "maxTimeDiff": 0,
        "shortIds": [SHORTID],
        "settings": {"publicKey": PUB, "fingerprint": "chrome", "spiderX": "/"}
    }
}
sniffing = {"enabled": True, "destOverride": ["http", "tls", "quic", "fakedns"], "metadataOnly": False, "routeOnly": False}

payload = {
    "up": 0, "down": 0, "total": 0,
    "remark": "sydney-vless",
    "enable": True, "expiryTime": 0,
    "listen": "", "port": NODE_PORT, "protocol": "vless",
    "settings": json.dumps(settings),
    "streamSettings": json.dumps(stream),
    "sniffing": json.dumps(sniffing)
}
st, body = post("/panel/api/inbounds/add", payload)
print("ADD:", st, body[:500])

st, body = get("/panel/api/inbounds/list")
print("LIST:", st, body[:1200])
print("=== API PHASE DONE ===")
