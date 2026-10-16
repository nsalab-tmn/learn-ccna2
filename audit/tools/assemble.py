# Pass 4: merge rows, assign ids in course order, build the hits ledger (N = M + K per term), write audit/ files' data.
import csv, json, os, re, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
from terms import TERMS

from common import REPO, WORK as S, OUT, AUD

rt = json.load(open(os.path.join(OUT, "rows_text.json")))
rv = json.load(open(os.path.join(OUT, "rows_visual.json")))
for i, r in enumerate(rt):
    r["_src"], r["_idx"] = "text", i
for i, r in enumerate(rv):
    r["_src"], r["_idx"] = "visual", i
rows = rt + rv

# course order of modules
root = json.load(open(os.path.join(REPO, "learn-metadata.json")))
order = [m["$ref"].split("/")[1] for m in root["materials"]]
def mkey(m):
    if m in order:
        return order.index(m)
    return 100 if m == "(root)" else 101
SURF = ["metadata", "filename", "text", "code", "comment", "quiz", "illustration", "animation", "raster", "video", "lab-infra", "figma-library", "internal-doc"]
def nat(s):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]
rows.sort(key=lambda r: (mkey(r["module"]), nat(r["material"]), nat(r["_file"]), r["_line"], SURF.index(r["surface"]) if r["surface"] in SURF else 99))
for n, r in enumerate(rows, 1):
    r["id"] = f"ccna2-vm-{n:04d}"
    for a, b in (("[D10]", "[D9]"), ("[D11]", "[D10]"), ("[D12]", "[D11]"), ("[D13]", "[D12]"), ("[D14]", "[D13]")):
        r["note"] = r["note"].replace(a, b)
    EXTRA = {
        "final-lab-part2/learn-metadata.json:3": "; ОПЕЧАТКА/ДЕФЕКТ: shortName «srwe-f1» совпадает с final-lab-part1 — должно быть «srwe-f2»",
        "09-fhrp-concepts/09.03.03-lab-hsrp-configuration-guide/learn-metadata.json:5": "; опечатка «отрабока»",
        "migration-instructions.md:278": "; опечатка «Packet Trcer»",
        "learn-metadata.json:2": "; опечатка «Ведение» (Введение)",
    }
    for k, v in EXTRA.items():
        if r["locator"] == k or r["locator"].startswith(k + " "):
            r["note"] += v
id_of = {(r["_src"], r["_idx"]): r["id"] for r in rows}

