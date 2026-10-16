# Pass 5: audit/vendor-mentions.md from stats + rows.
import csv, json, os, re, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
from terms import TERMS

from common import REPO, WORK as S, tracked_files
st = json.load(open(os.path.join(S, "out", "stats.json")))
R = list(csv.DictReader(open(os.path.join(S, "audit", "vendor-mentions.csv"), encoding="utf-8")))
files = tracked_files()
head = subprocess.check_output(["git", "-C", REPO, "rev-parse", "--short", "HEAD"]).decode().strip()
head_date = subprocess.check_output(["git", "-C", REPO, "log", "-1", "--format=%cs"]).decode().strip()


def ids(pred, limit=6):
    L = [r["id"] for r in R if pred(r)]
    s = ", ".join(L[:limit])
    return s + (f" … (+{len(L) - limit})" if len(L) > limit else "")


def cnt(pred):
    return sum(1 for r in R if pred(r))


def has(code):
    return lambda r: f"[{code}]" in r["note"]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def one(pred):
    L = [r["id"] for r in R if pred(r)]
    assert len(L) == 1, L
    return L[0]
ID_TAG = one(lambda r: r["locator"].startswith("material-tags.json:"))
ID_PDF = one(lambda r: "4.2.8-lab---" in r["locator"] and r["surface"] == "lab-infra")
ID_LIB = one(lambda r: r["surface"] == "figma-library")
ID_COURSE = one(lambda r: "learn-ccna2" in r["term"])
ID_STRUCT = one(lambda r: "SRWE v7 Scope" in r["term"])
ID_LEGAL = one(lambda r: "перевод/адаптация" in r["term"])
ID_FL = [r["id"] for r in R if r["material"].startswith("final-lab-part") and r["category"] == "certification"]
labs = [r for r in R if r["surface"] == "lab-infra" and r["category"] == "lab-infra" and "лаба" in r["term"].lower()]
pt_labs = [r for r in labs if r["term"].startswith("PT-лаба")]
gui = [r for r in pt_labs if r["action"] == "decide"]
nopt = [r for r in labs if not r["term"].startswith("PT-лаба")]


def fam(r):
    t, l = r["term"], r["locator"]
    if "иконки сети" in t: return "netacad-icons"
    if "логической топологии" in t: return "pt-topo"
    if "лабораторного руководства" in t: return "labmanual"
    if any(x in l for x in ("1.3.1.png", "1.3.2.png", "10.5.10.png")): return "wireshark"
    if any(x in l for x in ("1.1.3.png", "12.2.4.png", "13.1.2-1.png", "13.2.6-1.png", "13.4.4-1.png")): return "photo"
    if any(x in l for x in ("10.2.2.png", "13.1.6.png", "13.1.8.png")): return "netacad-fig"
    if "exam/assets" in l: return "cli"
    if "Packet Tracer" in t or "PT" in t or "WRT300N" in t: return "pt-gui"
    return "wlc"
FAM = collections.Counter(fam(r) for r in R if r["surface"] == "raster")
md = []
A = md.append
A("# Аудит упоминаний вендора в курсе CCNA2 (SRWE) — сводка")
A("")
A(f"Ответ на [nsalab-tmn/learn-ccna2#21](https://github.com/nsalab-tmn/learn-ccna2/issues/21). Срез: `{head}` ({head_date}). "
  "В материалах ничего не менялось — добавлен только каталог `audit/`.")
A("")
A("Файлы:")
A("")
A(f"- `audit/vendor-mentions.csv` — карта: **{len(R)} строк**, колонки по issue (`id … note`).")
A("- `audit/dictionary-hits.csv` — журнал **каждого** попадания словаря (текст, имена файлов, OCR картинок, текст `.docx`/`.pdf`): строка карты или «исключено» с причиной. По нему сходится N = M + K.")
A("- `audit/vendor-mentions.md` — этот отчёт.")
A("")
A("Как читать `note`: в начале стоит код решения `[D…]` из раздела «Решения для оператора». `action: decide` почти всегда ссылается на такой код — решать нужно по коду, а не построчно.")
A("")
A("## 1. Главное")
A("")
learner = cnt(lambda r: r["audience"] == "learner")
A(f"- В карте {len(R)} мест: {learner} видит обучающийся, {len(R) - learner} служебные. "
  f"Больше всего проприетарных технологий ({dict(st['by_category'])['proprietary-tech']}): это темы курса — EtherChannel/PAgP, HSRP/GLBP, DTP/VTP, PVST+, CDP. "
  f"За ними бренд ({dict(st['by_category'])['brand']}) и продукты ({dict(st['by_category'])['product']}, в основном Cisco IOS и Packet Tracer).")
A(f"- **Проще всего**: убрать тег `\"Cisco\"` в `material-tags.json` (одна строка, {ID_TAG} — тег наследуют все материалы); "
  f"убрать 38 закомментированных ссылок «Скачать файл Packet Tracer» (`surface=comment`); "
  f"убрать PDF NetAcad со знаком © в материале 04.02 ({ID_PDF} — единственный чужой документ, доступный обучающемуся); "
  f"заменить «cisco»/«ccna»/«netacad» в паролях, доменах и именах хостов ({cnt(has('D11'))} строк, D11).")
