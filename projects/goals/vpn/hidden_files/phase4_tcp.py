#!/usr/bin/env python3
import json, re, subprocess, urllib.request, http.cookiejar, sys

BASE = "http://127.0.0.1:2053/617d705d6b50a140"
USER = "kuai-panel"
PASS = "5ccc4c561fe61b0c8101fd69"
UUID = "11aaa861-aef4-426e-888f-067d0e209795"
SNI = "www.amazon.com"
PORT = 443

out = subprocess.run(["/usr/local/x-ui/bin/xray-linux-amd64", "x25519"], capture_output=True, text=True).stdout
priv = re.search(r"PrivateKey:\s*(\S+)", out).group(1)
pub = re.search(r"PublicKey\):\s*(\S+)", out).group(1)
shortid = subprocess.run(["openssl", "rand", "-hex", "4"], capture_output=True, text=True).stdout.strip()
print("NEWKEYS", priv, pub, shortid)

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch_csrf():
    with opener.open(BASE + "/", timeout=20) as r:
        html = r.read().decode(errors="replace")
    m = re.search(r'name="csrf-token" content="([^"]+)"', html)
    return m.group(1) if m else ""

CSRF = fetch_csrf()

def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": "application/json", "X-CSRF-Token": CSRF})
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:
        return -1, f"ERR {e!r}"

st, body = post("/login", {"username": USER, "password": PASS})
print("LOGIN:", st, body[:200])
if '"success":true' not in body.replace(" ", ""):
    print("LOGIN_FAILED_STOP"); sys.exit(1)

settings = {
    "clients": [{
        "id": UUID, "flow": "xtls-rprx-vision", "email": "kuai", "limitIp": 0,
        "totalGB": 0, "expiryTime": 0, "enable": True, "tgId": "", "subId": "kuai7syd", "reset": 0
    }],
    "decryption": "none", "fallbacks": []
}
stream = {
    "network": "tcp",
    "security": "reality",
    "externalProxy": [],
    "tcpSettings": {"acceptProxyProtocol": False, "header": {"type": "none"}},
    "realitySettings": {
        "show": False, "xver": 0,
        "dest": SNI + ":443",
        "serverNames": [SNI],
        "privateKey": priv,
        "minClientVer": "", "maxClientVer": "", "maxTimeDiff": 0,
        "shortIds": [shortid],
        "settings": {"publicKey": pub, "fingerprint": "chrome", "spiderX": "/"}
    }
}
sniffing = {"enabled": True, "destOverride": ["http", "tls", "quic", "fakedns"], "metadataOnly": False, "routeOnly": False}
payload = {
    "up": 0, "down": 0, "total": 0, "remark": "sydney-tcp443",
    "enable": True, "expiryTime": 0, "listen": "", "port": PORT, "protocol": "vless",
    "settings": json.dumps(settings), "streamSettings": json.dumps(stream), "sniffing": json.dumps(sniffing)
}
st, body = post("/panel/api/inbounds/add", payload)
print("ADD:", st, body[:400])
link = (f"vless://{UUID}@3.107.116.153:443?encryption=none&flow=xtls-rprx-vision"
        f"&security=reality&sni={SNI}&fp=chrome&pbk={pub}&sid={shortid}&spx=%2F&type=tcp#sydney-tcp443")
print("LINK:", link)
print("=== PHASE4 DONE ===")
