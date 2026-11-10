set -x
PW="$1"
mkdir -p /opt/promptbook /var/lib/promptbook
cp /tmp/app.py /opt/promptbook/app.py
chown -R www-data:www-data /var/lib/promptbook
SALT=$(openssl rand -hex 8)
HASH=$(python3 -c "import hashlib,sys; print(hashlib.sha256((sys.argv[1]+sys.argv[2]).encode()).hexdigest())" "$SALT" "$PW")
printf "PB_SALT=%s\nPB_HASH=%s\n" "$SALT" "$HASH" > /etc/promptbook.env
chmod 600 /etc/promptbook.env
cat > /etc/systemd/system/promptbook.service <<'UNIT'
[Unit]
Description=PromptBook notebook
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/promptbook
EnvironmentFile=/etc/promptbook.env
ExecStart=/usr/bin/python3 /opt/promptbook/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak-kuai 2>/dev/null || true
cat > /etc/nginx/sites-available/default <<'NGINX'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html;
    server_name _;
    location / {
        try_files $uri $uri/ =404;
    }
    location /nb/ {
        proxy_pass http://127.0.0.1:8077/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX
nginx -t
systemctl daemon-reload
systemctl enable --now promptbook
systemctl reload nginx
sleep 3
systemctl is-active promptbook
echo "--- direct app:"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8077/
echo "--- via nginx:"
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1/nb/
echo "=== NOTEBOOK INSTALL DONE ==="