A("- **Дороже всего**:")
A(f"  - {len(pt_labs)} лаб на Packet Tracer (D5), из них {len(gui)} завязаны на GUI PT (WLC, беспроводные устройства, физический режим PT);")
A("  - около 160 растров чужого стиля (D8): экзаменационные схемы NetAcad, скриншоты GUI WLC с логотипом, скриншоты PT;")
A("  - проприетарные протоколы как темы целых модулей 06 и 09 (D4).")
A("- **Иллюстрации из Figma (SVG) почти чистые**: логотипов, надписей вендора и узнаваемых панелей моделей нет. "
  f"Вендор есть только в подписях 13 рисунков (EtherChannel, PAgP, CDP, ESA/WSA/ISE/AMP, LWAPP, FlexConnect, MAC HSRP) и в одной анимации. "
  "Набор иконок нарисован заново, но повторяет смысл фирменных глифов Cisco (D7).")
A("- **Ограничение этой сессии.** Figma API/MCP недоступен: токена `/home/menus12/…/figma_ci` в контейнере нет, Figma MCP не подключился (403 от прокси). "
  "Поэтому подписи иллюстраций прочитаны через OCR (tesseract eng+rus) и проверены глазами по рендерам `rsvg-convert`, а не из узлов `TEXT`. "
  "Лист `_Библиотека` оценён по 206 экспортированным SVG. Подробности — в §7.")
A("")
A("## 2. Итоги")
A("")
A("### По категориям")
A("")
A(table(["category", "строк", "из них learner"], [(c, n, cnt(lambda r, c=c: r["category"] == c and r["audience"] == "learner")) for c, n in st["by_category"]]))
A("")
A("### По поверхностям")
A("")
A(table(["surface", "строк"], st["by_surface"]))
A("")
A("### По предложенному действию")
A("")
A(table(["action", "строк", "из них learner"], [(a, n, cnt(lambda r, a=a: r["action"].split(":")[0] == a and r["audience"] == "learner")) for a, n in st["by_action"]]))
A("")
A("### По модулям (в порядке курса)")
A("")
cats = ["proprietary-tech", "brand", "product", "model", "cli-vendor-string", "certification", "visual", "lab-infra", "link", "legal"]
A(table(["module", "всего"] + cats, [(m, n) + tuple(st["module_cat"][m].get(c, 0) or "" for c in cats) for m, n in st["by_module"]]))
A("")
A("`(root)` — корневые и служебные файлы: `figma-assets.json`, `migration-instructions.md`, `ccna2-labs.md`, `calc_duration.txt`, `readme-assets/`, `packet-tracer-source-files/`.")
A("")
A("## 3. Топ-20 самых «вендорных» материалов (по строкам, видимым обучающемуся)")
A("")
A(table(["#", "material", "строк", "основное"], [(i, f"`{m}`", n, ", ".join(f"{c} {k}" for c, k in cc)) for i, (m, n, cc) in enumerate(st["top_materials"], 1)]))
A("")
A("Экзамены и квизы стоят наверху, потому что одно и то же пояснение («HSRP и GLBP — собственные протоколы компании Cisco…») повторяется в `comment` каждого варианта ответа. Сами правки там почти механические.")
A("")
A("## 4. Решения для оператора")
A("")
A("Решения сгруппированы по типам. В скобках — сколько строк CSV ссылаются на код.")
A("")

dec = dict(st["dec_counts"])
def dn(code):
    return cnt(has(code))

A(f"### D1. Имя курса и служебные идентификаторы («CCNA», «SRWE») — {dn('D1')} строк")
A("")
A("**Где:**")
A("- репозиторий `learn-ccna2`;")
A("- `figma-assets.json`: `course: ccna2`, 288 id `ccna2-…`, 215 имён страниц «CCNA2 · …»;")
A("- каталоги `animations/ccna2-*`, файл `ccna2-labs.md`;")
A("- заголовки «SRWE-F1/F2» и `shortName: srwe-f1` в `final-lab-part1/2`;")
A("- ссылки `learn-ccna1#…` в `.github/scripts`.")
A("")
A(f"Сводная строка — {ID_COURSE}.")
A("")
A(f"**Рекомендация:** переименовать только то, что видит обучающийся: заголовки и `shortName` финальных лаб ({ID_FL[0]}…{ID_FL[-1]}). "
  "Служебные id (`ccna2-…`, страницы Figma, имя репозитория) оставить: они связывают Figma и git, обучающийся их не видит, а переименование задевает learn-ccna1/3 и CI. "
  "Решать вместе с названием траектории в `learn-metadata.json` — в нём вендора уже нет.")
