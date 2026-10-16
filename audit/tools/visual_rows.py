# Pass 3: rows from visual review (illustrations, animations, rasters, embedded textures, Figma library),
# videos (one summary row per video), binary docs (docx/pdf), and course-level rows.
# Verdicts below were made by viewing every rendered SVG / raster / animation frame (contact sheets) + OCR.
import json, os, re, subprocess, collections

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, WORK as S, tracked_files
manifest = json.load(open(os.path.join(REPO, "figma-assets.json")))
by_path = {a["out"]["path"]: a for a in manifest["assets"]}
files = tracked_files()
rows = []


def mod_mat(p):
    parts = p.split("/")
    if re.match(r"^\d\d-\d\d-exam$|^final-", parts[0]):
        return parts[0], parts[0]
    if re.match(r"^\d\d-", parts[0]):
        return parts[0], "/".join(parts[:2]) if len(parts) > 2 else parts[0]
    return "(root)", "(root)"


def loc_for(p):
    a = by_path.get(p)
    if a:
        nid = a.get("figma", {}).get("nodeId")
        return f"{p} (key {a['display']['key']}" + (f", nodeId {nid})" if nid else f", {a['kind']})")
    return p


def add(p, surface, term, category, audience, excerpt, action, note, terms=(), loc=None):
    m, mat = mod_mat(p)
    rows.append({"module": m, "material": mat, "surface": surface, "locator": loc or loc_for(p), "term": term,
                 "category": category, "audience": audience, "excerpt": excerpt[:160], "action": action,
                 "note": note, "_file": p, "_line": 0, "_terms": list(terms), "_hits": []})


def find(suffix):
    c = [f for f in files if f.endswith(suffix)]
    assert len(c) == 1, (suffix, c)
    return c[0]


# ---------------- illustrations (SVG): vendor text inside figures (OCR + visual check)
ILL = [
    ("03.01-overview-of-vlans/assets/3.1.3.svg", "CDP-кадры", "proprietary-tech", "выноска «Порт отправляет CDP-кадры для предоставления информации, используемой IP-телефоном»", "decide", "[D4.1] CDP в тексте выноски; OCR не распознал (мелкий шрифт) — найдено визуально"),
    ("05.03-evolution-of-stp/assets/5.3.4.svg", "PortFast и BPDU Guard", "proprietary-tech", "подпись у портов F0/11–F0/18 коммутатора S2: «PortFast и BPDU Guard»", "decide", "[D4.3] названия функций вендора в подписи схемы"),
    ("06.01-etherchannel-operation/assets/6.1.2.svg", "EtherChannel ×2", "proprietary-tech", "подписи двух агрегированных каналов «EtherChannel»", "decide", "[D4.5] торговое название агрегирования каналов"),
    ("06.01-etherchannel-operation/assets/6.1.7.svg", "PAgP", "proprietary-tech", "стрелка между S1 и S2 с подписью «PAgP»", "decide", "[D4.5] PAgP — проприетарный; пара к 6.1.9 (LACP)"),
    ("06.02-configure-etherchannel/assets/6.2.1-1.svg", "EtherChannel сформирован", "proprietary-tech", "заголовок над каналом S1–S2: «EtherChannel сформирован»", "decide", "[D4.5]"),
    ("06.02-configure-etherchannel/assets/6.2.1-2.svg", "EtherChannel не сформирован", "proprietary-tech", "заголовок над каналом S1–S2: «EtherChannel не сформирован»", "decide", "[D4.5]"),
    ("09.02-hsrp/assets/9.2.2.svg", "0000.0C07.AC01", "proprietary-tech", "подпись виртуального маршрутизатора: «Виртуальный MAC-адрес 0000.0C07.AC01» — well-known MAC HSRP (OUI 00:00:0C вендора)", "decide", "[D4.4] при переходе на VRRP — 0000.5E00.01xx (RFC 5798); найдено визуально, не словарём"),
    ("10.01-endpoint-security/assets/10.1.3.svg", "NAC AAA/ISE; ESA/WSA; AMP", "product", "подписи блоков «NAC AAA/ISE», «ESA/WSA», «устройства, защищённые с помощью AMP»", "neutralize", "[D4.10] продукты безопасности вендора → классы решений (NAC, шлюз почты, веб-прокси, защита конечных точек)"),
    ("10.01-endpoint-security/assets/10.1.4.svg", "ESA", "product", "подпись устройства «ESA» над межсетевым экраном", "neutralize", "[D4.10] → «шлюз безопасности почты»"),
    ("10.01-endpoint-security/assets/10.1.5.svg", "WSA", "product", "подпись устройства «WSA»", "neutralize", "[D4.10] → «веб-прокси / шлюз веб-безопасности»"),
    ("12.02-components-of-wlans/assets/12.2.5-2.svg", "LWAPP", "proprietary-tech", "подпись точки доступа под управлением контроллера «LWAPP»", "decide", "[D4.8] LWAPP устарел → CAPWAP (RFC 5415)"),
    ("12.04-capwap-operation/assets/12.4.5.svg", "FlexConnect AP", "proprietary-tech", "подпись точки доступа в филиале «FlexConnect AP»", "decide", "[D4.8]"),
    ("14.05-static-and-dynamic-routing/assets/14.5.2.svg", "IGRP; EIGRP", "proprietary-tech", "шкала истории протоколов: EGP, IGRP (1985), RIPv1, IS-IS, OSPFv2, EIGRP (1992), RIPv2, BGP …", "keep", "[D4.6] историческая шкала; IGRP/EIGRP — протоколы вендора, без бренда; оставить"),
]
for suf, term, cat, exc, act, note in ILL:
    add(find(suf), "illustration", term, cat, "learner", exc, act, note + "; имя узла TEXT не прочитано — доступа к Figma API в этой сессии нет")

