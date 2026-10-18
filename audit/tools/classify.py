# Pass 2: classify every dictionary hit (text files + file/dir names) into map rows or exclusions.
# In: out/hits.json. Out: out/rows_text.json, out/ledger_text.json
import json, os, re, subprocess, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from terms import COMPILED

from common import REPO, WORK, OUT, AUD, tracked_files
hits = json.load(open(os.path.join(OUT, "hits.json")))
files = tracked_files()
fileset = set(files)

# ---------- file/dir-name hits (surface: filename)
names = set()
for f in files:
    parts = f.split("/")
    for i in range(len(parts)):
        names.add("/".join(parts[: i + 1]))
for p in sorted(names):
    comp = p.split("/")[-1]
    for term, rx, cat, origin in COMPILED:
        for m in rx.finditer(comp):
            hits.append({"term": term, "file": p, "line": 0, "col": m.start(), "match": m.group(0),
                         "default_cat": cat, "origin": origin, "in_code": False, "in_comment": False,
                         "inline": None, "question": None, "text": comp, "is_name": True,
                         "is_dir": p not in fileset})

# ---------- helpers
LAB_DIRS = sorted({"/".join(f.split("/")[:2]) for f in files if re.match(r"^[0-9][^/]*/[^/]*-lab-", f)} |
                  {"final-lab-part1", "final-lab-part2"})


def lab_of(f):
    for d in LAB_DIRS:
        if f == d or f.startswith(d + "/"):
            return d
    return None


def module_of(f):
    top = f.split("/")[0]
    if re.match(r"^\d\d-|^final-", top):
        return top
    if top in ("videos",) and f.count("/") >= 1:
        return f.split("/")[1] if f.count("/") >= 2 else "(root)"
    return "(root)"


def material_of(f):
    parts = f.split("/")
    if re.match(r"^\d\d-\d\d-exam$|^final-", parts[0]):
        return parts[0]
    if re.match(r"^\d\d-", parts[0]):
        if len(parts) >= 3:
            return "/".join(parts[:2])
        return parts[0]
    if parts[0] == "videos" and len(parts) == 3:
        mat = parts[2].split("--")[0]
        return parts[1] + "/" + mat
    return "(root)"


def video_id(f):
    m = re.search(r"--([\w-]{11})\.md$", f)
    return m.group(1) if m else None


VIDEO_SECTIONS = {}


def video_section(f, n):
    if f not in VIDEO_SECTIONS:
        secs, cur = [], "header"
        for i, l in enumerate(open(os.path.join(REPO, f), encoding="utf-8").read().split("\n"), 1):
            if l.startswith("## "):
                cur = l[3:].strip()
            secs.append(cur)
        VIDEO_SECTIONS[f] = secs
    return VIDEO_SECTIONS[f][n - 1]


def timecode(text):
    m = re.search(r"\[(\d+:\d\d)\]", text) or re.search(r"^\|\s*(\d+:\d\d(?:[–-]\d+:\d\d)?)", text)
    return m.group(1) if m else None


PROMPT = re.compile(r"^\s*[\w.\-]+(\([\w\-]+\))?[#>]\s*\S|^\s*switch:\s")


def surface_audience(h):
    f = h["file"]
    if h.get("is_name"):
        return "filename", ("internal" if f.startswith((".github", "animations", "readme-assets", "packet-tracer-source-files", "videos")) or "/deploy" in f or "/assessment" in f or f in ("ccna2-labs.md", "migration-instructions.md", "calc_duration.txt", "figma-assets.json") else "learner")
    if f.startswith(".github/") or f in ("migration-instructions.md", "ccna2-labs.md", "calc_duration.txt", ".gitignore"):
        return "internal-doc", "internal"
    if f == "figma-assets.json":
        return "metadata", "internal"
    if f.startswith("animations/"):
        return "animation", "internal"
    if f.startswith("videos/"):
        if f == "videos/README.md":
            return "internal-doc", "internal"
        sec = video_section(f, h["line"])
        if sec in ("Сценарий", "Транскрипт"):
            return "video", "learner"
        return "internal-doc", "internal"
    lab = lab_of(f)
    if lab and ("/deploy/" in f or "/assessment/" in f or f.endswith("assessment.json")):
        return "lab-infra", "internal"
    if f.endswith("learn-metadata.json"):
        if re.search(r'"title":\s*"\d+\.', h["text"]) and lab_of(f):
            return "quiz", "learner"
        if h["question"]:
            return "quiz", "learner"
        return "metadata", "learner"
    if f in ("README.md", "material-tags.json"):
        return "metadata", "learner"
    if f.endswith("README.md"):
        if f.count("/") == 1:  # module description
            return "metadata", "learner"
        if h["in_comment"]:
            return "comment", "internal"
        if h["in_code"]:
            return "code", "learner"
        return "text", "learner"
    return "internal-doc", "internal"