A("")
A(f"### D2. Модели оборудования → идентичность learn-netsim — {dn('D2')} строк")
A("")
A(table(["что в курсе", "предложение"], [
    ("Catalyst 2960 / 2950, `WS-C…`", "**NS01**"),
    ("Catalyst 3560 / 3650 / 3550 (L3-коммутатор)", "**NS01** при условии, что NS01 умеет L3 (SVI, `ip routing`); иначе нужна модель L3 — **вопрос к learn-netsim**"),
    ("1941, 2901, 2911, 4221, 4321, ISR, `ISR4221-2x1GE`", "**NR01** (вторая модель в той же топологии — **NR02**)"),
    ("ПК / сервер в топологиях", "**NPC**"),
    ("WLC 3504, Aironet 1815i, `AIR-AP1815I`", "аналога нет → «контроллер WLC», «точка доступа» (зависит от D5)"),
    ("Meraki Go / MX64W, RV130W, WRT300N (Linksys)", "→ «беспроводной роутер SOHO», «точка доступа»"),
]))
A("")
A("Отдельный случай — типовое примечание «Роутеры, используемые в практических лабораторных работах CCNA, — это Cisco 4221 с Cisco IOS XE 16.9.4 (образ universalk9)…» в 5 лабах без PT. "
  "Его лучше заменить общим абзацем про learn-netsim, а не править модели по одной.")
