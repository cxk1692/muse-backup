import re, secrets, sys

p = "/opt/dujiao-next/config.yml"
t = open(p).read()

s2 = secrets.token_hex(32)
s3 = secrets.token_hex(32)
ap = secrets.token_hex(8)

t = t.replace("your-jwt-secret-key-change-in-production-please", s2)
t = t.replace("your-user-jwt-secret-key-change-in-production-please", s3)
t = t.replace("mode: debug", "mode: release")
t = re.sub(r'default_admin_username:\s*".*?"', 'default_admin_username: "admin"', t)
t = re.sub(r'default_admin_password:\s*".*?"', 'default_admin_password: "%s"' % ap, t)

open(p, "w").write(t)
print("ADMIN_PW=" + ap)
print("jwt set:", s2[:6], "user_jwt set:", s3[:6])