FEATURE_TERMS = {"EtherChannel", "PortFast", "BPDU Guard", "Root/Loop Guard", "UplinkFast/BackboneFast"}
PROTO_TERMS = {"CDP", "EIGRP", "HSRP", "GLBP", "VTP", "DTP", "ISL", "PVST", "PAgP", "CEF", "LWAPP/LAP",
               "FlexConnect", "SPAN/RSPAN", "UDLD", "TACACS+"}


def exclusion(h, surface):
    """Return a reason string if the hit is excluded (K), else None."""
    t, s, m, f = h["term"], h["text"], h["match"], h["file"]
    lo = s.lower()
    if f.startswith("videos/"):
        return "видео вне аудита по указанию оператора: уже классифицированы (videos/README.md) и будут пересобраны"
    # --- false positives
    if t == "ensa" and re.search(r"compensat", lo):
        return "ложное совпадение: подстрока слова (Compensates)"
    if t == "c\\d{4} (image/platform)" and re.search(r"[0-9a-f]{12}", m.lower() + lo[h["col"]:h["col"] + 14]) and not re.search(r"c\d{4}-", lo[h["col"]:]):
        if re.match(r"c\d{4}[0-9a-f]{4,}", m.lower()):
            return "ложное совпадение: шестнадцатеричный адрес (MAC/Neighbor address)"
    if t == "SPAN/RSPAN" and f.endswith(".py"):
        return "ложное совпадение: имя переменной span в коде скрипта"
    if t == "SPAN/RSPAN" and re.search(r"begin span", lo):
        return "синтаксис CLI: фильтр вывода `| begin span` (span = начало слова spanning-tree)"
    if t == "PT" and re.search(r"PT Mono", s):
        return "ложное совпадение: шрифт PT Mono (ParaType), не Packet Tracer"
    if t == "v7" and f == "figma-assets.json":
        return "ложное совпадение: подстрока идентификатора/хеша"
    if t == "c\\d{4} (image/platform)" and f == "figma-assets.json":
        return "ложное совпадение: подстрока идентификатора ассета ccna2-…"
    if t == "itn" and not re.search(r"itn-|\bitn\b", lo):
        return "ложное совпадение: подстрока слова"
    # --- CLI syntax: feature keywords kept by the IOS-style CLI (learn-netsim keeps the syntax)
    if t in FEATURE_TERMS:
        if h["in_code"] and surface in ("code", "video", "comment"):
            return "синтаксис CLI в стиле IOS: команда или ключевое слово вывода (сохраняется в learn-netsim)"
        if h["inline"] and re.search(r"(spanning-tree|show|channel|interface|port-channel|errdisable|bpduguard|portfast|guard)", h["inline"].lower()) and not re.search(r"[а-я]", h["inline"].lower()):
            return "синтаксис CLI в стиле IOS: команда в тексте (`…`/**…**), сохраняется в learn-netsim"
        if surface == "quiz" and re.search(r'"answer":\s*"[^а-яА-Я"]*(spanning-tree|show|channel-group|interface|port-channel)', s):
            return "синтаксис CLI в стиле IOS: вариант ответа — команда"
        if surface == "quiz" and re.search(r"(S\d|Sw\w*|R\d)\(config[\w-]*\)#[^\"]*" + re.escape(m.lower()), lo) and not re.search(r"[а-я]{4,}[^\"]*" + re.escape(m.lower()), lo[:h["col"] + 1].split("#")[-1]):
            return "синтаксис CLI в стиле IOS: команда в тексте вопроса"
    return None


ROUTER_MODELS = {"1941", "2901", "2911", "4221", "4321", "4331", "1841", "2811"}
SWITCH_MODELS = {"2960", "2950", "3560", "3550", "3650", "3750", "3850"}


def hit_category(h, surface):
    t, s, m = h["term"], h["text"], h["match"]
    lo = s.lower()
    cat = h["default_cat"]
    if t == "cisco":
        tail = lo[h["col"]:h["col"] + 30]
        if tail.startswith("cisco discovery protocol") or tail.startswith("cisco express forwarding"):
            return "proprietary-tech"
        if tail.startswith("cisco.com") or re.match(r"cisco\.com", tail):
            return "link"
    if t in ("netacad",) and re.match(r"netacad\.(com|pka|pt)", lo[h["col"]:]):
        return "link" if lo[h["col"]:].startswith("netacad.com") else "brand"
    if t in ("models", "models+"):
        return "model"
    if t == "LWAPP/LAP" and re.search(r"\bLAP-PT\b", s):
        return "product"
    if t == "PT" and re.search(r"non[ -]PT", s, re.I):
        return "product"
    if t == "youtube":
        return "link"
    if t == "cisco" and re.search(r"domain|домен", lo) and re.match(r"cisco\.com", lo[h["col"]:]):
        return "brand"
    if t == "cisco.com" and re.search(r"domain|домен", lo):
        return "brand"
    if surface == "code" and cat in ("brand", "product", "model") and not PROMPT.search(s):
        if re.search(r"host name|имя узла|hostname", lo):
            return "brand"
        return "cli-vendor-string"
    return cat