A("")
A(f"### D3. Cisco IOS как продукт и вендорные строки в выводе CLI — {dn('D3')} строк")
A("")
A(f"- «IOS / Cisco IOS» как название ОС — {cnt(lambda r: r['category'] == 'product' and re.search(r'IOS', r['term']) is not None)} строк. Предложение: **NetOS** (NSALAB NetOS), где речь об ОС устройства; нейтрально «ОС устройства», где бренд не важен.")
A("- `cli-vendor-string` и имена образов:")
A("  - баннер `Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.0(2)SE7` (01.03, строка 36);")
A("  - `Hardware is ISR4221-2x1GE`;")
A("  - колонка Platform в `show cdp neighbors` (`WS-C3560-`, `ISR4221/K`);")
A("  - имена образов `c2960-lanbasek9-mz.150-2.SE8.bin` в 01.01;")
A("  - `SSH-2.0-Cisco-1.25` и дерево CDP с `Copyright … Cisco Systems` в растрах 1.3.2 и 10.5.10.")
A("")
A("  Предложение: перегенерировать выводы из learn-netsim. **Нужно от learn-netsim:** строка версии, имя платформы и имя образа NetOS.")
A("- Синтаксис команд не трогаем (по issue). Исключение — вендорное ключевое слово `mls qos trust device cisco-phone` (03.03): решить, оставлять ли пример.")
A("")
A(f"### D4. Проприетарные протоколы и технологии — {sum(dn(c) for c in ['D4.1','D4.2','D4.3','D4.4','D4.5','D4.6','D4.7','D4.8','D4.9','D4.10'])} строк")
A("")
A("Решение принимается по протоколу. В тексте почти везде есть фраза «собственный/проприетарный протокол Cisco» — её стоит переписать в любом варианте (например, «проприетарный протокол одного производителя»).")
A("")
A(table(["код", "что", "строк", "где в курсе", "рекомендация"], [
    ("D4.1", "CDP", dn("D4.1"), "10.5 (CDP-разведка), 11.x, 16.2 `show cdp neighbors`, 3.1.3, 13.2", "основным протоколом обнаружения сделать **LLDP**; CDP оставить одним примером в теме атак, без бренда; `show cdp …` → `show lldp …` (нужна поддержка в learn-netsim)"),
    ("D4.2", "DTP, VTP, ISL", dn("D4.2"), "3.3, 3.5 (лаба 3.5.5 «настройка DTP»), 10.5, 11.x", "DTP оставить как тему безопасности («автосогласование транка»), без бренда; VTP — кратко; **ISL убрать** (устарел), оставить 802.1Q"),
    ("D4.3", "PVST+/Rapid PVST+, PortFast, BPDU Guard, Root/Loop Guard, UplinkFast/BackboneFast", dn("D4.3"), "модуль 05, 11.5", "подавать как «STP на каждую VLAN», упомянуть MSTP (802.1s); PortFast/BPDU Guard оставить как ключевые слова CLI и пояснить стандартным термином (edge port); UplinkFast/BackboneFast убрать (встроено в RSTP). Команды — синтаксис"),
    ("D4.4", "HSRP, GLBP", dn("D4.4"), "модуль 09 целиком, лаба 9.3.3 «HSRP Configuration Guide», рисунок 9.2.2 (MAC 0000.0C07.AC01), экзамен 07-09", "**крупное решение.** Основным FHRP сделать **VRRPv3** (RFC 5798) и переписать 9.2/9.3 и лабу 9.3.3 под VRRP (нужна поддержка в learn-netsim); HSRP/GLBP — абзац «проприетарные варианты»"),
    ("D4.5", "EtherChannel, PAgP", dn("D4.5"), "модуль 06 целиком (и имя каталога), 5 лаб, экзамены", "«агрегирование каналов (LAG, IEEE 802.1AX / LACP)»; EtherChannel — синоним при первом упоминании; основной протокол — **LACP**, PAgP упомянуть. Ключевые слова `channel-group`, `show etherchannel` — синтаксис (исключены из подсчёта)"),
    ("D4.6", "EIGRP, IGRP", dn("D4.6"), "14.5 (история протоколов), легенда `show ip route`, экзамены", "оставить как пример (EIGRP описан в RFC 7868), без слова Cisco; легенду кодов `show ip route` менять вместе с форматом вывода learn-netsim"),
    ("D4.7", "CEF", dn("D4.7"), "14.2", "описывать «FIB + таблица смежности»; CEF — как пример реализации"),
    ("D4.8", "LWAPP, LAP, FlexConnect", dn("D4.8"), "12.2, 12.4, 13.x", "основным сделать **CAPWAP** (RFC 5415); «облегчённая AP» без аббревиатуры LAP; FlexConnect → «локальная коммутация на AP»"),
    ("D4.9", "SPAN, UDLD, TACACS+ и прочее", dn("D4.9"), "10.x, 7.2 (порт 49)", "SPAN → «зеркалирование портов»; TACACS+ (RFC 8907) и UDLD — keep"),
    ("D4.10", "продукты безопасности и облако: ESA/WSA, AMP, ISE, Secure ACS, ASA, Talos, Meraki", dn("D4.10"), "10.1, 10.2, квизы модуля 10, 12.2, 13.1, 13.4", "neutralize: «шлюз безопасности почты», «веб-прокси», «защита конечных точек», «NAC-сервер», «облачная панель управления»; цитату «по данным Cisco Talos…» убрать или дать с нейтральным источником"),
]))
A("")
A(f"### D5. Packet Tracer и лабораторная инфраструктура — {dn('D5')} строк")
A("")
A(f"- **{len(labs)} лаб.** На learn-netsim ещё не переведена ни одна; в CCNA2 нет аналога learn-ccna1#53.")
A(f"- **{len(pt_labs)} лаб на PT.** Каждая — `.pka`, `deploy/pt-lab` (VM с PT, `pt-url`, `pt-api-port`) и `assessment/ms.yaml` с аспектами «Register packet tracer aspect mark». Одна строка на лабу, например {pt_labs[0]['id']}.")
A(f"- **Из них {len(gui)} с GUI-зависимостью** (`action: decide`): WLAN/WLC-лабы модуля 13 и лабы «physical mode» (физическая рабочая область PT: стойка, кабели). Прямой замены в learn-netsim у них нет:")
A("  " + ", ".join(f"`{r['material'].split('/')[-1]}`" for r in gui))
A("  Варианты: (а) оставить на PT как переходный fallback (так в `decisions/packet-tracer-substitution.md`); (б) переписать в CLI-форму; (в) снять.")
A(f"- **{len(nopt)} лаб без среды выполнения** — бывшие лабы на реальном оборудовании: `deploy` создаёт только Azure resource group и учётку, оценки нет:")
A("  " + ", ".join(f"`{r['material'].split('/')[-1]}`" for r in nopt))
A("  Решить: перевести на learn-netsim или убрать.")
A("- Ссылки и текст:")
A("  - 38 закомментированных ссылок `<!-- [Скачать файл Packet Tracer…](./assets/N-lab.pka) -->` → remove;")
A("  - «Packet Tracer» в видимом тексте → «симулятор»;")
A("  - имена устройств PT в шагах лаб (`LAP-PT`, `PT-HOST-NM-1CFE`, `HomeRouter-PT-AC`) → вместе с переводом лабы.")
A("- `packet-tracer-source-files/` — 44 исходных `.docx` NetAcad. В каждом логотип «Cisco Networking Academy» в верхнем колонтитуле и «© … Корпорация Cisco… www.netacad.com» в нижнем. Из курса на них ссылок нет. Решать вместе с D9.")
A("")
A(f"### D6. Видео — вне аудита ({dn('D6')} строк встраиваний)")
A("")
A("По указанию оператора документы `videos/` не разбирались. Все 15 роликов уже классифицированы в `videos/README.md` (учебные ролики NetAcad CCNA 7 SRWE на канале оператора, маркетинговых нет) и будут пересобраны. "
  "Попадания словаря в `videos/*.md` занесены в журнал как исключённые с этой причиной. "
  "В карте остались только 15 строк встраиваний `![youtube](…)` в README материалов и одна фраза «перенаправлены на YouTube» (10.5) — их меняют при замене роликов.")
A("")
A(f"### D7. Библиотека иконок Figma (лист `_Библиотека`) — {ID_LIB}")
A("")
A("**Наблюдение.** Иконки — собственная изометрическая отрисовка: свой синий, стохастическая тень, свои ПК и серверы, без логотипов и надписей. "
  "Но **смысл глифов повторяет набор сетевых иконок Cisco**:")
