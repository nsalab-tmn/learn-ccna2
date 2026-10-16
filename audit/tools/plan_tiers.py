# Pass 6: tier every learner-facing row of vendor-mentions.csv into a work item of the de-marketing plan.
# In: WORK/audit/vendor-mentions.csv (or REPO/audit/ if the pipeline was not re-run). Out: WORK/audit/demarketing-tiers.csv
import csv, re, json, collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, OUT, AUD
src_csv = os.path.join(AUD, "vendor-mentions.csv")
if not os.path.exists(src_csv):
    src_csv = os.path.join(REPO, "audit", "vendor-mentions.csv")
R = list(csv.DictReader(open(src_csv, encoding="utf-8")))
pt_labs = {r["material"] for r in R if r["surface"] == "lab-infra" and r["term"].startswith("PT-лаба")}
gui_labs = {r["material"] for r in R if r["surface"] == "lab-infra" and r["term"].startswith("PT-лаба") and r["action"] == "decide"}
nopt_labs = {r["material"] for r in R if r["surface"] == "lab-infra" and r["term"].startswith("лаба без PT")}
def kind(r):
    m = r["material"]
    if m in pt_labs: return "pt-lab"
    if m in nopt_labs: return "nopt-lab"
    if r["surface"] == "quiz" and "-lab-" not in m: return "quiz"
    return "lecture"
BRAND_PATTERNS = [
    ("атрибуция протокола («собственный/проприетарный протокол Cisco»)", r"(собствен|проприетар|запатент|патентован|разработ\w* (компанией |корпорацией )?|реализаци\w* (компанией )?|усовершенствован\w* (корпорацией |компанией )?|собственност\w* (компании )?|изначально)\W{0,40}cisco|cisco\W{0,3}(proprietary|fhrp|-fhrp)|протокол\w* (компании )?cisco|технологи\w* (stp |rstp )?cisco"),
    ("рекомендации («Cisco рекомендует», «лучшие практики Cisco»)", r"cisco рекоменд|рекомендаци\w* cisco|практик\w* (методами )?cisco"),
    ("«решения/продукты Cisco»", r"(решени\w*|продукт\w*) cisco|cisco (email|nac)"),
    ("квалификатор устройства («коммутатор/роутер/устройство/IP-телефон Cisco»)", r"(коммутатор\w*|роутер\w*|маршрутизатор\w*|устройств\w*|телефон\w*|контроллер\w*|интерфейс\w* командной строки|сет\w*|точк\w* доступа)( \w+)?\W{0,3}cisco|cisco( \w+)? (коммутатор|роутер|устройств|ip-телефон)"),
]
rows = []
def put(r, tier, item, hint=""):
    rows.append({"id": r["id"], "tier": tier, "item": item, "kind": kind(r), "surface": r["surface"], "locator": r["locator"], "term": r["term"], "hint": hint})