# animations
add(find("14.01-path-determination/assets/14.1.2.svg"), "animation", "show ip route: «I - IGRP», «D – EIGRP, EX - EIGRP external»", "proprietary-tech", "learner",
    "терминал в кадрах ~30–75 %: «R1# show ip route / Codes: C – connected, S - static, I - IGRP, R - RIP … D – EIGRP …» (текст узла есть в animations/ccna2-vazbtn3/spec.json:200,205)",
    "keep", "[D4.6] легенда кодов вывода `show ip route` в стиле IOS; менять вместе с форматом вывода learn-netsim")

# shared texture + icon library (one row each)
emb = json.load(open(os.path.join(S, "out", "embedded.json")))
tex = [h for h, v in emb["images"].items() if len(v["svgs"]) > 100]
add("figma-assets.json", "illustration", "фото-/стохастические текстуры корпусов (3 растра в 180 SVG)", "visual", "learner",
    "встроенные PNG " + ", ".join(tex) + ": чёрно-белый стохастический растр-заливка для корпусов ПК/серверов; вендора нет",
    "keep", loc="встроенные <image> в ~180 SVG (sha256-префиксы " + ", ".join(tex) + "; список SVG — по figma-assets.json, kind illustration/animation)", note="общий стиль курса, отмечен один раз (как просит issue); вендорных признаков нет. Прочие встроенные растры: рентген кисти (12.1.5), череп (12.6.5-1/-2) — без вендора")
add("figma-assets.json", "figma-library", "набор иконок устройств (лист «_Библиотека», файл 3FtCg22qFubpLBPOetQU03)", "visual", "learner",
    "маршрутизатор — синий цилиндр с 4 стрелками «крест»; коммутатор — синий блок с 4 стрелками; L3-коммутатор — блок со «звездой» стрелок; WLC, AP, межсетевой экран (кирпичи), ESA/WSA (лупа), хаб",
    "decide", loc="Figma 3FtCg22qFubpLBPOetQU03, лист «_Библиотека» (компоненты устройств)", note="[D7] собственная изометрическая отрисовка (стохастическая тень, свой синий, свои ПК/серверы), но СЕМАНТИКА ГЛИФОВ повторяет набор сетевых иконок Cisco (цилиндр-крест для роутера, стрелки для коммутатора, «звезда» L3). Логотипов и надписей вендора нет. Вывод по 206 экспортированным SVG; лист _Библиотека напрямую не открыт — Figma API/MCP в сессии недоступен")

# ---------------- rasters
def R(p, term, cat, exc, act, note, aud=None):
    add(p, "raster" if not p.startswith("readme-assets/") else "internal-doc", term, cat,
        aud or ("internal" if p.startswith("readme-assets/") else "learner"), exc, act, note)

