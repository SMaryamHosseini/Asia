import base64
import json
import re
import urllib.request
from urllib.parse import urlparse

SOURCE = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_base64_Sub.txt"

PREFIXES = (
    "185.",
    "104.",
    "23.",
    "34.",
)

def get_host(line):
    try:
        if line.startswith(("vless://", "trojan://")):
            return urlparse(line).hostname

        if line.startswith("vmess://"):
            raw = line[8:]
            padding = len(raw) % 4
            if padding:
                raw += "=" * (4 - padding)

            data = json.loads(base64.b64decode(raw).decode("utf-8", errors="ignore"))
            return data.get("add")

    except Exception:
        pass

    return None


raw = urllib.request.urlopen(SOURCE, timeout=30).read().decode()

decoded = base64.b64decode(raw).decode("utf-8", errors="ignore")

filtered = []

for line in decoded.splitlines():
    line = line.strip()

    if not line:
        continue

    host = get_host(line)

    if host and host.startswith(PREFIXES):
        filtered.append(line)

encoded = base64.b64encode(
    "\n".join(filtered).encode()
).decode()

with open("sub.txt", "w", encoding="utf-8") as f:
    f.write(encoded)

print(f"Saved {len(filtered)} configs")