A("- маршрутизатор — цилиндр с четырьмя стрелками «крестом»;")
A("- коммутатор — блок с двумя парами встречных стрелок;")
A("- L3-коммутатор — блок со «звездой» стрелок;")
A("- WLC, AP, межсетевой экран из «кирпичей».")
A("")
A("**Рекомендация: keep.** Эти глифы — де-факто отраслевая нотация (ими рисуют и вендоро-независимые учебники), прямого копирования нет. "
  "Если нужна полная независимость, перерисовывать стоит маршрутизатор и L3-коммутатор — они узнаваемее всего. "
  "Оценка сделана по 206 экспортированным SVG; сам лист в Figma в этой сессии не открыт.")
A("")
A(f"### D8. Растры и рисунки чужого стиля — {dn('D8')} строк")
A("")
A(table(["семейство", "растров", "что делать"], [
    ("экзаменационные и квизовые схемы NetAcad (бирюзовые 3D-иконки Cisco)", FAM["netacad-icons"], "перерисовать в библиотеке курса; в `raster-inventory-ccna2.md` их нет — это новый объём работ"),
    ("GUI Cisco WLC с логотипом (классический и новый UI, вкладка браузера «CCNA7», страница входа с ©)", FAM["wlc"], "компоненты К4/К5/К6 из `raster-inventory-ccna2.md`, без логотипа; зависит от D5"),
    ("скриншоты логической топологии Packet Tracer (`topology.png` лаб)", FAM["pt-topo"], "схема топологии в стиле курса — вместе с переводом лабы"),
    ("GUI Packet Tracer (HomeRouter-PT-AC, WRT300N, Web Browser PT, Command Prompt PT)", FAM["pt-gui"], "компоненты К3/К4"),
    ("схемы из лабораторных руководств NetAcad (синие иконки Cisco)", FAM["labmanual"], "перерисовать"),
    ("продуктовые фото и схемы с логотипом (1.1.3 Catalyst 2960, 12.2.4 Meraki, 13.1.2-1 MX64W, 13.2.6-1 WLC 3504, 13.4.4-1 Meraki Dashboard)", FAM["photo"], "как в raster-inventory (A/B/C)"),
    ("Wireshark с вендорными данными (1.3.1 пароль ccna, 1.3.2 SSH-2.0-Cisco, 10.5.10 дерево CDP)", FAM["wireshark"], "компонент К1 с нейтральными данными"),
    ("фигуры NetAcad (10.2.2, 13.1.6, 13.1.8)", FAM["netacad-fig"], "перерисовать"),
    ("CLI-растры экзаменов с брендом в значениях (CiscoVille, cisco.com, netacad.net) или протоколами (PAgP, GLBP, CDP, EIGRP)", FAM["cli"], "D11 / D4"),
]))
A("")
A(f"Всего {sum(FAM.values())} строк `surface=raster`. Служебные `readme-assets/*.png` — в D9.")
A("")
A("30 растров без вендора: CLI-скриншоты без бренда, диалоги Windows, стоковые фото, окно WannaCry. Они перечислены в таблице покрытия (§6) и в карту не попали.")
A("")
A(f"### D9. Служебные документы и имена файлов/каталогов — {dn('D9')} строк")
A("")
A("**Служебные документы** (обучающемуся не показываются):")
A("- `migration-instructions.md` — описывает перенос курса из NetAcad: srwe-v7, ITN, ссылки на netacad;")
A("- `ccna2-labs.md` — колонка PT / non PT;")
A("- `calc_duration.txt`;")
A("- `readme-assets/`:")
A("  - скриншоты сайта NetAcad с логотипом Cisco;")
A("  - PDF «CCNAv7 SRWE Scope and Sequence» с ®;")
A("  - `pt-menu.png` с локальным путём пользователя;")
A("  - `video.png` с видимым адресом электронной почты.")
A("")
A("**Рекомендация:** пока репозиторий закрыт — keep. Перед публикацией убрать `readme-assets/*` со скриншотами NetAcad, PDF Scope & Sequence и `packet-tracer-source-files/*.docx`. `video.png` и `pt-menu.png` проверить на персональные данные в любом случае.")
A("")
A("**Имена каталогов:**")
A("- суффикс `-ilm` (Instructor Lab Manual NetAcad) — 4 лабы;")
A("- `-non-pt` — 1 лаба;")
A("- `06-etherchannel/…etherchannel…`, `…-hsrp-…`, `…-dtp` — имена тем, решаются вместе с D4.")
A("")
A("**Рекомендация:** каталоги переименовывать только вместе с миграцией путей на платформе — путь служит идентификатором материала.")
A("")
A(f"### D10. Тег «Cisco» — {ID_TAG}")
A("")
A("`material-tags.json` = `[\"Network\", \"Cisco\"]`. Тег наследуют все материалы через `$ref`. **remove** (или заменить нейтральным тегом).")
A("")
A(f"### D11. Бренд и сертификация как значения конфигурации — {dn('D11')} строк")
A("")
A("**Где встречается:**")
A("- пароли: `cisco`, `Cisco123`, `Cisco123!`, `cisco123`, `Ciscoenpa55`, `Ciscolinepa55`, `$cisco!PRIV*`, `ccna`;")
A("- имена хостов, SSID и community: `CiscoVille`, `ciscolab`, `ciscosb1`, `CCNAv7`;")
A("- домены и URL: `cisco.com`, `ccna-lab.com`, `CCNA-lab.com`, `CCNA2.Lab-11.6.1`, `netacad.pka`, `www.cisco.pka`, `www.netacad.pt`, `netacad.net`.")
A("")
A("**Рекомендация:** replace на нейтральные значения. **Важно:** в PT-лабах эти значения зашиты в `.pka` и в `assessment` — менять синхронно с топологией и проверками, иначе оценка сломается.")
A("")
A(f"### D12. Структура курса = SRWE v7 Scope and Sequence — {ID_STRUCT}")
A("")
A("Нумерация и состав тем повторяют NetAcad:")
A("- каталоги `NN.NN-…`;")
A("- 432 маркера `<!-- 1.1.1 -->` в 78 README;")
A("- «Тема 3.5.0 -» в пояснениях квизов;")
A("- `migration-instructions.md:23`: «согласно оригинальному scope & sequence».")
A("")
A("Обучающийся маркеров не видит. Решить, сохраняем ли мы нумерацию SRWE как опору.")
A("")
A(f"### D13. Производный контент (вопрос права) — {ID_LEGAL}")
A("")
A("Это не упоминание, но главный вывод аудита. Текст лекций, банк вопросов квизов и экзаменов, рисунки и ролики — перевод и адаптация материалов NetAcad SRWE v7 (см. `migration-instructions.md`). "
  "Чистка бренда делает курс вендоро-нейтральным по виду, но не меняет происхождения материала. Рекомендую решить это до массовых правок: от ответа зависит, чистить ли текст точечно (D1–D12) или переписывать.")