PRIORITY = ["legal", "link", "cli-vendor-string", "model", "proprietary-tech", "product", "brand",
            "certification", "lab-infra", "visual"]

ROUTER_RX = re.compile(r"\b(1941|2901|2911|4221|4321|4331|1841|2811)\b|ISR\d{4}")
SWITCH_RX = re.compile(r"\b(2960s?|2950|3560|3550|3650|3750|3850)\b|WS-C")
L3_RX = re.compile(r"\b(3560|3650|3750|3850)\b")
CRED_RX = re.compile(r"password|secret|пароль|парол|passphrase|key-string|community|username|login|логин", re.I)



def token_at(text, col, mlen):
    a, b = col, col + mlen
    while a > 0 and not text[a - 1].isspace() and text[a - 1] not in "*`\"'«»|(":
        a -= 1
    while b < len(text) and not text[b].isspace() and text[b] not in "*`\"'«»|),;":
        b += 1
    return text[a:b].strip(".,:;!?") if text[a:b].strip(".,:;?").lower() not in ("cisco!",) else text[a:b]


def value_kind(h):
    """'cred' | 'host' | 'cli-keyword' | 'domain' | None for brand/cert words used as config values."""
    t = token_at(h["text"], h["col"], len(h["match"]))
    tl = t.lower()
    word = h["match"].lower()
    lo = h["text"].lower()
    if re.fullmatch(r"cisco-phone", tl):
        return "cli-keyword", t
    if re.search(r"\.(pka|pt|com|lab|local)\b|\.lab-", tl) or re.search(r"domain|домен", lo) and ("." in tl):
        return "domain", t
    if tl == word:
        if h["match"].islower() and CRED_RX.search(lo):
            return "cred", t
        if h["match"].islower() and h.get("in_code") and re.search(r"password|secret|login|username", lo):
            return "cred", t
        return None, t
    if re.fullmatch(r"cisco[-_][a-z]+", tl) and not re.search(r"\d", tl) and t[0].isupper():
        return None, t  # Cisco-FHRP, Cisco_98:8c:95 handled below
    if re.match(r"cisco_[0-9a-f]{2}:", tl):
        return "oui", t
    if re.search(r"ville|lab$|sb\d|^ciscolab", tl):
        return "host", t
    return "cred", t


