# Extract data: URIs from <image> elements of every tracked SVG; dedupe by sha256.
import base64, hashlib, json, os, re, subprocess
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, WORK as S, tracked_files
OUTD = os.path.join(S, "render", "embedded")
svgs = [f for f in tracked_files() if f.endswith(".svg")]
os.makedirs(OUTD, exist_ok=True)
rx = re.compile(rb'(?:xlink:)?href="data:image/([a-z+]+);base64,([A-Za-z0-9+/=\s]+)"')
idx = {}
per_svg = {}
for f in svgs:
    data = open(os.path.join(REPO, f), "rb").read()
    imgs = []
    for m in rx.finditer(data):
        raw = base64.b64decode(re.sub(rb"\s", b"", m.group(2)))
        h = hashlib.sha256(raw).hexdigest()[:16]
        ext = m.group(1).decode().replace("jpeg", "jpg").replace("svg+xml", "svg")
        p = os.path.join(OUTD, f"{h}.{ext}")
        if h not in idx:
            open(p, "wb").write(raw)
            idx[h] = {"file": p, "bytes": len(raw), "svgs": []}
        idx[h]["svgs"].append(f)
        imgs.append(h)
    per_svg[f] = imgs
json.dump({"images": idx, "per_svg": per_svg}, open(os.path.join(S, "out", "embedded.json"), "w"), indent=1)
print(len(idx), "unique embedded images;", sum(1 for v in per_svg.values() if v), "svgs with images")