EXAM_ICONS = {
    "01-04-exam": ["10.png", "11.png", "13.png", "15.png", "16.gif", "18.png", "2.png", "3.gif", "4.png", "5.png", "7.gif"],
    "05-06-exam": ["1.png", "10.png", "2.png", "4.png", "5.png", "6.png", "8.png", "9.png"],
    "07-09-exam": ["1.png", "10.png", "2.png", "3.png", "8.png"],
    "10-13-exam": ["1.png", "2.jpg", "3.png", "4.png"],
    "14-16-exam": ["10.gif", "12.jpg", "13.png", "14.png", "15.gif", "17.png", "18.jpg", "19.gif", "2.jpg", "20.png", "21.gif", "23.gif", "3.jpg", "5.jpg", "6.png", "7.png", "8.png"],
    "final-exam": ["1.png", "12.gif", "13.png", "15.png", "3.png", "4.PNG", "5.png"],
}
for ex, L in EXAM_ICONS.items():
    for fn in L:
        p = f"{ex}/assets/{fn}"
        extra = " (L3-коммутатор «Si»/«звезда», виртуальный маршрутизатор)" if (ex, fn) in (("07-09-exam", "10.png"), ("10-13-exam", "4.png"), ("01-04-exam", "7.gif"), ("05-06-exam", "9.png")) else ""
        R(p, "иконки сети в стиле Cisco/NetAcad", "visual", "схема из экзаменационного банка NetAcad: бирюзовые 3D-иконки Cisco (маршрутизатор, коммутатор, ПК, облако)" + extra,
          "replace:<перерисовать схему в библиотеке курса>", "[D8] растр экзамена NetAcad; текст в нём — CLI/адресация без бренда")
QUIZ_ICONS = ["03.02.09-vlans-in-a-multi-switched-environment-quiz/assets/3.2.9-1.png", "03.02.09-vlans-in-a-multi-switched-environment-quiz/assets/3.2.9-2.png",
              "03.02.09-vlans-in-a-multi-switched-environment-quiz/assets/3.2.9-3.png", "04.01.05-inter-vlan-routing-operation-quiz/assets/4.1.5-1.png",
              "04.01.05-inter-vlan-routing-operation-quiz/assets/4.1.5-2.png", "04.01.05-inter-vlan-routing-operation-quiz/assets/4.1.5-3.png",
              "16.01.02-packet-processing-with-static-routes-quiz/assets/16.1.2.png"]
for suf in QUIZ_ICONS:
    R(find(suf), "иконки сети в стиле Cisco/NetAcad", "visual", "рисунок к квизу в стиле NetAcad: иконки Cisco (коммутатор, L3-коммутатор, маршрутизатор, ПК)",
      "replace:<перерисовать схему в библиотеке курса>", "[D8]")
EXAM_TEXT = [
    ("01-04-exam/assets/12.png", "CiscoVille", "brand", "вывод CLI: «CiscoVille# configure terminal … CiscoVille(config-subif)#» — имя хоста с брендом", "replace:<нейтральное имя хоста>", "[D12] имя хоста в растре; в learn-metadata.json вопросы #35/#36/#41 ссылаются на то же имя"),
    ("01-04-exam/assets/8.png", "CiscoVille; ISL", "brand", "«CiscoVille(config)#…», сообщение IOS «…IEEE 802.1Q, or ISL vLAN.»", "replace:<нейтральное имя хоста>", "[D12][D4.2] имя хоста + ISL в сообщении IOS"),
    ("01-04-exam/assets/9.png", "CiscoVille", "brand", "«CiscoVille# configure terminal …»", "replace:<нейтральное имя хоста>", "[D12]"),
    ("01-04-exam/assets/17.jpg", "ip domain-name cisco.com", "brand", "«Switch1(config)# ip domain-name cisco.com»", "replace:<нейтральный домен, напр. example.com>", "[D12]"),
    ("05-06-exam/assets/3.png", "PAgP", "proprietary-tech", "вывод show etherchannel summary: «1 Po1(SU) PAgP Fa0/1(P) Fa0/2(P)»", "decide", "[D4.5] PAgP в выводе; сама команда — синтаксис"),
    ("05-06-exam/assets/7.png", "PAgP", "proprietary-tech", "вывод show etherchannel summary: «1 Po1(SD) PAgP …»", "decide", "[D4.5]"),
    ("07-09-exam/assets/4.png", "netacad.net", "brand", "«R1(config-dhcp)# domain-name netacad.net», «Domain name: netacad.net»", "replace:<нейтральный домен>", "[D12]"),
    ("07-09-exam/assets/5.png", "netacad.net", "brand", "«domain-name netacad.net», «Domain name: netacad.net»", "replace:<нейтральный домен>", "[D12]"),
    ("07-09-exam/assets/6.png", "netacad.net", "brand", "«R1(config-dhcp)# domain-name netacad.net»", "replace:<нейтральный домен>", "[D12]"),
    ("07-09-exam/assets/7.png", "netacad.com", "brand", "«domain-name netacad.com»", "replace:<нейтральный домен>", "[D12]"),
    ("07-09-exam/assets/9.png", "вывод show glbp (GLBP)", "proprietary-tech", "«FastEthernet0/1 - Group 1 … Load balancing: round-robin … Forwarder 1 … MAC address is 0007.b400.0101» — вывод GLBP", "decide", "[D4.4] слово GLBP в растре отсутствует, найдено визуально"),
    ("final-exam/assets/11.gif", "D … [90/21024000] (EIGRP)", "proprietary-tech", "вывод show ip route: «D 172.16.1.0 [90/21024000] via 172.16.0.1 …» — маршрут EIGRP", "keep", "[D4.6] найдено визуально"),
    ("final-exam/assets/2.png", "%CDP-4-NATIVE_VLAN_MISMATCH", "proprietary-tech", "«%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on FastEthernet0/1 (99), with DLS2 …»", "decide", "[D4.1] сообщение CDP в выводе; при отказе от CDP — аналог LLDP"),
    ("final-exam/assets/8.png", "domain-name cisco.com", "brand", "«domain-name cisco.com» в show running-config", "replace:<нейтральный домен>", "[D12]"),
]
for p, *rest in EXAM_TEXT:
    R(p, *rest)