def action_note(cat, terms, text, surface, audience, f):
    """Proposed action + note (decision ids D1..D14, see vendor-mentions.md)."""
    lo = text.lower()
    tset = set(terms)
    labdir = lab_of(f)
    if audience == "internal" and surface in ("internal-doc", "metadata", "animation", "filename") and cat not in ("legal",):
        if surface == "filename":
            pass
        elif f == "figma-assets.json" or f.startswith("animations/"):
            return "decide", "[D1] служебный идентификатор/имя страницы Figma с «CCNA2»; переименование ломает контракт Figma↔git — решать вместе с именем курса"
        elif f.startswith(".github/"):
            return "keep", "[D10] ссылка на соседний репозиторий learn-ccnaN в комментарии кода; меняется только при переименовании репозиториев (D1)"
        elif f.startswith("videos/"):
            return "keep", "[D6] наш служебный документ описывает исходный ролик NetAcad; устареет после пересборки видео"
        else:
            return "decide", "[D10] служебный документ (не показывается обучающемуся); чистить, если репозиторий/документ станет публичным"
    if cat == "legal":
        return "remove", "знак/копирайт вендора"
    if cat == "link":
        if any("youtu" in t.lower() for t in tset) and "watch?v=" not in lo:
            return "neutralize", "[D6] фраза о переходе на YouTube к ролику NetAcad; переписать после пересборки видео"
        if any("youtu" in t.lower() for t in tset):
            return "replace:<пересобранное видео (см. D6)>", "[D6] встраивание ролика NetAcad (перезалив на канале оператора); после пересборки — заменить ссылку"
        if re.search(r"domain|домен", lo):
            return "replace:<нейтральный домен, напр. example.com>", "[D12] cisco.com как пример доменного имени в конфигурации — не ссылка, а значение"
        return "remove", "ссылка на ресурс вендора"
    if cat == "cli-vendor-string":
        return "replace:<эквивалентный вывод NSALAB NetOS>", "[D3] вендорная строка в выводе CLI (баннер/платформа/образ); заменить на вывод learn-netsim (NetOS, NR01/NS01)"
    if cat == "model":
        jt = " ".join(terms)
        if ROUTER_RX.search(jt) and SWITCH_RX.search(jt):
            return "replace:NR01 (маршрутизатор) / NS01 (коммутатор)", "[D2] в строке и маршрутизатор, и коммутатор вендора → NR01 / NS01"
        if ROUTER_RX.search(jt) and not SWITCH_RX.search(jt):
            return "replace:NR01", "[D2] модель маршрутизатора → NR01 (NR02 при второй модели в той же топологии)"
        if L3_RX.search(" ".join(terms)):
            return "replace:NS01 (L3)", "[D2] L3-коммутатор → NS01; уточнить, поддерживает ли NS01 маршрутизацию (SVI, ip routing)"
        if SWITCH_RX.search(" ".join(terms)):
            return "replace:NS01", "[D2] модель коммутатора → NS01"
        if re.search(r"3504|1815|aironet|wlc", " ".join(terms).lower() + lo):
            return "neutralize", "[D2] модель WLC/AP — в идентичности learn-netsim аналога нет; писать «контроллер WLC»/«точка доступа»"
        if re.search(r"universalk9|lanbase|ipbase|\bc\d{4}", " ".join(terms).lower()):
            return "replace:<имя образа NetOS>", "[D3] имя образа/платформы IOS → образ NetOS"
        if re.search(r"\d+\.\d\(\d", " ".join(terms)):
            return "neutralize", "[D3] версия IOS — убрать или заменить версией NetOS"
        if re.search(r"rv\s?\d{3}|mx64|wrt\d", " ".join(terms).lower()):
            return "neutralize", "[D2] модель SOHO-роутера вендора → «беспроводной роутер SOHO»"
        return "replace:NR01/NS01", "[D2] модель оборудования → идентичность learn-netsim"
    if cat == "product":
        tl = " ".join(terms).lower()
        if "packet" in tl or tl.strip() in ("pt",) or re.search(r"\bpt\b", tl):
            if surface == "comment":
                return "remove", "[D5] закомментированная ссылка «Скачать файл Packet Tracer» на .pka"
            if labdir and re.search(r"13-wlan|12-wlan|physical-mode|09.03.04", f):
                return "decide", "[D5] лаба опирается на GUI Packet Tracer (WLC/физический режим/беспроводные устройства); прямой замены в learn-netsim нет"
            return "replace:симулятор learn-netsim", "[D5] Packet Tracer → «симулятор» (learn-netsim), см. decisions/packet-tracer-substitution.md"
        if re.search(r"\bios\b", tl):
            return "replace:NetOS", "[D3] Cisco IOS как название ОС → NSALAB NetOS (или нейтрально «ОС устройства»)"
        if "catalyst" in tl:
            return "neutralize", "[D2] серия коммутаторов вендора → «коммутатор» (NS01 в лабах)"
        if "isr" in tl:
            return "neutralize", "[D2] серия маршрутизаторов вендора → «маршрутизатор» (NR01 в лабах)"
        if "linksys" in tl:
            return "neutralize", "[D5] устройство PT Linksys WRT300N → «беспроводной роутер»"
        if "lap" in tl:
            return "decide", "[D5] устройство Packet Tracer LAP-PT (облегчённая AP) — зависит от решения по WLAN-лабам"
        return "neutralize", "[D4.10] продукт вендора → назвать класс решения без бренда"
    if cat == "brand":
        if f == "material-tags.json":
            return "remove", "[D11] тег «Cisco» наследуют все материалы курса через $ref"
        vk = CURRENT.get("vk")
        if vk == "cred":
            return "replace:<нейтральный пароль>", "[D12] «cisco…» как пароль/ключ/учётные данные; в лабах менять синхронно с .pka и assessment"
        if vk == "host":
            return "replace:<нейтральное имя>", "[D12] имя хоста/SSID/сети с «cisco»; в лабах менять синхронно с .pka и assessment"
        if vk == "domain":
            return "replace:<нейтральный домен, напр. example.com>", "[D12] домен/URL с брендом как значение конфигурации (в PT-лабах — сервер внутри .pka); менять синхронно с топологией"
        if vk == "cli-keyword":
            return "decide", "[D3] вендорное ключевое слово команды IOS (`mls qos trust device cisco-phone`) — оставить как синтаксис или убрать пример"
        if vk == "oui":
            return "neutralize", "[D6] OUI вендора в выводе Wireshark (Cisco_xx:xx:xx) — при пересборке заменить нейтральным MAC"
        if re.search(r"netacad|networking academy|академи", " ".join(terms).lower()):
            return "remove", "[D13] упоминание Сетевой академии Cisco"
        return "neutralize", "бренд вендора — переписать без бренда (часто достаточно удалить слово)"
    if cat == "certification":
        tl = " ".join(terms).lower()
        vk = CURRENT.get("vk")
        if vk in ("cred", "host", "domain") or re.search(r"ccnav7", tl):
            return "replace:<нейтральное значение>", "[D12] «CCNA» как пароль/домен/имя/SNMP community — значение конфигурации; в лабах менять синхронно с .pka и assessment"
        if "ilm" in tl:
            return "decide", "[D10] суффикс -ilm (Instructor Lab Manual NetAcad) в имени каталога/ссылке; переименование меняет путь материала"
        if "srwe" in tl:
            return "replace:<код курса NSALAB>", "[D1] код курса NetAcad SRWE в shortName/заголовке"
        return "neutralize", "[D1] упоминание сертификации/кода курса вендора"
    if cat == "proprietary-tech":
        return "decide", PROTO_NOTES.get(terms[0], "[D4.9] проприетарная технология вендора")
    if cat == "lab-infra":
        if surface == "comment":
            return "remove", "[D5] закомментированная ссылка на .pka"
        return "replace:learn-netsim", "[D5] зависимость от Packet Tracer"
    return "decide", ""