for r in R:
    if r["audience"] != "learner":
        continue
    s, c, t, n, k, ex = r["surface"], r["category"], r["term"], r["note"], kind(r), r["excerpt"]
    tl, exl = t.lower(), ex.lower()
    if "[D6]" in n:
        put(r, "X", "X.1 видео (вне плана: пересборка)"); continue
    if s == "illustration" and "текстуры" in t or s == "figma-library":
        put(r, "K", "K.4 стиль иллюстраций и иконки — оставить"); continue
    # ---- values
    if "[D11]" in n:
        if k == "pt-lab": put(r, "3", "3.1 лабы PT → learn-netsim (значения зашиты в .pka)")
        elif s == "raster": put(r, "2", "2.7 растры: перерисовка без изменения смысла")
        else: put(r, "1", "1.1 значения конфигурации (пароли, домены, имена)")
        continue
    # ---- PT / labs / WLAN GUI
    if c in ("product", "lab-infra") and re.search(r"packet|\bpt\b|pt-|homerouter|wrt300n|lap-pt", tl):
        if k == "pt-lab" or "логической топологии" in t: put(r, "3", "3.1 лабы PT → learn-netsim")
        elif "GUI Packet Tracer" in t or "HomeRouter" in t or "WRT300N" in t: put(r, "2", "2.8 скриншоты GUI домашнего роутера PT → нейтральный компонент")
        else: put(r, "1", "1.3 «Packet Tracer» в тексте лекций")
        continue
    if s == "raster" and ("логической топологии" in t): put(r, "3", "3.1 лабы PT → learn-netsim"); continue
    if s == "raster" and re.search(r"wlc|cisco 3500|air-ap|meraki dashboard|© 2005|3504", tl) or "13.2.5.png" in r["locator"]:
        put(r, "3", "3.2 WLAN/WLC: GUI контроллера Cisco"); continue
    # ---- protocols
    if c == "proprietary-tech":
        if re.search(r"hsrp|glbp|0000\.0c07|show glbp", tl): put(r, "3", "3.3 FHRP: HSRP/GLBP → VRRP")
        elif "pagp" in tl: put(r, "3", "3.4 агрегирование: PAgP → LACP")
        elif "etherchannel" in tl: put(r, "K", "K.1 EtherChannel как имя функции и ключевое слово CLI — оставить")
        elif re.search(r"cdp|cisco discovery", tl): put(r, "3", "3.5 обнаружение соседей: CDP → LLDP")
        elif re.search(r"\bdtp\b|dtp", tl): put(r, "3", "3.6 DTP: тема безопасности транков")
        elif re.search(r"\bvtp\b|\bisl\b", tl): put(r, "2", "2.6 мелкие проприетарные упоминания со стандартной заменой")
        elif "pvst" in tl: put(r, "3", "3.7 STP: PVST+/Rapid PVST+")
        elif re.search(r"lwapp|\blap\b|flexconnect", tl):
            put(r, "3", "3.2 WLAN/WLC: GUI контроллера Cisco") if k == "pt-lab" else put(r, "2", "2.6 мелкие проприетарные упоминания со стандартной заменой")
        elif re.search(r"\bcef\b|express forwarding", tl): put(r, "2", "2.5 CEF → пересылка по FIB")
        elif re.search(r"portfast|bpdu|guard|uplinkfast|backbonefast", tl): put(r, "K", "K.2 PortFast/BPDU Guard/Root Guard — ключевые слова CLI, оставить")
        elif re.search(r"eigrp|igrp", tl): put(r, "K", "K.3 EIGRP/IGRP/TACACS+ — открытые описания (RFC), оставить без бренда")
        else: put(r, "K", "K.3 EIGRP/IGRP/TACACS+ — открытые описания (RFC), оставить без бренда")
        continue
    # ---- brand word
    if "[D10]" in n:
        put(r, "1", "1.5 точечные удаления (тег, PDF, заголовки)"); continue
    if s == "lab-infra" and c == "legal":
        put(r, "1", "1.5 точечные удаления (тег, PDF, заголовки)"); continue
    if c == "brand" and tl.startswith("cisco") and s in ("text", "code", "quiz", "metadata"):
        if "cisco-phone" in tl:
            put(r, "1", "1.2 бренд в тексте: убрать или переформулировать", "ключевое слово команды `device cisco-phone` — оставить как синтаксис или убрать пример"); continue
        if "talos" in tl:
            put(r, "1", "1.2 бренд в тексте: убрать или переформулировать", "цитата Cisco Talos → «по данным отраслевых отчётов»"); continue
        hint = next((name for name, rx in BRAND_PATTERNS if re.search(rx, exl)), "прочее (переформулировать вручную)")
        put(r, "1", "1.2 бренд в тексте: убрать или переформулировать", hint); continue
    if c == "brand" and "talos" in tl:
        put(r, "1", "1.2 бренд в тексте: убрать или переформулировать", "цитата Cisco Talos → «по данным отраслевых отчётов»"); continue
    # ---- OS name
    if c == "product" and re.search(r"\bios\b", tl):
        if re.search(r"IOS\s*(XE\s*)?(Release\s*)?(версии\s*)?\d|\d+\.\d\(\d|верси\w*\s+(ОС\s+)?(Cisco\s+)?IOS|IOS\s+\d", ex):
            put(r, "2", "2.2 утверждения о версиях IOS")
        else:
            put(r, "1", "1.4 «IOS / Cisco IOS» как имя ОС")
        continue
    # ---- models & CLI output
    if c == "model" and s in ("text", "quiz", "metadata", "code") or c == "product" and re.search(r"catalyst|\bisr\b|aironet|meraki", tl):
        if k == "pt-lab": put(r, "3", "3.1 лабы PT → learn-netsim")
        elif re.search(r"3504|1815|aironet|wlc|meraki|rv\d|mx64", tl): put(r, "3" if k != "quiz" and "13-wlan" in r["module"] else "2", "3.2 WLAN/WLC: GUI контроллера Cisco" if k != "quiz" and "13-wlan" in r["module"] else "2.1 модели оборудования → NR01/NS01")
        elif s == "code": put(r, "2", "2.3 вендорные строки в выводах CLI → вывод learn-netsim")
        else: put(r, "2", "2.1 модели оборудования → NR01/NS01")
        continue
    if c == "cli-vendor-string":
        put(r, "2", "2.3 вендорные строки в выводах CLI → вывод learn-netsim"); continue
    if c == "certification":
        if "ilm" in tl: continue  # $ref paths — dev-facing
        if re.search(r"srwe", tl): put(r, "1", "1.5 точечные удаления (тег, PDF, заголовки)")
        else: put(r, "2", "2.4 примечание об оборудовании в 5 лабах без PT")
        continue
    if "[D4.10]" in n or c == "product":
        put(r, "2", "2.5б продукты безопасности → классы решений"); continue
    if s == "raster":
        if "1.3.2.png" in r["locator"] or "10.5.10.png" in r["locator"]:
            put(r, "2", "2.3 вендорные строки в выводах CLI → вывод learn-netsim") if "1.3.2" in r["locator"] else put(r, "3", "3.5 обнаружение соседей: CDP → LLDP")
        else:
            put(r, "2", "2.7 растры: перерисовка без изменения смысла")
        continue
    if c == "link":
        put(r, "1", "1.1 значения конфигурации (пароли, домены, имена)"); continue
    put(r, "?", "unsorted")