PT_TOPO = ["01.03.06-lab-configure-ssh-ilm", "01.04.07-lab-configure-router-interfaces-ilm", "01.05.10-lab-verify-directly-connected-networks",
           "03.01.04-lab-who-hears-the-broadcast-ilm", "03.02.08-lab-investigate-a-vlan-implementation-ilm", "03.03.12-lab-vlan-configuration",
           "03.04.05-lab-configure-trunks", "03.05.05-lab-configure-dtp", "03.06.01-lab-implement-vlans-and-trunking",
           "04.02.07-lab-configure-router-on-a-stick-inter-vlan-routing", "04.03.08-lab-configure-layer-3-switching-and-inter-vlan-routing",
           "04.04.08-lab-troubleshoot-inter-vlan-routing", "04.05.01-lab-inter-vlan-routing-challenge", "05.01.09-lab-investigate-stp-loop-prevention",
           "06.02.04-lab-configure-etherchannel", "06.03.04-lab-troubleshoot-etherchannel", "07.02.10-lab-configure-dhcpv4", "07.04.01-lab-implement-dhcpv4",
           "09.03.03-lab-hsrp-configuration-guide", "11.01.10-lab-implement-port-security", "11.06.01-lab-switch-security-configuration",
           "13.01.10-lab-configure-a-wireless-network", "13.02.07-lab-configure-a-basic-wlan-on-the-wlc", "13.03.12-lab-configure-a-wpa2-enterprise-wlan-on-the-wlc",
           "13.04.05-lab-troubleshoot-wlan-issues", "13.05.01-lab-wlan-configuration", "14.03.05-lab-basic-router-configuration-review",
           "15.06.01-lab-configure-ipv4-and-ipv6-static-and-default-routes", "16.03.01-lab-troubleshoot-static-and-default-routes"]
PT_TOPO_EXTRA = {
    "07.02.10-lab-configure-dhcpv4": " Сервер «www.cisco.com» на схеме.",
    "07.04.01-lab-implement-dhcpv4": " Сервер «www.cisco.com» на схеме.",
    "13.01.10-lab-configure-a-wireless-network": " Сервер «www.cisco.pka».",
    "13.04.05-lab-troubleshoot-wlan-issues": " Подписи «www.netacad.pt», «admin/Cisco123», «LAP-1».",
    "13.05.01-lab-wlan-configuration": " Подписи «www.netacad.pt», «admin/Cisco123», «LAP-1».",
    "13.02.07-lab-configure-a-basic-wlan-on-the-wlc": " Устройства «WLC-1», «LAP-1».",
    "13.03.12-lab-configure-a-wpa2-enterprise-wlan-on-the-wlc": " Устройства «WLC-1», «LAP-1».",
    "06.02.04-lab-configure-etherchannel": " Подписи «PAgP», «LACP».",
}
for lab in PT_TOPO:
    p = find(lab + "/assets/topology.png")
    R(p, "скриншот логической топологии Packet Tracer", "visual", "снимок рабочей области PT: иконки устройств PT, зелёные/красные индикаторы линков." + PT_TOPO_EXTRA.get(lab, ""),
      "replace:<схема топологии в стиле курса (learn-netsim)>", "[D5][D8] меняется вместе с переводом лабы с PT")
