import re, secrets

p = "/opt/dujiao-next/config.yml"
lines = open(p).read().splitlines(True)

section = None
changed = []
out = []
vals = {}
for ln in lines:
    m = re.match(r"^([a-z_]+):\s*$", ln)
    if m:
        section = m.group(1)
    if section in ("jwt", "user_jwt") and re.match(r"^\s+(secret|secret_key):", ln):
        key = "jwt" if section == "jwt" else "user_jwt"
        if key not in vals:
            vals[key] = secrets.token_hex(32)
        indent = re.match(r"^(\s+)", ln).group(1)
        field = re.match(r"^\s+(secret|secret_key):", ln).group(1)
        ln = "%s%s: %s\n" % (indent, field, vals[key])
        changed.append(section + "." + field)
    out.append(ln)

open(p, "w").write("".join(out))
print("changed:", changed)