# text coupled with a raster that shows the same value → move together with the raster (2.7)
for x in rows:
    if x["item"].startswith("1.1") and "01.03-secure-remote-access" in x["locator"] and "ccna" in x["term"].lower():
        x["item"], x["tier"], x["hint"] = "2.7 растры: перерисовка без изменения смысла", "2", "текст связан с растром 1.3.1 (Wireshark, Password: ccna) — менять вместе"  # ggignore: публичный учебный пароль из скриншота курса, не секрет
    if x["item"].startswith("1.1") and "CiscoVille" in x["term"]:
        x["item"], x["tier"], x["hint"] = "2.7 растры: перерисовка без изменения смысла", "2", "вопрос ссылается на растр 01-04-exam/8.png, 9.png, 12.png с тем же именем — менять вместе"
# 2.4: the lab equipment paragraphs in non-PT labs are model+IOS-version+CCNA rows of those labs — re-route
for x in rows:
    if x["kind"] == "nopt-lab" and x["item"] in ("2.1 модели оборудования → NR01/NS01", "2.2 утверждения о версиях IOS"):
        x["item"] = "2.4 примечание об оборудовании в 5 лабах без PT"
c = collections.Counter((x["tier"], x["item"]) for x in rows)
for k, v in sorted(c.items()): print(v, k)
print("brand hints:", collections.Counter(x["hint"] for x in rows if x["item"].startswith("1.2")).most_common())
# final numbering of tier-2 items as published in demarketing-plan.md
REN = {"2.5б продукты безопасности → классы решений": "2.6 продукты безопасности → классы решений",
       "2.6 мелкие проприетарные упоминания со стандартной заменой": "2.7 мелкие проприетарные упоминания со стандартной заменой",
       "2.7 растры: перерисовка без изменения смысла": "2.8 растры и связанный с ними текст: перерисовка без изменения смысла"}
ORDER = {"1": 1, "2": 2, "3": 3, "K": 4, "X": 5}
for x in rows:
    x["item"] = REN.get(x["item"], x["item"])
rows.sort(key=lambda x: (ORDER[x["tier"]], [int(p) if p.isdigit() else p for p in x["item"].split(" ")[0].split(".")], x["id"]))
with open(os.path.join(AUD, "demarketing-tiers.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "tier", "item", "hint", "kind", "surface", "locator", "term"])
    w.writeheader(); w.writerows(rows)
summ = {}
for item in sorted({x["item"] for x in rows}):
    rs = [x for x in rows if x["item"] == item]
    files = collections.Counter(re.split(r":\d|\s\(", x["locator"])[0] for x in rs)
    summ[item] = {"tier": rs[0]["tier"], "rows": len(rs), "files": len(files), "kinds": dict(collections.Counter(x["kind"] for x in rs)),
                  "top_files": files.most_common(12)}
json.dump({"items": summ, "gui_labs": sorted(gui_labs), "pt_labs": sorted(pt_labs), "nopt_labs": sorted(nopt_labs)},
          open(os.path.join(OUT, "plan-summary.json"), "w"), ensure_ascii=False, indent=1)
print("total", len(rows))
