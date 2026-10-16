# Pass 1: dictionary scan over every tracked text file. Emits out/hits.json.
# Binary/visual files (svg, rasters, pka, docx, pdf) are handled by other passes.
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, WORK, OUT, AUD, tracked_files
from terms import COMPILED

BINARY_EXT = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".pka", ".pkt", ".docx", ".pdf")

files = tracked_files()


def quiz_spans(text):
    """Line spans (1-based, inclusive) of each object in a top-level "questions" array."""
    spans, depth, in_str, esc, line = [], 0, False, False, 1
    q_depth, start = None, None
    i = text.find('"questions"')
    if i < 0:
        return spans
    line = text.count("\n", 0, i) + 1
    j = text.index("[", i)
    line += text.count("\n", i, j)
    arr_depth = 0
    for k in range(j, len(text)):
        ch = text[k]
        if ch == "\n":
            line += 1
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "[{":
            arr_depth += 1
            if ch == "{" and arr_depth == 2:
                start = line
        elif ch in "]}":
            if ch == "}" and arr_depth == 2:
                spans.append((start, line))
            arr_depth -= 1
            if arr_depth == 0:
                break
    return spans


hits = []
for f in files:
    if f.lower().endswith(BINARY_EXT):
        continue
    p = os.path.join(REPO, f)
    try:
        text = open(p, encoding="utf-8").read()
    except UnicodeDecodeError:
        text = open(p, encoding="latin-1").read()
    lines = text.split("\n")
    offs, o = [], 0
    for l in lines:
        offs.append(o); o += len(l) + 1
    cspans = [(m.start(), m.end()) for m in re.finditer(r"<!--.*?(?:-->|$)", text, re.S)] if f.endswith(".md") else []
    qs = quiz_spans(text) if f.endswith("learn-metadata.json") else []
    in_fence = False
    for n, raw in enumerate(lines, 1):
        fence_line = f.endswith(".md") and raw.strip().startswith("```")
        if fence_line:
            in_fence = not in_fence
        code = f.endswith(".md") and (in_fence or fence_line)
        inline = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"`[^`]+`|\*\*[^*]+\*\*", raw)]
        q = next((qi for qi, (a, b) in enumerate(qs, 1) if a <= n <= b), None)
        for term, rx, cat, origin in COMPILED:
            for m in rx.finditer(raw):
                ab = offs[n - 1] + m.start()
                il = next((s[2] for s in inline if s[0] <= m.start() < s[1]), None)
                hits.append({
                    "term": term, "file": f, "line": n, "col": m.start(), "match": m.group(0),
                    "default_cat": cat, "origin": origin, "in_code": code,
                    "in_comment": any(a <= ab < b for a, b in cspans),
                    "inline": il, "question": q, "text": raw,
                })
json.dump(hits, open(os.path.join(OUT, "hits.json"), "w"), ensure_ascii=False)
print(len(hits), "hits")