A("")
A("## 5. Сверка полноты по словарю (N = M + K)")
A("")
A("Единица подсчёта — одно попадание регулярного выражения (без учёта регистра) в строке файла, в имени файла или каталога, в OCR-тексте картинки или в извлечённом тексте `.docx`/`.pdf`. "
  "M — попадания, покрытые строкой карты. Несколько соседних попаданий одной категории на строке файла сливаются в одну строку: «Cisco Catalyst 2960» — одна строка `model`. "
  "Для лаб все попадания в `deploy/`, `assessment/` и `assessment.json` покрыты одной строкой на лабу, как просит issue. K — исключено с причиной. Полный журнал — `audit/dictionary-hits.csv`.")
A("")
A("Колонка «файлов (текст)» — число текстовых файлов с совпадением, без SVG и бинарных; сверяется с ориентиром из issue. В колонке regex знак `¦` означает `|` (заменён, чтобы не ломать таблицу).")
A("")
rec = []
for x in st["recon"]:
    src = ", ".join(f"{k} {v}" for k, v in x["sources"].items())
    rsn = "; ".join(f"{k} {v}" for k, v in x["reasons"].items())
    rec.append((f"`{x['term']}`", f"`{x['regex'].replace('|', '¦')}`", x["origin"], x["files_text"], x["N"], x["M"], x["K"], src, rsn))
A(table(["термин", "regex (i)", "словарь", "файлов (текст)", "N", "M", "K", "источники", "причины K"], rec))
A("")
A("Сверка с ориентирами issue (файлы без SVG): `cisco` 120 = 120, `netacad` 4 = 4, `networking academy` 16 = 16, `ccna` 88 = 88, `packet tracer` 87 = 87, `webex` 0 = 0, `catalyst` 27 = 27, `meraki` 3 = 3, `\\.pka` 79 = 79. "
  "`\\bIOS\\b` даёт 57 текстовых файлов против 63 в issue: разница — бинарные файлы (`git grep` без `-I` даёт 76). В текстовых файлах ничего не потеряно, бинарные `.docx`/`.pdf` разобраны отдельно.")
A("")
A("Пояснения к K:")
A("- **синтаксис CLI** — по правилу issue. Ключевые слова команд и вывода в стиле IOS (`show etherchannel summary`, `spanning-tree portfast`, `Portfast Default is disabled`, `| begin span`) — синтаксис, который learn-netsim сохраняет. "
  "Названия протоколов (CDP, DTP, PAgP, HSRP…) внутри команд **не** исключены: при смене протокола (D4) эти строки меняются.")
