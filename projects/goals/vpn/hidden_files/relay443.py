#!/usr/bin/env python3
# Local TCP relay: listen :38149, forward to 3.107.116.153:443 via egress HTTP CONNECT proxy.
import os, socket, sys, base64, urllib.parse, threading

TARGET = ("3.107.116.153", 443)
LISTEN = ("127.0.0.1", 38149)

def connect_via_proxy():
    p = urllib.parse.urlparse(os.environ["https_proxy"])
    auth = base64.b64encode(
        f"{urllib.parse.unquote(p.username or '')}:{urllib.parse.unquote(p.password or '')}".encode()
    ).decode()
    s = socket.create_connection((p.hostname, p.port or 3128), timeout=30)
    s.sendall(
        f"CONNECT {TARGET[0]}:{TARGET[1]} HTTP/1.1\r\nHost: {TARGET[0]}:{TARGET[1]}\r\n"
        f"Proxy-Authorization: Basic {auth}\r\n\r\n".encode()
    )
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = s.recv(4096)
        if not chunk:
            raise IOError("proxy closed during CONNECT")
        buf += chunk
    head, _, rest = buf.partition(b"\r\n\r\n")
    if b" 200 " not in head.split(b"\r\n")[0]:
        raise IOError("CONNECT failed: " + head.split(b"\r\n")[0].decode(errors="replace"))
    return s, rest

def pipe(src, dst, initial=b""):
    try:
        if initial:
            dst.sendall(initial)
        while True:
            data = src.recv(65536)
            if not data:
                break
            dst.sendall(data)
    except Exception:
        pass
    try:
        dst.shutdown(socket.SHUT_WR)
    except Exception:
        pass

def handle(client):
    try:
        upstream, rest = connect_via_proxy()
    except Exception as e:
        print("upstream failed:", e, flush=True)
        client.close()
        return
    t = threading.Thread(target=pipe, args=(client, upstream), daemon=True)
    t.start()
    pipe(upstream, client, rest)
    try:
        client.close(); upstream.close()
    except Exception:
        pass

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(LISTEN)
    srv.listen(64)
    print(f"relay listening on {LISTEN} -> {TARGET}", flush=True)
    while True:
        c, _ = srv.accept()
        threading.Thread(target=handle, args=(c,), daemon=True).start()

if __name__ == "__main__":
    main()