PROTO_NOTES = {
    "CDP": "[D4.1] CDP — проприетарный; рекомендация: основным протоколом обнаружения сделать LLDP (IEEE 802.1AB), CDP оставить только как пример в теме атак (10.5/11.x) без бренда",
    "EIGRP": "[D4.6] EIGRP (RFC 7868, informational); рекомендация: оставить как пример динамической маршрутизации без слова Cisco",
    "HSRP": "[D4.4] HSRP — проприетарный FHRP; рекомендация: основным сделать VRRPv3 (RFC 5798), HSRP упомянуть; лаба 9.3.3 построена на HSRP",
    "GLBP": "[D4.4] GLBP — проприетарный FHRP; рекомендация: упомянуть как пример балансировки, без бренда",
    "VTP": "[D4.2] VTP — проприетарный; рекомендация: оставить кратко (влияет на VLAN расширенного диапазона) без бренда или убрать",
    "DTP": "[D4.2] DTP — проприетарный; рекомендация: оставить как тему безопасности («автосогласование транка», 3.5, 10.5, 11.x), подать нейтрально",
    "ISL": "[D4.2] ISL — устаревший проприетарный транк; рекомендация: убрать, оставить только 802.1Q",
    "PVST": "[D4.3] PVST+/Rapid PVST+ — проприетарные варианты STP; рекомендация: подать как «STP на каждую VLAN», упомянуть MSTP (802.1s); команды `spanning-tree mode rapid-pvst` — синтаксис",
    "PAgP": "[D4.5] PAgP — проприетарный; рекомендация: основным сделать LACP (IEEE 802.1AX), PAgP упомянуть",
    "CEF": "[D4.7] CEF — проприетарный механизм пересылки; рекомендация: описывать FIB + таблицу смежности, CEF — как пример",
    "LWAPP/LAP": "[D4.8] LWAPP/LAP — проприетарные термины; рекомендация: CAPWAP (RFC 5415) и «облегчённая AP» без бренда",
    "FlexConnect": "[D4.8] FlexConnect — функция WLC вендора; рекомендация: «локальная коммутация на AP (split MAC/local mode)»",
    "SPAN/RSPAN": "[D4.9] SPAN — термин вендора для зеркалирования портов; рекомендация: «зеркалирование портов (port mirroring)»",
    "UDLD": "[D4.9] UDLD (RFC 5171, informational); рекомендация: оставить как есть",
    "TACACS+": "[D4.9] TACACS+ описан в RFC 8907 — де-факто открытый; рекомендация: keep",
    "EtherChannel": "[D4.5] EtherChannel — торговое название вендора для агрегирования каналов; рекомендация: «агрегирование каналов (LAG, IEEE 802.1AX)», EtherChannel — как синоним; ключевые слова команд — синтаксис",
    "PortFast": "[D4.3] PortFast — название функции вендора; стандартный аналог — edge port (802.1D-2004/802.1w); рекомендация: оставить как ключевое слово CLI, в тексте дать стандартный термин",
    "BPDU Guard": "[D4.3] BPDU Guard — название функции вендора; рекомендация: оставить как ключевое слово CLI, пояснить нейтрально",
    "Root/Loop Guard": "[D4.3] Root/Loop Guard — функции вендора; рекомендация: оставить как ключевые слова CLI",
    "UplinkFast/BackboneFast": "[D4.3] UplinkFast/BackboneFast — устаревшие функции вендора; рекомендация: убрать (в RSTP встроено)",
}