A("- **OCR-артефакты ©/®/™** — tesseract принимает круглые маркеры легенды, иконки портов и фавиконы вкладок за знаки. Каждый такой случай проверен глазами. Настоящие знаки в растрах есть только в 13.2.3-1 (© Cisco Systems) и 10.5.10 («Copyright (c) … Cisco Systems»), они в карте.")
A("- **видео вне аудита** — попадания в `videos/*.md` (разборы роликов): по указанию оператора видео не входят в аудит, они уже классифицированы и будут пересобраны (D6).")
A("- **ложные совпадения** — `ensa` в «Compensates», `c\\d{4}` в шестнадцатеричном адресе `C80084AEF101`, `span` как имя переменной в `figma_sync.py`, `PT` в названии шрифта «PT Mono», ESA = Extended Service Area на рисунке 12.3.3-2.")
A("")
A("**Не исключено, но по сути не вендор:** `youtube` — это не ссылки на вендора, а встраивания роликов NetAcad в README материалов. Они в карте как `link` с D6.")
A("")
A("### Итоговый словарь")
A("")
A("Из issue: " + ", ".join(f"`{t}`" for t, rx, c, o in TERMS if o == "issue") + ".")
A("")
A("Добавлено по ходу работы: " + ", ".join(f"`{t}` (`{rx.replace('|', '¦')}`)" for t, rx, c, o in TERMS if o == "added") + ".")
A("")
A("Вне словаря, найдено глазами и внесено в карту:")
A("- CDP в выноске рисунка 3.1.3;")
A("- MAC HSRP `0000.0C07.AC01` на рисунке 9.2.2;")
A("- вывод GLBP в 07-09-exam/9.png;")
A("- маршрут EIGRP «D …» в final-exam/11.gif;")
A("- `%CDP-4-…` в final-exam/2.png;")
A("- логотипы на фото и в GUI.")
A("")
A("Кандидаты на словарь следующих курсов: `Linksys`, `Aironet`, `AIR-AP`, `RV1\\d\\dW`, `MX\\d\\dW`, `WRT\\d+N`, `CleanAir`, `0000\\.0c07\\.ac`, `0007\\.b400`, `HomeRouter-PT`, `LAP-PT`, `CCNAv7`, `Ville\\b`.")
A("")
A("## 6. Таблица покрытия")
A("")
ext = collections.Counter((os.path.splitext(f)[1].lower() or os.path.basename(f)) for f in files)
how = {
    ".tf": "словарь построчно (лабы — сводно, одна строка на лабу)", ".json": "словарь построчно; квизы — с номером вопроса", ".md": "словарь построчно с контекстом: ограждённый код, HTML-комментарии",
    ".svg": "рендер `rsvg-convert -b white -w 1600` → OCR eng+rus → просмотр глазами (18 контакт-листов); встроенные `<image>` извлечены", ".png": "OCR eng+rus (мелкие ×2) + просмотр глазами (19 контакт-листов)",
    ".yaml": "словарь построчно", ".sh": "словарь построчно", ".docx": "текст тела, таблиц и колонтитулов (python-docx) + словарь; картинки колонтитулов просмотрены", ".tpl": "словарь построчно",
    ".pka": "не открывались (зашифрованный формат PT); покрыты строкой лабы и именем файла", ".jpg": "OCR + просмотр", ".jpeg": "OCR + просмотр", ".gif": "1-й кадр (все GIF однокадровые) → OCR + просмотр",
    ".py": "словарь построчно", ".pdf": "`pdftotext` + словарь; список картинок `pdfimages`", ".yml": "словарь построчно", ".txt": "словарь построчно", ".gitignore": "словарь построчно",
}
rows_cov = []
for e, n in sorted(ext.items(), key=lambda kv: -kv[1]):
    if e == ".pka":
        rows_cov.append((f"`{e}`", n, f"{n} как файлы", f"содержимое {n}", how.get(e, "")))
    elif e == ".md":
        nv = sum(1 for f in files if f.startswith("videos/"))
        rows_cov.append((f"`{e}`", n, n - nv, f"{nv} (`videos/` — по указанию оператора)", how.get(e, "")))
    else:
        rows_cov.append((f"`{e}`", n, n, 0, how.get(e, "")))