NETACAD_TOPO = ["01.01.07-lab-basic-switch-configuration-physical-mode", "01.06.02-lab-configure-basic-router-settings-physical-mode",
                "03.04.06-lab-configure-vlans-and-trunking-physical-mode", "04.02.08-lab-configure-router-on-a-stick-inter-vlan-routing-non-pt",
                "04.04.09-lab-troubleshoot-inter-vlan-routing-physical-mode", "06.04.02-lab-implement-etherchannel", "07.04.02-lab-implement-dhcpv4",
                "08.05.01-lab-configure-dhcpv6", "11.06.02-lab-switch-security-configuration",
                "16.03.02-lab-troubleshoot-ipv4-and-ipv6-static-and-default-routes-physical-mode"]
for lab in NETACAD_TOPO:
    p = find(lab + "/assets/topology.png")
    R(p, "схема топологии из лабораторного руководства NetAcad", "visual", "синие иконки Cisco (маршрутизатор, коммутатор, ПК) в стиле Lab Manual NetAcad",
      "replace:<схема топологии в стиле курса>", "[D8]")

NATIVE = [
    ("01.01-configure-a-switch-with-initial-settings/assets/1.1.3.png", "логотип Cisco; Catalyst 2960 (лицевая панель)", "visual", "схема Cisco лицевой панели Catalyst 2960 с выносками 1–8 + фото панели с логотипом «cisco» и кнопкой MODE", "replace:<перерисовать панель NS01 с выносками>", "[D2][D8] raster-inventory: A, P1; чужая схема Cisco (штамп 204012)"),
    ("01.03-secure-remote-access/assets/1.3.1.png", "Password: ccna", "certification", "Wireshark, Follow TCP Stream сеанса Telnet: «Username: … Password: ccna»", "replace:<перехват с нейтральным паролем>", "[D12] пароль «ccna» в перехвате; raster-inventory: E (К1)"),  # ggignore: публичный учебный пароль из скриншота курса, не секрет
    ("01.03-secure-remote-access/assets/1.3.2.png", "SSH-2.0-Cisco-1.25", "cli-vendor-string", "Wireshark, поток SSH: строка версии сервера «SSH-2.0-Cisco-1.25»", "replace:<строка версии SSH NetOS>", "[D3] баннер SSH-сервера IOS"),
    ("07.03-configure-dhcpv4-client/assets/7.3.3.png", "HomeRouter-PT-AC (GUI Packet Tracer)", "visual", "GUI домашнего роутера PT: «Wireless Tri-Band Home Router», «HomeRouter-PT-AC», Setup → DHCP", "replace:<компонент К3 без имени модели PT>", "[D5][D8] raster-inventory: E (К3)"),
    ("10.02-access-control/assets/10.2.2.png", "фигура NetAcad (оранжевые выноски)", "visual", "кредитная карта + выписка, оранжевые выноски «Аутентификация / Авторизация / Учёт» в фирменном стиле NetAcad", "replace:<перерисовать в стиле курса>", "[D8] raster-inventory: B, P1"),
    ("10.05-lan-attacks/assets/10.5.10.png", "Cisco IOS Software, C3550…; Copyright (c) 1986-2007 by Cisco Systems; Platform: Cisco WS-C3550-24-PWR; Cisco_98:8c:95; CDP/VTP/DTP/PAgP/UDLD", "cli-vendor-string", "Wireshark, фильтр cdp: дерево Cisco Discovery Protocol — Software Version, Copyright Cisco Systems, Platform WS-C3550-24-PWR", "replace:<перехват LLDP/CDP с данными NetOS>", "[D3][D4.1] сразу cli-vendor-string + legal + model + proprietary-tech; raster-inventory: E (К1)"),
    ("12.02-components-of-wlans/assets/12.2.4.png", "Cisco Meraki (логотипы на корпусах)", "visual", "продуктовое фото двух точек доступа Cisco Meraki Go с логотипами «cisco» на корпусах", "remove", "[D8] raster-inventory: B (или C); в README 12.2.4 подпись «Точки доступа Cisco Meraki Go»"),
    ("12.06-wlan-threats/assets/12.6.4.png", "логотип Cisco; GUI WLC (TACACS+, FlexConnect)", "visual", "классический GUI WLC: логотип «cisco» в шапке, меню MONITOR…FEEDBACK, Rogue Policies, «Auto Containment on FlexConnect Standalone»", "replace:<компонент К6 без логотипа>", "[D5][D8] raster-inventory: E (К6)"),
    ("13.01-remote-site-wlan-configuration/assets/13.1.2-1.png", "Cisco Meraki MX64W (продуктовое фото)", "visual", "продуктовое фото Meraki MX64W, едва различимый логотип на корпусе", "replace:<изометрический роутер SOHO из библиотеки>", "[D2][D8] raster-inventory: B"),
    ("13.01-remote-site-wlan-configuration/assets/13.1.6.png", "фигура NetAcad + вырезки PT", "visual", "дом с роутером и mesh-узлами (стиль NetAcad) + две вырезки окна PT «Port 1» (каналы 1 и 11)", "replace:<перерисовать в стиле курса>", "[D5][D8] raster-inventory: A, P1"),
    ("13.01-remote-site-wlan-configuration/assets/13.1.7.png", "WRT300N (GUI Packet Tracer)", "visual", "GUI PT «Wireless-N Broadband Router», модель «WRT300N» (Linksys), Status → Router", "replace:<компонент К3 без имени модели>", "[D5][D8]"),
    ("13.01-remote-site-wlan-configuration/assets/13.1.8.png", "макет QoS NetAcad (Netgear-подобный)", "visual", "макет страницы «Настройка QoS» из материалов NetAcad (уже по-русски), стиль GUI Netgear", "decide", "[D8] вендора Cisco нет, но чужая фигура NetAcad; raster-inventory: E"),
    ("13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.3-1.png", "© 2005 - 2019 Cisco Systems, Inc. All rights reserved; trademarks of Cisco Systems; вкладка «Cisco Systems Login»", "legal", "Chrome: страница входа WLC 192.168.200.254 — внизу копирайт и текст о товарных знаках Cisco, вкладка «Cisco Systems Login»", "replace:<компонент К4 без копирайта>", "[D8] legal + brand в одном растре"),
    ("13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.3-2.png", "логотип Cisco; «Cisco 3500 Series Wireless Controller»; вкладка «CCNA7»", "visual", "новый GUI WLC: логотип, название продукта в шапке, вкладка браузера «CCNA7» (имя WLC)", "replace:<компонент К5 без логотипа>", "[D5][D8]"),
    ("13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.4.png", "AIR-AP1815I", "visual", "новый GUI WLC, Access Point View: Model «AIR-AP1815I-…», CDP/LLDP соседи", "replace:<компонент К5>", "[D2][D8] модель AP вендора в поле Model"),
    ("13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.5.png", "логотип Cisco; рисунок панели 3504; «Cisco CleanAir»; System Name «CCNA7»", "visual", "классический GUI WLC, Monitor → Summary: логотип, изображение лицевой панели 3504 с логотипом, пункт меню «Cisco CleanAir»", "replace:<компонент К6 без логотипа и панели>", "[D5][D8]"),
    ("13.02-configure-a-basic-wlc-on-the-wlc/assets/13.2.6-1.png", "логотип Cisco; «Cisco 3500 Series Wireless Controller»; «Model 3504»", "visual", "продуктовое фото лицевой панели Cisco 3504 с логотипом и надписями", "replace:<панель WLC в стиле курса>", "[D2][D8] raster-inventory: A (или D)"),
    ("13.04-troubleshoot-wlan-issues/assets/13.4.4-1.png", "Meraki Dashboard (my.meraki.com); вкладка «Cisco Meraki Local Device»", "visual", "страница статуса AP: «registered on the Meraki cloud», «Meraki cloud», адрес my.meraki.com", "replace:<карточка статуса в стиле курса>", "[D8] raster-inventory: E (или C)"),
]
for suf, *rest in NATIVE:
    R(find(suf), *rest)
