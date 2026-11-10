set -x
ls /usr/local/x-ui/bin/
TOKEN=$(openssl rand -hex 8)
echo "TOKEN=$TOKEN"
cd /usr/local/x-ui && ./x-ui setting -webBasePath "/$TOKEN/" 2>&1 || ./x-ui setting -h 2>&1 | head -40
systemctl restart x-ui
sleep 3
cd /usr/local/x-ui && ./x-ui setting -show true 2>&1 | grep -v "^warning"
echo "--- x25519 keys ---"
/usr/local/x-ui/bin/xray-linux-amd64 x25519
echo "--- uuid ---"
cat /proc/sys/kernel/random/uuid
echo "--- shortid ---"
openssl rand -hex 4
echo "--- login test ---"
curl -s -X POST "http://127.0.0.1:2053/$TOKEN/login" -H 'Content-Type: application/json' -d '{"username":"kuai-panel","password":"5ccc4c561fe61b0c8101fd69"}' -c /tmp/cookies.txt
echo
echo "=== PHASE2 DONE ==="