COLS = ["id", "module", "material", "surface", "locator", "term", "category", "audience", "excerpt", "action", "note"]
with open(os.path.join(AUD, "vendor-mentions.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(COLS)
    for r in rows:
        w.writerow([r[c] for c in COLS])

# ---------------- ledger
ledger = []
for l in json.load(open(os.path.join(OUT, "ledger_text.json"))):
    src = "filename" if l["line"] == 0 else "text"
    if l["disposition"] == "row":
        ledger.append({"term": l["term"], "source": src, "file": l["file"], "line": l["line"], "match": l["match"],
                       "disposition": id_of[("text", l["row"])], "reason": ""})
    else:
        ledger.append({"term": l["term"], "source": src, "file": l["file"], "line": l["line"], "match": l["match"],
                       "disposition": "excluded", "reason": l["reason"]})
rows_by_file = collections.defaultdict(list)
for r in rows:
    rows_by_file[r["_file"]].append(r["id"])
REAL_LEGAL = {"13-wlan-configuration/13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.3-1.png"}
for h in json.load(open(os.path.join(OUT, "ocr_hits.json"))):
    src = "ocr-" + h["kind"]
    f = h["file"]
    reason = None
    if h["term"] in ("©", "®", "™") and f not in REAL_LEGAL:
        reason = "OCR-артефакт: круглые маркеры легенды, иконки или фавикон вкладки распознаны как ©/®/™ (проверено глазами)"
    elif h["term"] == "ESA/WSA" and f.endswith("12.3.3-2.svg"):
        reason = "ложное совпадение: ESA = Extended Service Area (зона обслуживания 802.11)"
    elif h["term"] in ("EtherChannel",) and re.search(r"show etherchannel", h["text"], re.I):
        reason = "синтаксис CLI в стиле IOS: команда show etherchannel summary в растре"
    elif h["term"] in ("v7", "itn", "srwe", "ccna") and f.startswith("readme-assets/") and f in rows_by_file:
        reason = None
    if reason is None and f in rows_by_file:
        ledger.append({"term": h["term"], "source": src, "file": f, "line": h["line"], "match": h["match"],
                       "disposition": rows_by_file[f][0], "reason": ""})
    else:
        ledger.append({"term": h["term"], "source": src, "file": f, "line": h["line"], "match": h["match"],
                       "disposition": "excluded", "reason": reason or "НЕТ СТРОКИ"})
for h in json.load(open(os.path.join(OUT, "doc_hits.json"))):
    src = "docx" if h["file"].endswith(".docx") else "pdf"
    ledger.append({"term": h["term"], "source": src, "file": h["file"], "line": h["line"], "match": h["match"],
                   "disposition": rows_by_file[h["file"]][0], "reason": ""})
missing = [l for l in ledger if l["reason"] == "НЕТ СТРОКИ"]
print("ledger", len(ledger), "missing", len(missing))
for l in missing[:40]:
    print("  MISSING", l)
with open(os.path.join(AUD, "dictionary-hits.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["term", "source", "file", "line", "match", "disposition", "reason"])
    for l in ledger:
        w.writerow([l[k] for k in ("term", "source", "file", "line", "match", "disposition", "reason")])

# ---------------- stats for the report
st = {}
st["rows"] = len(rows)
st["by_category"] = collections.Counter(r["category"] for r in rows).most_common()
st["by_surface"] = collections.Counter(r["surface"] for r in rows).most_common()
st["by_audience"] = collections.Counter(r["audience"] for r in rows).most_common()
st["by_action"] = collections.Counter(r["action"].split(":")[0] for r in rows).most_common()
st["by_module"] = sorted(collections.Counter(r["module"] for r in rows).items(), key=lambda kv: mkey(kv[0]))
st["module_cat"] = {m: collections.Counter(r["category"] for r in rows if r["module"] == m) for m, _ in st["by_module"]}
lm = collections.Counter(r["material"] for r in rows if r["audience"] == "learner" and r["material"] not in ("(root)",))
st["top_materials"] = []
for mat, n in lm.most_common(20):
    cc = collections.Counter(r["category"] for r in rows if r["material"] == mat and r["audience"] == "learner")
    st["top_materials"].append((mat, n, cc.most_common(3)))
recon = []
for t, rx, cat, origin in TERMS:
    L = [l for l in ledger if l["term"] == t]
    N = len(L); M = sum(1 for l in L if l["disposition"] != "excluded"); K = N - M
    srcs = collections.Counter(l["source"] for l in L)
    reasons = collections.Counter(l["reason"].split(":")[0] for l in L if l["disposition"] == "excluded")
    files_n = len({l["file"] for l in L if l["source"] in ("text",)})
    recon.append({"term": t, "regex": rx, "origin": origin, "N": N, "M": M, "K": K, "files_text": files_n,
                  "sources": dict(srcs), "reasons": dict(reasons)})
st["recon"] = recon
st["dec_counts"] = collections.Counter(d for r in rows for d in re.findall(r"\[(D\d+(?:\.\d+)?)\]", r["note"])).most_common()
json.dump(st, open(os.path.join(OUT, "stats.json"), "w"), ensure_ascii=False, indent=1, default=list)
print(st["rows"], st["by_category"])
print(st["by_surface"])
print(st["by_action"])
print("recon ok:", all(x["N"] == x["M"] + x["K"] for x in recon))