PT_GUI = ["12.07-secure-wlans/assets/12.7.2-1.png", "12.07-secure-wlans/assets/12.7.2-2.png", "12.07-secure-wlans/assets/12.7.5.png",
          "12.07-secure-wlans/assets/12.7.6.png", "12.07-secure-wlans/assets/12.7.7.png", "13.01-remote-site-wlan-configuration/assets/13.1.3.png",
          "13.01-remote-site-wlan-configuration/assets/13.1.4-1.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.4-2.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.4-3.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.4-4.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.4-5.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.4-6.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.5-1.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.5-2.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.5-3.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.5-4.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.5-5.jpeg", "13.01-remote-site-wlan-configuration/assets/13.1.5-6.jpeg",
          "13.01-remote-site-wlan-configuration/assets/13.1.9.png"]
for suf in PT_GUI:
    extra = {"13.1.3.png": " Окно «Web Browser» PT + диалог Authorization.", "13.1.4-3.jpeg": " Диалог Authorization PT.",
             "13.1.4-6.jpeg": " Диалог Authorization PT.", "13.1.4-5.jpeg": " Окно PT «Command Prompt»: «Packet Tracer PC Command Line 1.0».",
             "13.1.5-6.jpeg": " Passphrase «cisco123»."}.get(suf.split("/")[-1], " Шапка «Wireless Tri-Band Home Router … HomeRouter-PT-AC».")
    R(find(suf), "GUI Packet Tracer (HomeRouter-PT-AC / Web Browser PT)", "visual", "скриншот GUI устройства Packet Tracer." + extra,
      "replace:<компонент К3/К4 в стиле курса>", "[D5][D8] raster-inventory: E (К3/К4)" + ("; [D12] пароль cisco123" if "5-6" in suf else ""))