CURRENT = {}


def rec_action(cat, terms, text, surface, audience, f):
    a, n = action_note(cat, terms, text, surface, audience, f)
    if cat == "proprietary-tech":
        t0 = terms[0]
        if t0 == "TACACS+" or t0 == "UDLD":
            a = "keep"
        elif t0 == "ISL" or t0 == "UplinkFast/BackboneFast":
            a = "decide"
    return a, n


# ---------- classify hits
ledger = []
rows = []
groups = collections.OrderedDict()  # (file,line,category) -> list of hits
LAB_AGG = collections.OrderedDict()
FIGMA_AGG = collections.OrderedDict()
NAME_AGG = collections.OrderedDict()
INTERNAL_AGG = collections.OrderedDict()

for i, h in enumerate(hits):
    h["hid"] = i
    surface, audience = surface_audience(h)
    h["surface"], h["audience"] = surface, audience
    reason = exclusion(h, surface)
    if reason:
        ledger.append({**{k: h[k] for k in ("term", "file", "line", "match")}, "disposition": "excluded", "reason": reason})
        continue
    cat = hit_category(h, surface)
    h["cat"] = cat
    f = h["file"]
    if surface == "lab-infra" or (h.get("is_name") and lab_of(f) and "/deploy" in f):
        LAB_AGG.setdefault(lab_of(f), []).append(h)
    elif f == "figma-assets.json" or f.startswith("animations/"):
        FIGMA_AGG.setdefault((f if f == "figma-assets.json" else "animations/*", h["term"], cat), []).append(h)
    elif h.get("is_name"):
        NAME_AGG.setdefault((h["file"], cat), []).append(h)
    elif surface == "internal-doc" and f in ("ccna2-labs.md", "calc_duration.txt") :
        INTERNAL_AGG.setdefault((f, h["term"], cat), []).append(h)
    else:
        groups.setdefault((f, h["line"]), []).append(h)


def excerpt(text, col, width=160):
    s = text.strip()
    if len(s) <= width:
        return s
    off = len(text) - len(text.lstrip())
    c = max(0, col - off - 60)
    return ("…" if c > 0 else "") + s[c:c + width - 2] + "…"


def add_row(r, hs):
    r["_hits"] = [h["hid"] for h in hs]
    rows.append(r)


def phrases(hs):
    hs = sorted(hs, key=lambda h: (h["col"], -len(h["match"])))
    out, cur, end = [], [], -1
    for h in hs:
        s = h["text"]
        if cur and (h["col"] <= end or (h["col"] - end <= 2 and re.fullmatch(r"[\s/\-(]*", s[end:h["col"]]))):
            cur.append(h); end = max(end, h["col"] + len(h["match"]))
        else:
            if cur: out.append(cur)
            cur, end = [h], h["col"] + len(h["match"])
    if cur: out.append(cur)
    return out


for (f, n), hl in groups.items():
    bycat = collections.OrderedDict()
    for ph in phrases(hl):
        cats = [h["cat"] for h in ph]
        cat = min(cats, key=lambda c: PRIORITY.index(c) if c in PRIORITY else 99)
        bycat.setdefault(cat, []).append(ph)
    for cat, phs in bycat.items():
        hs = [h for ph in phs for h in ph]
        text = hs[0]["text"]
        terms = []
        for ph in phs:
            a = min(h["col"] for h in ph); b = max(h["col"] + len(h["match"]) for h in ph)
            t = text[a:b]
            if t not in terms:
                terms.append(t)
        termkeys = []
        for h in hs:
            if h["term"] not in termkeys:
                termkeys.append(h["term"])
        surface, audience = hs[0]["surface"], hs[0]["audience"]
        loc = f"{f}:{n}"
        vid = video_id(f)
        if vid and surface == "video":
            tc = timecode(text)
            loc = f"{f}:{n} (videoId {vid}" + (f" @ {tc})" if tc else ")")
        if hs[0]["question"] and surface == "quiz":
            loc += f" (вопрос #{hs[0]['question']})"
        elif surface == "quiz":
            mq = re.search(r'"title":\s*"(\d+)\.', text)
            if mq:
                loc += f" (answerSchema q_{mq.group(1)})"
        vks = [value_kind(h) for h in hs if h["term"] in ("cisco", "ccna", "netacad") and surface != "internal-doc"]
        CURRENT["vk"] = next((k for k, _ in vks if k), None)
        vtoks = [tk for k, tk in vks if k]
        if vtoks:
            terms = list(dict.fromkeys(vtoks))
        if cat == "proprietary-tech":
            pk = [k for k in termkeys if k in PROTO_TERMS or k in FEATURE_TERMS] or termkeys
            a, note = rec_action(cat, pk, text, surface, audience, f)
        else:
            a, note = rec_action(cat, terms, text, surface, audience, f)
        if surface == "video" and cat not in ("proprietary-tech",):
            if CURRENT.get("vk") in ("cred", "host"):
                a, note = "replace:<нейтральный пароль/имя>", "[D6][D12] реплика/кадр исходного ролика NetAcad: «cisco»/«Cisco123» как учётные данные или имя; при пересборке заменить"
            else:
                a, note = "neutralize", "[D6] реплика/кадр исходного ролика NetAcad; при пересборке видео — без бренда/модели/продукта"
        add_row({"module": module_of(f), "material": material_of(f), "surface": surface, "locator": loc,
                 "term": "; ".join(terms), "category": cat, "audience": audience,
                 "excerpt": excerpt(text, hs[0]["col"]), "action": a, "note": note,
                 "_file": f, "_line": n, "_terms": termkeys}, hs)

