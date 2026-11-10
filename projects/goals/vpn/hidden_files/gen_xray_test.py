#!/usr/bin/env python3
import os, json, urllib.parse

p = urllib.parse.urlparse(os.environ["https_proxy"])
cfg = {
    "log": {"loglevel": "warning"},
    "inbounds": [{
        "tag": "socks-in", "listen": "127.0.0.1", "port": 11080,
        "protocol": "socks", "settings": {"udp": True}
    }],
    "outbounds": [
        {
            "tag": "vless-out", "protocol": "vless",
            "settings": {"vnext": [{
                "address": "3.107.116.153", "port": 38147,
                "users": [{"id": "11aaa861-aef4-426e-888f-067d0e209795", "encryption": "none"}]
            }]},
            "streamSettings": {
                "network": "xhttp", "security": "reality",
                "realitySettings": {
                    "serverName": "www.microsoft.com", "fingerprint": "chrome",
                    "publicKey": "k1jQx1-NuC-9Tunn1gyC5krzkHQr8tnF6oYoPd6QdGw",
                    "shortId": "5e9cca74", "spiderX": "/"
                },
                "xhttpSettings": {"path": "/k9x2m7", "mode": "auto"},
                "sockopt": {"dialerProxy": "egress"}
            }
        },
        {
            "tag": "egress", "protocol": "http",
            "settings": {"servers": [{
                "address": p.hostname, "port": p.port or 3128,
                "users": [{"user": urllib.parse.unquote(p.username or ""), "pass": urllib.parse.unquote(p.password or "")}]
            }]}
        },
        {"tag": "direct", "protocol": "freedom"}
    ],
    "routing": {"rules": [{"type": "field", "inboundTag": ["socks-in"], "outboundTag": "vless-out"}]}
}
with open(os.path.expanduser("~/workspace/goals/vpn/hidden_files/xray_client_test.json"), "w") as f:
    json.dump(cfg, f, indent=1)
print("config written")