WLC = [f for f in files if re.search(r"13\.0[234]-[^/]+/assets/13\.(2\.6-[2-8]|3\.\d+-\d|4\.4-2)\.(png|jpe?g)$", f)]
for p in sorted(WLC):
    fn = p.split("/")[-1]
    extra = {"13.3.4-1.jpg": " Меню «TACACS+».", "13.3.4-3.jpg": " Меню «TACACS+».", "13.3.4-2.jpg": " Флажок «Apply Cisco ISE Default settings».",
             "13.3.11-5.png": " Флажок «Apply Cisco ISE Default Settings».", "13.3.3-2.jpg": " Community Name «CCNAv7».",
             "13.2.6-7.png": " Пункт «Cisco CleanAir», рисунок панели 3504.", "13.2.6-8.png": " Пункт «Cisco CleanAir».",
             "13.4.4-2.png": " Раздел «FlexConnect»."}.get(fn, "")
    R(p, "логотип Cisco в шапке GUI WLC; вкладка браузера «CCNA7»", "visual",
      "классический GUI Cisco WLC 3504: логотип «cisco», меню MONITOR · WLANs · CONTROLLER … FEEDBACK." + extra,
      "replace:<компонент К6 без логотипа>", "[D5][D8] raster-inventory: E (К6)")

README_ASSETS = {
    "gif-1.png": ("Cisco; contenthub.netacad.com/srwe-dl; «Switching, Routing, and Wireless Essentials»", "brand", "скриншот курса на сайте NetAcad (логотип Cisco, URL contenthub.netacad.com/srwe-dl/2.1.1)"),
    "gif-2.png": ("Cisco; contenthub.netacad.com/srwe-dl; EtherChannel в меню", "brand", "скриншот курса на сайте NetAcad (логотип, URL, оглавление SRWE)"),
    "gif-4.png": ("страница курса NetAcad", "brand", "скриншот страницы NetAcad (вкладки браузера курса), анимация таблицы портов"),
    "gif-5.png": ("страница курса NetAcad", "brand", "скриншот страницы NetAcad, контекстное меню «сохранить как»"),
    "headers_example.png": ("Cisco; «Introduction to Networks»", "brand", "скриншот курса ITN на NetAcad (логотип Cisco, заголовки H1/H2)"),
    "hidden_text.png": ("интерфейс NetAcad", "brand", "скриншот «Модули 1-3: Содержание курса» в интерфейсе NetAcad"),
    "pictures.png": ("Cisco; /courses/itn-dl/…", "brand", "скриншот NetAcad + DevTools: путь /courses/itn-dl/… к SVG"),
    "quiz-example.png": ("Cisco; «Introduction to Networks»", "brand", "скриншот квиза в интерфейсе NetAcad"),
    "test-example.png": ("Cisco; Packet Tracer", "brand", "скриншот теста NetAcad («Packet Tracer. Представление…»)"),
    "video.png": ("Cisco; v7.02; ciscotest…@gmail.com", "brand", "скриншот NetAcad + DevTools (videocloud tracker), в форме виден e-mail вида ciscotest…@gmail.com"),
    "lab-topology-bad.png": ("Packet Tracer (скриншот топологии)", "product", "пример «плохой» топологии — скриншот PT"),
    "lab-topology-good.png": ("Packet Tracer (скриншот топологии)", "product", "пример «хорошей» топологии — скриншот PT"),
    "pt-editor.png": ("Packet Tracer Activity Wizard", "product", "окно Activity Wizard PT с инструкцией «Packet Tracer. Создание основных подключений»"),
    "pt-menu.png": ("«Cisco Packet Tracer - \\\\wsl$\\Ubuntu-20.04\\home\\menus12\\dev…»", "product", "меню Extensions → Activity Wizard; заголовок окна с локальным путём пользователя"),
    "writage-1.png": ("Packet Tracer (текст инструкции)", "product", "Word + Writage: инструкция лабы «Packet Tracer. Создание основных подключений»"),
    "writage-2.png": ("Packet Tracer PC Command Line", "product", "Word + Writage: блок кода «Packet Tracer PC Command Line 1.0»"),
}
for fn, (term, cat, exc) in README_ASSETS.items():
    note = "[D10] служебная иллюстрация к migration-instructions.md"
    if fn == "video.png":
        note += "; содержит адрес электронной почты — проверить, не персональные ли это данные"
    if fn == "pt-menu.png":
        note += "; содержит локальный путь и имя пользователя"
    R("readme-assets/" + fn, term, cat, exc, "decide", note, aud="internal")