# internal-doc aggregates (tables with one hit per line)
for (f, term, cat), hs in INTERNAL_AGG.items():
    lines = sorted({h["line"] for h in hs})
    a, note = action_note(cat, [term], hs[0]["text"], "internal-doc", "internal", f)
    add_row({"module": "(root)", "material": "(root)", "surface": "internal-doc",
             "locator": f"{f}:" + ",".join(map(str, lines)), "term": f"{term} ×{len(hs)}", "category": cat,
             "audience": "internal", "excerpt": excerpt(hs[0]["text"], hs[0]["col"]),
             "action": a, "note": note + f" (агрегировано: {len(lines)} строк таблицы)",
             "_file": f, "_line": lines[0], "_terms": [term]}, hs)

# figma manifest / animation spec aggregates
for (f, term, cat), hs in FIGMA_AGG.items():
    lines = sorted({h["line"] for h in hs})
    files_ = sorted({h["file"] for h in hs})
    matches = collections.Counter(h["match"] for h in hs)
    if f == "figma-assets.json":
        kinds = collections.Counter()
        for h in hs:
            s = h["text"]
            if '"id"' in s: kinds["id ассета"] += 1
            elif '"page"' in s: kinds["page Figma"] += 1
            elif '"path"' in s: kinds["out.path"] += 1
            elif '"course"' in s: kinds["course"] += 1
            else: kinds["прочее"] += 1
        loc = f"figma-assets.json:{lines[0]}…{lines[-1]} ({len(lines)} строк)"
        exc = "; ".join(f"{k} ×{v}" for k, v in kinds.most_common()) + " — пример: " + hs[0]["text"].strip()[:80]
    else:
        loc = ", ".join(sorted({x.split('/')[1] for x in files_}))[:200] + f" ({len(files_)} файлов spec/tracks)"
        exc = hs[0]["text"].strip()[:150]
    if cat == "proprietary-tech":
        a, note = "keep", "[D7] служебное поле (путь/имя страницы/текст спецификации анимации); меняется вместе с текстом материала"
    else:
        a, note = action_note(cat, [term], hs[0]["text"], "metadata", "internal", f)
    add_row({"module": "(root)" if f == "figma-assets.json" else "(анимации)", "material": "(root)",
             "surface": "metadata" if f == "figma-assets.json" else "animation", "locator": loc,
             "term": ", ".join(f"{k} ×{v}" for k, v in matches.most_common(4)), "category": cat, "audience": "internal",
             "excerpt": exc[:160], "action": a, "note": note, "_file": f, "_line": lines[0], "_terms": [term]}, hs)

