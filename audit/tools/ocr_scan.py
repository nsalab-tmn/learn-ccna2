# Dictionary pass over OCR text of rendered SVGs and rasters. Out: out/ocr_hits.json
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from terms import COMPILED
from common import REPO, WORK as S, tracked_files
files = tracked_files()
bymangled = {}
for f in files:
    bymangled[f.replace("/", "_")] = f
hits = []
for d, kind, suffix in (("ocr", "svg", ".svg.txt"), ("ocr_raster", "raster", ".txt")):
    for fn in sorted(os.listdir(os.path.join(S, d))):
        if not fn.endswith(".txt"):
            continue
        key = fn[len("svg__"):] if fn.startswith("svg__") else fn
        key = key[:-4]
        src = bymangled.get(key)
        if not src:
            print("unmapped", fn); continue
        text = open(os.path.join(S, d, fn), encoding="utf-8", errors="replace").read()
        for n, line in enumerate(text.split("\n"), 1):
            for term, rx, cat, origin in COMPILED:
                for m in rx.finditer(line):
                    hits.append({"term": term, "file": src, "kind": kind, "line": n, "match": m.group(0), "text": line.strip()})
json.dump(hits, open(os.path.join(S, "out", "ocr_hits.json"), "w"), ensure_ascii=False, indent=0)
import collections
print(len(hits))
c = collections.Counter((h["kind"], h["term"]) for h in hits)
for k, v in sorted(c.items()): print(k, v)