# ---------------- binary docs
docinfo = json.load(open(os.path.join(S, "out", "doc_info.json")))
dochits = json.load(open(os.path.join(S, "out", "doc_hits.json")))
dh = collections.defaultdict(collections.Counter)
for h in dochits:
    dh[h["file"]][h["term"]] += 1
for f in sorted(docinfo):
    tc = dh[f]
    summ = ", ".join(f"{k} ×{v}" for k, v in tc.most_common(8))
    if f.startswith("packet-tracer-source-files/"):
        kind = "инструкция PT" if "Packet Tracer" in f else "лабораторная работа (реальное оборудование)"
        add(f, "lab-infra", "исходный .docx NetAcad: логотип «Cisco Networking Academy» в колонтитуле; «© … Корпорация Cisco… www.netacad.com» в нижнем колонтитуле", "lab-infra", "internal",
            f"{kind}; попадания словаря в тексте: {summ}"[:160], "decide",
            "[D5][D10] исходник, из которого собран README лабы; в курс не встраивается (ссылок из README нет). Колонтитул: legal + brand + link; все попадания словаря в .docx относятся к этой строке")
    elif f.startswith("readme-assets/"):
        add(f, "internal-doc", "документ Cisco «CCNAv7 SRWE Scope and Sequence» (Cisco Networking Academy®)", "certification", "internal",
            f"официальный документ NetAcad, {docinfo[f]['pages']} стр.; попадания: {summ}"[:160], "decide",
            "[D10][D13] опора нумерации курса (migration-instructions.md:23); содержит ®, ссылки netacad.com")
    else:
        add(f, "lab-infra", "PDF лабораторной работы NetAcad 4.2.8 (ru-RU): логотип NetAcad, «© 2013 г. - гггг Корпорация Cisco…», www.netacad.com, Cisco 4221/2960, IOS XE 16.9.4", "legal", "learner",
            f"PDF доступен обучающемуся по ссылке из README 04.02 (строка 323); {docinfo[f]['pages']} стр.; попадания: {summ}"[:160], "remove",
            "[D5][D8] чужой документ Cisco со знаком копирайта в учебном материале; README 04.02:323 ссылается на него")

# videos: skipped by operator request (already classified in videos/, will be re-made)

# ---------------- course-level rows
add("material-tags.json", "metadata", "название курса/репозитория «learn-ccna2», id ассетов «ccna2-…», страницы Figma «CCNA2 · …»", "certification", "internal",
    "репозиторий nsalab-tmn/learn-ccna2; figma-assets.json: course «ccna2», 288 id «ccna2-…», 215 страниц «CCNA2 · …»; animations/ccna2-*/; ccna2-labs.md",
    "decide", "[D1] сертификация вендора в имени курса и всех служебных идентификаторах; переименование задевает контракт Figma↔git и ссылки learn-ccna1/3")
add("migration-instructions.md", "internal-doc", "структура курса = SRWE v7 Scope and Sequence (нумерация и состав тем)", "certification", "internal",
    "каталоги NN.NN-…, маркеры <!-- 1.1.1 --> (432 шт. в 78 README), «Тема 3.5.0 -» в комментариях квизов повторяют нумерацию NetAcad",
    "decide", "[D13] migration-instructions.md:23 — «Именование лекций … согласно оригинальному scope & sequence»; маркеры не видны обучающемуся")
add("migration-instructions.md", "internal-doc", "текст курса — перевод/адаптация материалов NetAcad SRWE v7", "legal", "internal",
    "migration-instructions.md описывает перенос лекций, квизов и лаб из курса NetAcad («Пример: оригинал лекции из Netacad», строка 63)",
    "decide", "[D14] вопрос права, а не упоминаний: даже после чистки бренда текст, рисунки NetAcad и банк вопросов остаются производными от материалов Cisco")

json.dump(rows, open(os.path.join(S, "out", "rows_visual.json"), "w"), ensure_ascii=False, indent=0)
print(len(rows), "visual/doc/video/course rows")
print(collections.Counter(r["surface"] for r in rows))