A(table(["тип", "всего в git", "просмотрено", "пропущено", "как"], rows_cov))
A("")
A(f"Итого `git ls-files` = {len(files)} (без каталога `audit/` — это сам аудит). Не просмотрено содержимое 40 `.pka`: формат зашифрован. Они покрыты строками лаб и строками имён файлов, внутренние строки PT-топологий (имена хостов, пароли, URL серверов) видны по README и скриншотам `topology.png`.")
A("")
A("Ассеты `figma-assets.json`:")
A("")
A(table(["kind", "в манифесте", "просмотрено", "как", "не просмотрено"], [
    ("illustration", 197, 187, "рендер + OCR + глазами (185 synced + 2 orphan, лежащих в git)", "10 orphan без файла в git (6.3.3, 10.1.2-1…-3, 14.3.3, 14.3.4, 15.2.3, 15.2.7, 15.3.2, 15.4.3): Figma недоступна. По `notes` манифеста это дубли просмотренных рисунков и три одиночные иконки"),
    ("animation", 18, 18, "5 кадров каждой (SMIL, Chromium: `pauseAnimations` + `setCurrentTime` на 12/32/52/72/92 %) + OCR + тексты узлов из `animations/*/spec.json`", "—"),
    ("native", 73, 73, "OCR + глазами, сверка с `design/raster-inventory-ccna2.md`", "—"),
    ("вне манифеста: SVG", 1, 1, "`16.01.02-…-quiz/assets/16.1.2.svg`", "—"),
    ("вне манифеста: растры", 152, 152, "экзамены 82, `topology.png` лаб 39, `readme-assets` 17, квизы и фото 14", "—"),
]))
A("")
A(table(["прочее", "всего", "просмотрено", "как"], [
    ("видео (документы `videos/`)", 16, 0, "пропущены по указанию оператора: уже классифицированы и будут пересобраны; попадания словаря — в журнале как исключённые"),
    ("встроенные растры в SVG", 5, 5, "3 текстуры (в ~180 SVG), рентген 12.1.5, череп 12.6.5 — вендора нет"),
    ("лист `_Библиотека` (Figma)", 1, 0, "напрямую не открыт; вывод D7 — по иконкам в 206 экспортах"),
    ("листы Figma «Видео · …»", "?", 0, "не проверены: Figma недоступна"),
]))
A("")
A("## 7. Ограничения и что осталось сделать")
A("")
A("1. **Figma.** Не прочитаны `characters` узлов `TEXT` и имена инстансов. Нет токена, Figma MCP получил 403 от прокси сессии. "
  "Вместо этого — OCR и просмотр рендеров. Мелкий текст OCR может пропустить: так CDP в 3.1.3 нашёлся только глазами. "
  "**Рекомендация:** перед правками одним проходом `GET /v1/files/3FtCg22qFubpLBPOetQU03/nodes?ids=…` по 197 иллюстрациям собрать `characters` и сверить с разделом `surface=illustration`. "
  "Заодно открыть `_Библиотека` (D7) и листы «Видео · …».")
A("2. **Имя узла Figma** в `locator` для иллюстраций не указано: есть `key` и `nodeId` из манифеста, имя узла без API не получить.")
A("3. **`.pka` не открывались.** Значения внутри топологий PT (пароли, URL `www.cisco.pka`, имена `Cisco*`) видны только там, где они попали в README или в `topology.png`.")
A("4. **Ветка и PR.** По инструкции сессии файлы лежат в ветке `claude/issue-21-analysis-ocqub8`, а не в `audit/vendor-mentions`. PR не открыт: оператор попросил результат комментарием. Если нужна PR — открыть её из этой ветки, она меняет только `audit/`.")
A("5. **Хаб.** Сигналы «взял / PR открыт» в хаб не отправлены: доступа к хабу из этой сессии нет.")
A("")
A("## 8. Замечено попутно (в материалах не правилось)")
A("")
A("- `final-lab-part2/learn-metadata.json:3` — `shortName: \"srwe-f1\"`, совпадает с part1, должно быть `srwe-f2` (дефект).")
A("- `learn-metadata.json:2` и `migration-instructions.md:2` — «**Ведение** в коммутацию…» → «Введение».")
A("- `migration-instructions.md:278` — «Packet **Trcer**».")
A("- `09-fhrp-concepts/09.03.03-lab-hsrp-configuration-guide/learn-metadata.json:5` — «отрабока».")
A("- `03-vlans/03.04-vlan-trunks/README.md:20` — «На **риунке**»; `09-fhrp-concepts/09.03.04-…/README.md:118` — «на **торой** интерфейс»; `13-wlan-configuration/13.05.02-…/README.md:112` — «назначте».")
A("- Каталог `08-slaac-and-dhcpv6-concepts/08.01-ipv6-global-unicast-address-**assigment**` (assignment).")
A("- `readme-assets/video.png` — в кадре адрес электронной почты; `readme-assets/pt-menu.png` — локальный путь с именем пользователя.")
A("")
A("## 9. Метод (для повторения на CCNA1/CCNA3)")
A("")
A("Скрипты — в `audit/tools/` (запуск и зависимости — `audit/tools/README.md`). Шаги:")
A("")
A("1. `git ls-files` → словарь по текстовым файлам построчно. Контекст строки: ограждённый код, HTML-комментарий, номер вопроса квиза, `answerSchema` лабы. Попадания в именах файлов и каталогов — отдельно.")
A("2. Классификация: соседние попадания сливаются в фразу, фраза получает категорию по приоритету "
  "legal > link > cli-vendor-string > model > proprietary-tech > product > brand > certification > lab-infra. "
  "«cisco»/«ccna» в значении конфигурации (пароль, домен, хост) отделяются по токену (D11).")
A("3. Картинки: рендер SVG → OCR; кадры анимаций → OCR; растры → OCR. Всё просмотрено глазами по контакт-листам. Встроенные растры извлечены и дедуплицированы по sha256.")
A("4. `.docx`/`.pdf` → текст, включая колонтитулы, → словарь; картинки колонтитулов просмотрены.")
A("5. Журнал попаданий → строка карты или исключение с причиной → N = M + K по каждому термину.")
A("")
open(os.path.join(S, "audit", "vendor-mentions.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("md lines", len(md))