# filename aggregates
for (p, cat), hs in NAME_AGG.items():
    terms = []
    for h in hs:
        if h["match"] not in terms:
            terms.append(h["match"])
    termkeys = sorted({h["term"] for h in hs})
    isdir = hs[0].get("is_dir")
    if p.endswith(".pka"):
        a, note = "replace:learn-netsim", "[D5] файл Packet Tracer; учтён в строке лабы (lab-infra)"
    elif p.startswith("packet-tracer-source-files"):
        a, note = "decide", "[D5] исходные инструкции PT (.docx); см. строки lab-infra по файлам"
    elif p.startswith("animations/"):
        a, note = "decide", "[D1] каталог анимации назван по id ассета ccna2-…"
    elif cat == "proprietary-tech":
        a, note = "decide", "[D10] имя каталога/файла содержит название технологии вендора; переименование меняет путь материала — " + PROTO_NOTES.get(termkeys[0], "")[:80]
    elif "ilm" in [t.lower() for t in terms]:
        a, note = "decide", "[D10] суффикс -ilm (Instructor Lab Manual NetAcad) в имени каталога; переименование меняет путь материала"
    elif cat == "product" and re.search(r"non-pt", p):
        a, note = "decide", "[D10] суффикс -non-pt (не Packet Tracer) в имени каталога"
    else:
        a, note = "decide", "[D10] имя файла/каталога с упоминанием вендора/курса"
    add_row({"module": module_of(p), "material": material_of(p) if not isdir else (p if p.count('/') <= 1 else material_of(p)),
             "surface": "filename", "locator": p + ("/" if isdir else ""), "term": "; ".join(terms), "category": cat,
             "audience": hs[0]["audience"], "excerpt": p.split("/")[-1][:160], "action": a, "note": note,
             "_file": p, "_line": 0, "_terms": termkeys}, hs)

# lab-infra: one row per lab
lab_artifacts = {}
for d in LAB_DIRS:
    fl = [f for f in files if f.startswith(d + "/")]
    pka = [f for f in fl if f.endswith(".pka")]
    tf = [f for f in fl if f.endswith((".tf", ".tpl", ".sh"))]
    ms = [f for f in fl if "/assessment/" in f or f.endswith("assessment.json")]
    lab_artifacts[d] = (pka, tf, ms, fl)
for d in LAB_DIRS:
    hs = LAB_AGG.get(d, [])
    pka, tf, ms, fl = lab_artifacts[d]
    tc = collections.Counter(h["term"] for h in hs)
    if pka:
        parts = [f"{os.path.relpath(pka[0], d)}", f"deploy/pt-lab: {len([x for x in tf if '/pt-lab/' in x])} файлов .tf/.tpl/.sh (VM с PT, pt-url, pt-api-port)"]
        if ms:
            parts.append("assessment/ms.yaml: «Register packet tracer aspect mark», http://{pt-url}:{pt-api-port}")
        term = "PT-лаба: " + "; ".join(parts)
        a = "replace:learn-netsim"
        note = "[D5] лаба целиком на Packet Tracer (.pka + VM pt-lab + оценка через PT API); перевод на learn-netsim — отдельной задачей. Попадания словаря: " + ", ".join(f"{k} ×{v}" for k, v in tc.most_common())
        if re.search(r"13-wlan|physical-mode|09.03.04", d):
            a = "decide"
            note = "[D5] PT-лаба с GUI-зависимостью (WLC/беспроводные устройства/физический режим PT) — прямого аналога в learn-netsim нет; " + note[5:]
    else:
        term = "лаба без PT-артефактов: deploy/*.tf — Azure resource group/учётка, без устройств; оценки нет"
        a = "decide"
        note = "[D5] бывшая лаба на реальном оборудовании NetAcad (Cisco 4221/2960 в тексте); среды выполнения нет — решить: перевести на learn-netsim или убрать"
        if tc:
            note += ". Попадания словаря: " + ", ".join(f"{k} ×{v}" for k, v in tc.most_common())
    add_row({"module": module_of(d), "material": d, "surface": "lab-infra", "locator": d + "/deploy/ + assessment/",
             "term": term[:300], "category": "lab-infra", "audience": "internal",
             "excerpt": ", ".join(sorted({os.path.relpath(x, d) for x in pka + ms}))[:160] or "deploy/main.tf, outputs.tf, policies.tf, variables.tf",
             "action": a, "note": note, "_file": d, "_line": 0, "_terms": list(tc)}, hs)

# ledger for map rows
for r in rows:
    pass
covered = {}
for ri, r in enumerate(rows):
    for hid in r["_hits"]:
        covered[hid] = ri
for h in hits:
    if h["hid"] in covered:
        ledger.append({**{k: h[k] for k in ("term", "file", "line", "match")}, "disposition": "row", "row": covered[h["hid"]]})
json.dump(rows, open(os.path.join(OUT, "rows_text.json"), "w"), ensure_ascii=False, indent=0)
json.dump(ledger, open(os.path.join(OUT, "ledger_text.json"), "w"), ensure_ascii=False)
print(len(hits), "hits;", len(rows), "rows;", sum(1 for l in ledger if l["disposition"] == "excluded"), "excluded;",
      sum(1 for l in ledger if l["disposition"] == "row"), "covered")
print(collections.Counter(r["category"] for r in rows))
print(collections.Counter(r["surface"] for r in rows))
print(collections.Counter(r["action"].split(":")[0] for r in rows))
