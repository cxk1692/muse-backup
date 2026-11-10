#!/usr/bin/env python3
import os, socket, sys, base64, urllib.parse

host, port = sys.argv[1], int(sys.argv[2])
p = urllib.parse.urlparse(os.environ["https_proxy"])
auth = base64.b64encode(
    f"{urllib.parse.unquote(p.username or '')}:{urllib.parse.unquote(p.password or '')}".encode()
).decode()
s = socket.create_connection((p.hostname, p.port or 3128), timeout=15)
s.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\nProxy-Authorization: Basic {auth}\r\n\r\n".encode())
resp = s.recv(1024)
print("PROBE", host, port, "->", resp.split(b"\r\n")[0].decode(errors="replace"))
s.close()
