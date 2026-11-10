set -x
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y curl tar
VER=$(curl -fsSL https://api.github.com/repos/MHSanaei/3x-ui/releases/latest | grep -oP '"tag_name": *"[^"]+' | sed 's/.*"\([^"]*\)$/\1/')
echo "VERSION=$VER"
curl -fsSL -o /tmp/x-ui.tar.gz "https://github.com/MHSanaei/3x-ui/releases/download/${VER}/x-ui-linux-amd64.tar.gz"
ls -la /tmp/x-ui.tar.gz
rm -rf /usr/local/x-ui
tar -xzf /tmp/x-ui.tar.gz -C /usr/local/
chmod +x /usr/local/x-ui/x-ui
ls -la /usr/local/x-ui/
cat > /etc/systemd/system/x-ui.service <<'UNIT'
[Unit]
Description=x-ui Service
After=network.target
Wants=network.target

[Service]
Type=simple
WorkingDirectory=/usr/local/x-ui/
ExecStart=/usr/local/x-ui/x-ui
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable x-ui
cd /usr/local/x-ui && ./x-ui setting -username kuai-panel -password 5ccc4c561fe61b0c8101fd69 -port 2053
systemctl restart x-ui
sleep 3
systemctl is-active x-ui
cd /usr/local/x-ui && ./x-ui setting -show true
ss -tlnp | grep 2053 || true
echo "=== MANUAL INSTALL DONE ==="
