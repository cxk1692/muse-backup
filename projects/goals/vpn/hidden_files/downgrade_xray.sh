set -x
cd /tmp
curl -fsSL -o xray26627.zip "https://github.com/XTLS/Xray-core/releases/download/v26.6.27/Xray-linux-64.zip"
ls -la xray26627.zip
rm -rf /tmp/xray26627 && mkdir -p /tmp/xray26627
python3 -m zipfile -e /tmp/xray26627.zip /tmp/xray26627/
ls -la /tmp/xray26627/
/tmp/xray26627/xray version | head -2
systemctl stop x-ui
cp /usr/local/x-ui/bin/xray-linux-amd64 /usr/local/x-ui/bin/xray-linux-amd64.bak-26.10.21
install -m 755 /tmp/xray26627/xray /usr/local/x-ui/bin/xray-linux-amd64
/usr/local/x-ui/bin/xray-linux-amd64 version | head -2
systemctl start x-ui
sleep 4
systemctl is-active x-ui
ss -tlnp 2>/dev/null | grep -E ":443 |:38147 " || ss -tln | grep -E "443|38147"
echo "=== DOWNGRADE DONE ==="
