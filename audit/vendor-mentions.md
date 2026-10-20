# Аудит упоминаний вендора в курсе CCNA2 (SRWE) — сводка

Ответ на [nsalab-tmn/learn-ccna2#21](https://github.com/nsalab-tmn/learn-ccna2/issues/21). Срез: `origin/main` @ `88c6c4d` (2026-10-16). В материалах ничего не менялось — добавлен только каталог `audit/`.

Файлы:

- `audit/vendor-mentions.csv` — карта: **2233 строк**, колонки по issue (`id … note`).
- `dictionary-hits.csv` (план снят; открытые пункты — kb#291) — журнал **каждого** попадания словаря (текст, имена файлов, OCR картинок, текст `.docx`/`.pdf`): строка карты или «исключено» с причиной. По нему сходится N = M + K.
- `audit/vendor-mentions.md` — этот отчёт.

Как читать `note`: в начале стоит код решения `[D…]` из раздела «Решения для оператора». `action: decide` почти всегда ссылается на такой код — решать нужно по коду, а не построчно.

## 1. Главное

- В карте 2233 мест: 1939 видит обучающийся, 294 служебные. Больше всего проприетарных технологий (1100): это темы курса — EtherChannel/PAgP, HSRP/GLBP, DTP/VTP, PVST+, CDP. За ними бренд (337) и продукты (342, в основном Cisco IOS и Packet Tracer).
- **Проще всего**: убрать тег `"Cisco"` в `material-tags.json` (одна строка, ccna2-vm-2079 — тег наследуют все материалы); убрать 38 закомментированных ссылок «Скачать файл Packet Tracer» (`surface=comment`); убрать PDF NetAcad со знаком © в материале 04.02 (ccna2-vm-0310 — единственный чужой документ, доступный обучающемуся); заменить «cisco»/«ccna»/«netacad» в паролях, доменах и именах хостов (83 строк, D11).
- **Дороже всего**:
  - 40 лаб на Packet Tracer (D5), из них 12 завязаны на GUI PT (WLC, беспроводные устройства, физический режим PT);
  - около 160 растров чужого стиля (D8): экзаменационные схемы NetAcad, скриншоты GUI WLC с логотипом, скриншоты PT;
  - проприетарные протоколы как темы целых модулей 06 и 09 (D4).
- **Иллюстрации из Figma (SVG) почти чистые**: логотипов, надписей вендора и узнаваемых панелей моделей нет. Вендор есть только в подписях 13 рисунков (EtherChannel, PAgP, CDP, ESA/WSA/ISE/AMP, LWAPP, FlexConnect, MAC HSRP) и в одной анимации. Набор иконок нарисован заново, но повторяет смысл фирменных глифов Cisco (D7).
- **Ограничение этой сессии.** Figma API/MCP недоступен: токена `/home/menus12/…/figma_ci` в контейнере нет, Figma MCP не подключился (403 от прокси). Поэтому подписи иллюстраций прочитаны через OCR (tesseract eng+rus) и проверены глазами по рендерам `rsvg-convert`, а не из узлов `TEXT`. Лист `_Библиотека` оценён по 206 экспортированным SVG. Подробности — в §7.

## 2. Итоги

### По категориям

| category | строк | из них learner |
|---|---|---|
| proprietary-tech | 1100 | 1083 |
| product | 342 | 244 |
| brand | 337 | 321 |
| visual | 163 | 163 |
| lab-infra | 132 | 0 |
| model | 70 | 70 |
| certification | 53 | 27 |
| link | 22 | 18 |
| cli-vendor-string | 11 | 11 |
| legal | 3 | 2 |

### По поверхностям

| surface | строк |
|---|---|
| quiz | 862 |
| text | 717 |
| raster | 179 |
| metadata | 92 |
| lab-infra | 90 |
| comment | 78 |
| internal-doc | 75 |
| filename | 64 |
| code | 58 |
| illustration | 14 |
| animation | 3 |
| figma-library | 1 |

### По предложенному действию

| action | строк | из них learner |
|---|---|---|
| decide | 1264 | 1080 |
| replace | 527 | 499 |
| neutralize | 328 | 328 |
| remove | 79 | 3 |
| keep | 35 | 29 |

### По модулям (в порядке курса)

| module | всего | proprietary-tech | brand | product | model | cli-vendor-string | certification | visual | lab-infra | link | legal |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-basic-device-configuration | 130 | 5 | 22 | 49 | 18 | 5 | 11 | 6 | 12 | 2 |  |
| 02-switching-concepts | 4 |  | 2 |  | 1 |  |  |  |  | 1 |  |
| 03-vlans | 168 | 62 | 38 | 30 | 10 |  | 4 | 10 | 14 |  |  |
| 04-inter-vlan-routing | 61 | 9 | 5 | 15 | 8 | 2 | 1 | 9 | 11 |  | 1 |
| 01-04-exam | 67 | 14 | 22 | 12 | 8 |  |  | 11 |  |  |  |
| 05-stp | 84 | 46 | 21 | 13 |  |  |  | 1 | 2 | 1 |  |
| 06-etherchannel | 334 | 296 | 13 | 8 | 6 |  | 1 | 3 | 7 |  |  |
| 05-06-exam | 199 | 161 | 30 |  |  |  |  | 8 |  |  |  |
| 07-dhcpv4 | 47 | 2 | 12 | 19 | 3 |  | 2 | 4 | 5 |  |  |
| 08-slaac-and-dhcpv6-concepts | 20 |  | 6 | 8 | 3 |  | 1 | 1 | 1 |  |  |
| 09-fhrp-concepts | 180 | 133 | 27 | 14 | 1 |  |  | 1 | 4 |  |  |
| 07-09-exam | 65 | 39 | 21 |  |  |  |  | 5 |  |  |  |
| 10-lan-security-concepts | 111 | 43 | 24 | 39 |  | 1 |  | 1 |  | 3 |  |
| 11-switch-security-configuration | 84 | 56 | 5 | 9 | 4 |  | 2 | 3 | 5 |  |  |
| 12-wlan-concepts | 29 | 14 | 1 | 2 |  |  |  | 7 |  | 5 |  |
| 13-wlan-configuration | 153 | 23 | 30 | 16 | 7 |  |  | 58 | 12 | 6 | 1 |
| 10-13-exam | 61 | 35 | 9 | 13 |  |  |  | 4 |  |  |  |
| 14-routing-concepts | 67 | 41 | 12 | 9 |  | 1 | 1 | 1 | 2 |  |  |
| 15-ip-static-routing | 30 | 19 |  | 8 |  |  |  | 1 | 2 |  |  |
| 16-troubleshoot-static-and-default-routes | 29 | 10 | 5 | 5 |  | 2 |  | 3 | 4 |  |  |
| 14-16-exam | 31 | 10 |  | 4 |  |  |  | 17 |  |  |  |
| final-lab-part1 | 27 | 15 | 1 | 8 |  |  | 2 |  | 1 |  |  |
| final-lab-part2 | 7 | 3 |  | 1 |  |  | 2 |  | 1 |  |  |
| final-exam | 70 | 48 | 14 |  | 1 |  |  | 7 |  |  |  |
| (root) | 173 | 15 | 17 | 60 |  |  | 25 | 2 | 49 | 4 | 1 |
| (анимации) | 2 | 1 |  |  |  |  | 1 |  |  |  |  |

`(root)` — корневые и служебные файлы: `figma-assets.json`, `migration-instructions.md`, `ccna2-labs.md`, `calc_duration.txt`, `readme-assets/`, `packet-tracer-source-files/`.

## 3. Топ-20 самых «вендорных» материалов (по строкам, видимым обучающемуся)

| # | material | строк | основное |
|---|---|---|---|
| 1 | `05-06-exam` | 199 | proprietary-tech 161, brand 30, visual 8 |
| 2 | `06-etherchannel/06.04.04-quiz` | 86 | proprietary-tech 83, brand 3 |
| 3 | `final-exam` | 70 | proprietary-tech 48, brand 14, visual 7 |
| 4 | `09-fhrp-concepts/09.03.02-quiz` | 69 | proprietary-tech 49, brand 17, product 3 |
| 5 | `01-04-exam` | 67 | brand 22, proprietary-tech 14, product 12 |
| 6 | `07-09-exam` | 65 | proprietary-tech 39, brand 21, visual 5 |
| 7 | `10-13-exam` | 61 | proprietary-tech 35, product 13, brand 9 |
| 8 | `06-etherchannel/06.01-etherchannel-operation` | 48 | proprietary-tech 42, brand 4, model 1 |
| 9 | `06-etherchannel/06.02.04-lab-configure-etherchannel` | 45 | proprietary-tech 43, model 1, visual 1 |
| 10 | `05-stp/05.04.02-quiz` | 39 | proprietary-tech 24, product 8, brand 7 |
| 11 | `10-lan-security-concepts/10.06.02-quiz` | 36 | brand 16, proprietary-tech 15, product 5 |
| 12 | `09-fhrp-concepts/09.03.03-lab-hsrp-configuration-guide` | 33 | proprietary-tech 27, product 5, visual 1 |
| 13 | `14-16-exam` | 31 | visual 17, proprietary-tech 10, product 4 |
| 14 | `03-vlans/03.06.04-quiz` | 26 | brand 16, proprietary-tech 9, product 1 |
| 15 | `13-wlan-configuration/13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc` | 26 | visual 22, link 4 |
| 16 | `final-lab-part1` | 26 | proprietary-tech 15, product 8, certification 2 |
| 17 | `06-etherchannel/06.03-verify-and-troubleshoot-etherchannel` | 25 | proprietary-tech 25 |
| 18 | `03-vlans/03.05-dynamic-trunking-protocol` | 24 | proprietary-tech 16, brand 4, model 3 |
| 19 | `11-switch-security-configuration/11.06.04-quiz` | 24 | proprietary-tech 18, brand 5, product 1 |
| 20 | `01-basic-device-configuration/01.01-configure-a-switch-with-initial-settings` | 23 | product 11, model 7, cli-vendor-string 3 |

Экзамены и квизы стоят наверху, потому что одно и то же пояснение («HSRP и GLBP — собственные протоколы компании Cisco…») повторяется в `comment` каждого варианта ответа. Сами правки там почти механические.

## 4. Решения для оператора

Решения сгруппированы по типам. В скобках — сколько строк CSV ссылаются на код.

### D1. Имя курса и служебные идентификаторы («CCNA», «SRWE») — 12 строк

**Где:**
- репозиторий `learn-ccna2`;
- `figma-assets.json`: `course: ccna2`, 288 id `ccna2-…`, 215 имён страниц «CCNA2 · …»;
- каталоги `animations/ccna2-*`, файл `ccna2-labs.md`;
- заголовки «SRWE-F1/F2» и `shortName: srwe-f1` в `final-lab-part1/2`;
- ссылки `learn-ccna1#…` в `.github/scripts`.

Сводная строка — ccna2-vm-2078.

**Рекомендация:** переименовать только то, что видит обучающийся: заголовки и `shortName` финальных лаб (ccna2-vm-1979…ccna2-vm-1988). Служебные id (`ccna2-…`, страницы Figma, имя репозитория) оставить: они связывают Figma и git, обучающийся их не видит, а переименование задевает learn-ccna1/3 и CI. Решать вместе с названием траектории в `learn-metadata.json` — в нём вендора уже нет.

### D2. Модели оборудования → идентичность learn-netsim — 90 строк

| что в курсе | предложение |
|---|---|
| Catalyst 2960 / 2950, `WS-C…` | **NS01** |
| Catalyst 3560 / 3650 / 3550 (L3-коммутатор) | **NS01** при условии, что NS01 умеет L3 (SVI, `ip routing`); иначе нужна модель L3 — **вопрос к learn-netsim** |
| 1941, 2901, 2911, 4221, 4321, ISR, `ISR4221-2x1GE` | **NR01** (вторая модель в той же топологии — **NR02**) |
| ПК / сервер в топологиях | **NPC** |
| WLC 3504, Aironet 1815i, `AIR-AP1815I` | аналога нет → «контроллер WLC», «точка доступа» (зависит от D5) |
| Meraki Go / MX64W, RV130W, WRT300N (Linksys) | → «беспроводной роутер SOHO», «точка доступа» |

Отдельный случай — типовое примечание «Роутеры, используемые в практических лабораторных работах CCNA, — это Cisco 4221 с Cisco IOS XE 16.9.4 (образ universalk9)…» в 5 лабах без PT. Его лучше заменить общим абзацем про learn-netsim, а не править модели по одной.

### D3. Cisco IOS как продукт и вендорные строки в выводе CLI — 149 строк

- «IOS / Cisco IOS» как название ОС — 132 строк. Предложение: **NetOS** (NSALAB NetOS), где речь об ОС устройства; нейтрально «ОС устройства», где бренд не важен.
- `cli-vendor-string` и имена образов:
  - баннер `Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.0(2)SE7` (01.03, строка 36);
  - `Hardware is ISR4221-2x1GE`;
  - колонка Platform в `show cdp neighbors` (`WS-C3560-`, `ISR4221/K`);
  - имена образов `c2960-lanbasek9-mz.150-2.SE8.bin` в 01.01;
  - `SSH-2.0-Cisco-1.25` и дерево CDP с `Copyright … Cisco Systems` в растрах 1.3.2 и 10.5.10.

  Предложение: перегенерировать выводы из learn-netsim. **Нужно от learn-netsim:** строка версии, имя платформы и имя образа NetOS.
- Синтаксис команд не трогаем (по issue). Исключение — вендорное ключевое слово `mls qos trust device cisco-phone` (03.03): решить, оставлять ли пример.

### D4. Проприетарные протоколы и технологии — 1132 строк

Решение принимается по протоколу. В тексте почти везде есть фраза «собственный/проприетарный протокол Cisco» — её стоит переписать в любом варианте (например, «проприетарный протокол одного производителя»).

| код | что | строк | где в курсе | рекомендация |
|---|---|---|---|---|
| D4.1 | CDP | 57 | 10.5 (CDP-разведка), 11.x, 16.2 `show cdp neighbors`, 3.1.3, 13.2 | основным протоколом обнаружения сделать **LLDP**; CDP оставить одним примером в теме атак, без бренда; `show cdp …` → `show lldp …` (нужна поддержка в learn-netsim) |
| D4.2 | DTP, VTP, ISL | 118 | 3.3, 3.5 (лаба 3.5.5 «настройка DTP»), 10.5, 11.x | DTP оставить как тему безопасности («автосогласование транка»), без бренда; VTP — кратко; **ISL убрать** (устарел), оставить 802.1Q |
| D4.3 | PVST+/Rapid PVST+, PortFast, BPDU Guard, Root/Loop Guard, UplinkFast/BackboneFast | 137 | модуль 05, 11.5 | подавать как «STP на каждую VLAN», упомянуть MSTP (802.1s); PortFast/BPDU Guard оставить как ключевые слова CLI и пояснить стандартным термином (edge port); UplinkFast/BackboneFast убрать (встроено в RSTP). Команды — синтаксис |
| D4.4 | HSRP, GLBP | 174 | модуль 09 целиком, лаба 9.3.3 «HSRP Configuration Guide», рисунок 9.2.2 (MAC 0000.0C07.AC01), экзамен 07-09 | **крупное решение.** Основным FHRP сделать **VRRPv3** (RFC 5798) и переписать 9.2/9.3 и лабу 9.3.3 под VRRP (нужна поддержка в learn-netsim); HSRP/GLBP — абзац «проприетарные варианты» |
| D4.5 | EtherChannel, PAgP | 457 | модуль 06 целиком (и имя каталога), 5 лаб, экзамены | «агрегирование каналов (LAG, IEEE 802.1AX / LACP)»; EtherChannel — синоним при первом упоминании; основной протокол — **LACP**, PAgP упомянуть. Ключевые слова `channel-group`, `show etherchannel` — синтаксис (исключены из подсчёта) |
| D4.6 | EIGRP, IGRP | 59 | 14.5 (история протоколов), легенда `show ip route`, экзамены | оставить как пример (EIGRP описан в RFC 7868), без слова Cisco; легенду кодов `show ip route` менять вместе с форматом вывода learn-netsim |
| D4.7 | CEF | 24 | 14.2 | описывать «FIB + таблица смежности»; CEF — как пример реализации |
| D4.8 | LWAPP, LAP, FlexConnect | 36 | 12.2, 12.4, 13.x | основным сделать **CAPWAP** (RFC 5415); «облегчённая AP» без аббревиатуры LAP; FlexConnect → «локальная коммутация на AP» |
| D4.9 | SPAN, UDLD, TACACS+ и прочее | 25 | 10.x, 7.2 (порт 49) | SPAN → «зеркалирование портов»; TACACS+ (RFC 8907) и UDLD — keep |
| D4.10 | продукты безопасности и облако: ESA/WSA, AMP, ISE, Secure ACS, ASA, Talos, Meraki | 45 | 10.1, 10.2, квизы модуля 10, 12.2, 13.1, 13.4 | neutralize: «шлюз безопасности почты», «веб-прокси», «защита конечных точек», «NAC-сервер», «облачная панель управления»; цитату «по данным Cisco Talos…» убрать или дать с нейтральным источником |

### D5. Packet Tracer и лабораторная инфраструктура — 337 строк

- **45 лаб.** На learn-netsim ещё не переведена ни одна; в CCNA2 нет аналога learn-ccna1#53.
- **40 лаб на PT.** Каждая — `.pka`, `deploy/pt-lab` (VM с PT, `pt-url`, `pt-api-port`) и `assessment/ms.yaml` с аспектами «Register packet tracer aspect mark». Одна строка на лабу, например ccna2-vm-0026.
- **Из них 12 с GUI-зависимостью** (`action: decide`): WLAN/WLC-лабы модуля 13 и лабы «physical mode» (физическая рабочая область PT: стойка, кабели). Прямой замены в learn-netsim у них нет:
  `01.01.07-lab-basic-switch-configuration-physical-mode`, `01.06.02-lab-configure-basic-router-settings-physical-mode`, `03.04.06-lab-configure-vlans-and-trunking-physical-mode`, `04.04.09-lab-troubleshoot-inter-vlan-routing-physical-mode`, `09.03.04-lab-data-center-exploration-physical-mode`, `13.01.10-lab-configure-a-wireless-network`, `13.02.07-lab-configure-a-basic-wlan-on-the-wlc`, `13.03.12-lab-configure-a-wpa2-enterprise-wlan-on-the-wlc`, `13.04.05-lab-troubleshoot-wlan-issues`, `13.05.01-lab-wlan-configuration`, `13.05.02-lab-wireless-technology-exploration-physical-mode`, `16.03.02-lab-troubleshoot-ipv4-and-ipv6-static-and-default-routes-physical-mode`
  Варианты: (а) оставить на PT как переходный fallback (так в `decisions/packet-tracer-substitution.md`); (б) переписать в CLI-форму; (в) снять.
- **5 лаб без среды выполнения** — бывшие лабы на реальном оборудовании: `deploy` создаёт только Azure resource group и учётку, оценки нет:
  `04.02.08-lab-configure-router-on-a-stick-inter-vlan-routing-non-pt`, `06.04.02-lab-implement-etherchannel`, `07.04.02-lab-implement-dhcpv4`, `08.05.01-lab-configure-dhcpv6`, `11.06.02-lab-switch-security-configuration`
  Решить: перевести на learn-netsim или убрать.
- Ссылки и текст:
  - 38 закомментированных ссылок `<!-- [Скачать файл Packet Tracer…](./assets/N-lab.pka) -->` → remove;
  - «Packet Tracer» в видимом тексте → «симулятор»;
  - имена устройств PT в шагах лаб (`LAP-PT`, `PT-HOST-NM-1CFE`, `HomeRouter-PT-AC`) → вместе с переводом лабы.
- `packet-tracer-source-files/` — 44 исходных `.docx` NetAcad. В каждом логотип «Cisco Networking Academy» в верхнем колонтитуле и «© … Корпорация Cisco… www.netacad.com» в нижнем. Из курса на них ссылок нет. Решать вместе с D9.

### D6. Видео — вне аудита (16 строк встраиваний)

По указанию оператора документы `videos/` не разбирались. Все 15 роликов уже классифицированы в `videos/README.md` (учебные ролики NetAcad CCNA 7 SRWE на канале оператора, маркетинговых нет) и будут пересобраны. Попадания словаря в `videos/*.md` занесены в журнал как исключённые с этой причиной. В карте остались только 15 строк встраиваний `![youtube](…)` в README материалов и одна фраза «перенаправлены на YouTube» (10.5) — их меняют при замене роликов.

### D7. Библиотека иконок Figma (лист `_Библиотека`) — ccna2-vm-2073

**Наблюдение.** Иконки — собственная изометрическая отрисовка: свой синий, стохастическая тень, свои ПК и серверы, без логотипов и надписей. Но **смысл глифов повторяет набор сетевых иконок Cisco**:
- маршрутизатор — цилиндр с четырьмя стрелками «крестом»;
- коммутатор — блок с двумя парами встречных стрелок;
- L3-коммутатор — блок со «звездой» стрелок;
- WLC, AP, межсетевой экран из «кирпичей».

**Рекомендация: keep.** Эти глифы — де-факто отраслевая нотация (ими рисуют и вендоро-независимые учебники), прямого копирования нет. Если нужна полная независимость, перерисовывать стоит маршрутизатор и L3-коммутатор — они узнаваемее всего. Оценка сделана по 206 экспортированным SVG; сам лист в Figma в этой сессии не открыт.

### D8. Растры и рисунки чужого стиля — 163 строк

| семейство | растров | что делать |
|---|---|---|
| экзаменационные и квизовые схемы NetAcad (бирюзовые 3D-иконки Cisco) | 59 | перерисовать в библиотеке курса; в `raster-inventory-ccna2.md` их нет — это новый объём работ |
| GUI Cisco WLC с логотипом (классический и новый UI, вкладка браузера «CCNA7», страница входа с ©) | 35 | компоненты К4/К5/К6 из `raster-inventory-ccna2.md`, без логотипа; зависит от D5 |
| скриншоты логической топологии Packet Tracer (`topology.png` лаб) | 29 | схема топологии в стиле курса — вместе с переводом лабы |
| GUI Packet Tracer (HomeRouter-PT-AC, WRT300N, Web Browser PT, Command Prompt PT) | 21 | компоненты К3/К4 |
| схемы из лабораторных руководств NetAcad (синие иконки Cisco) | 10 | перерисовать |
| продуктовые фото и схемы с логотипом (1.1.3 Catalyst 2960, 12.2.4 Meraki, 13.1.2-1 MX64W, 13.2.6-1 WLC 3504, 13.4.4-1 Meraki Dashboard) | 5 | как в raster-inventory (A/B/C) |
| Wireshark с вендорными данными (1.3.1 пароль ccna, 1.3.2 SSH-2.0-Cisco, 10.5.10 дерево CDP) | 3 | компонент К1 с нейтральными данными |
| фигуры NetAcad (10.2.2, 13.1.6, 13.1.8) | 3 | перерисовать |
| CLI-растры экзаменов с брендом в значениях (CiscoVille, cisco.com, netacad.net) или протоколами (PAgP, GLBP, CDP, EIGRP) | 14 | D11 / D4 |

Всего 179 строк `surface=raster`. Служебные `readme-assets/*.png` — в D9.

30 растров без вендора: CLI-скриншоты без бренда, диалоги Windows, стоковые фото, окно WannaCry. Они перечислены в таблице покрытия (§6) и в карту не попали.

### D9. Служебные документы и имена файлов/каталогов — 143 строк

**Служебные документы** (обучающемуся не показываются):
- `migration-instructions.md` — описывает перенос курса из NetAcad: srwe-v7, ITN, ссылки на netacad;
- `ccna2-labs.md` — колонка PT / non PT;
- `calc_duration.txt`;
- `readme-assets/`:
  - скриншоты сайта NetAcad с логотипом Cisco;
  - PDF «CCNAv7 SRWE Scope and Sequence» с ®;
  - `pt-menu.png` с локальным путём пользователя;
  - `video.png` с видимым адресом электронной почты.

**Рекомендация:** пока репозиторий закрыт — keep. Перед публикацией убрать `readme-assets/*` со скриншотами NetAcad, PDF Scope & Sequence и `packet-tracer-source-files/*.docx`. `video.png` и `pt-menu.png` проверить на персональные данные в любом случае.

**Имена каталогов:**
- суффикс `-ilm` (Instructor Lab Manual NetAcad) — 4 лабы;
- `-non-pt` — 1 лаба;
- `06-etherchannel/…etherchannel…`, `…-hsrp-…`, `…-dtp` — имена тем, решаются вместе с D4.

**Рекомендация:** каталоги переименовывать только вместе с миграцией путей на платформе — путь служит идентификатором материала.

### D10. Тег «Cisco» — ccna2-vm-2079

`material-tags.json` = `["Network", "Cisco"]`. Тег наследуют все материалы через `$ref`. **remove** (или заменить нейтральным тегом).

### D11. Бренд и сертификация как значения конфигурации — 83 строк

**Где встречается:**
- пароли: `cisco`, `Cisco123`, `Cisco123!`, `cisco123`, `Ciscoenpa55`, `Ciscolinepa55`, `$cisco!PRIV*`, `ccna`;
- имена хостов, SSID и community: `CiscoVille`, `ciscolab`, `ciscosb1`, `CCNAv7`;
- домены и URL: `cisco.com`, `ccna-lab.com`, `CCNA-lab.com`, `CCNA2.Lab-11.6.1`, `netacad.pka`, `www.cisco.pka`, `www.netacad.pt`, `netacad.net`.

**Рекомендация:** replace на нейтральные значения. **Важно:** в PT-лабах эти значения зашиты в `.pka` и в `assessment` — менять синхронно с топологией и проверками, иначе оценка сломается.

### D12. Структура курса = SRWE v7 Scope and Sequence — ccna2-vm-2080

Нумерация и состав тем повторяют NetAcad:
- каталоги `NN.NN-…`;
- 432 маркера `<!-- 1.1.1 -->` в 78 README;
- «Тема 3.5.0 -» в пояснениях квизов;
- `migration-instructions.md:23`: «согласно оригинальному scope & sequence».

Обучающийся маркеров не видит. Решить, сохраняем ли мы нумерацию SRWE как опору.

### D13. Производный контент (вопрос права) — ccna2-vm-2081

Это не упоминание, но главный вывод аудита. Текст лекций, банк вопросов квизов и экзаменов, рисунки и ролики — перевод и адаптация материалов NetAcad SRWE v7 (см. `migration-instructions.md`). Чистка бренда делает курс вендоро-нейтральным по виду, но не меняет происхождения материала. Рекомендую решить это до массовых правок: от ответа зависит, чистить ли текст точечно (D1–D12) или переписывать.

## 5. Сверка полноты по словарю (N = M + K)

Единица подсчёта — одно попадание регулярного выражения (без учёта регистра) в строке файла, в имени файла или каталога, в OCR-тексте картинки или в извлечённом тексте `.docx`/`.pdf`. M — попадания, покрытые строкой карты. Несколько соседних попаданий одной категории на строке файла сливаются в одну строку: «Cisco Catalyst 2960» — одна строка `model`. Для лаб все попадания в `deploy/`, `assessment/` и `assessment.json` покрыты одной строкой на лабу, как просит issue. K — исключено с причиной. Полный журнал — `dictionary-hits.csv` (план снят; открытые пункты — kb#291).

Колонка «файлов (текст)» — число текстовых файлов с совпадением, без SVG и бинарных; сверяется с ориентиром из issue. В колонке regex знак `¦` означает `|` (заменён, чтобы не ломать таблицу).

| термин | regex (i) | словарь | файлов (текст) | N | M | K | источники | причины K |
|---|---|---|---|---|---|---|---|---|
| `cisco` | `cisco` | issue | 120 | 1200 | 1057 | 143 | text 671, ocr-raster 101, pdf 52, docx 376 | видео вне аудита по указанию оператора 143 |
| `сиско` | `сиско` | issue | 0 | 0 | 0 | 0 |  |  |
| `циско` | `циско` | issue | 0 | 0 | 0 | 0 |  |  |
| `netacad` | `netacad` | issue | 4 | 120 | 119 | 1 | text 5, ocr-raster 10, pdf 15, docx 90 | видео вне аудита по указанию оператора 1 |
| `networking academy` | `networking\s+academy` | issue | 16 | 19 | 2 | 17 | text 17, pdf 2 | видео вне аудита по указанию оператора 17 |
| `сетевая академия` | `сетев\w*\s+академи` | issue | 0 | 0 | 0 | 0 |  |  |
| `академи` | `академи` | issue | 1 | 1 | 0 | 1 | text 1 | видео вне аудита по указанию оператора 1 |
| `linksys` | `linksys` | added | 5 | 20 | 18 | 2 | text 20 | видео вне аудита по указанию оператора 2 |
| `talos` | `\btalos\b` | added | 1 | 2 | 2 | 0 | text 2 |  |
| `ccna` | `ccna` | issue | 88 | 809 | 783 | 26 | text 735, filename 19, ocr-raster 21, pdf 20, docx 14 | видео вне аудита по указанию оператора 26 |
| `ccnp` | `ccnp` | issue | 0 | 0 | 0 | 0 |  |  |
| `ccent` | `ccent` | issue | 0 | 0 | 0 | 0 |  |  |
| `itn` | `itn` | issue | 1 | 6 | 6 | 0 | text 2, ocr-raster 2, pdf 2 |  |
| `srwe` | `srwe` | issue | 19 | 31 | 15 | 16 | text 22, filename 1, ocr-raster 2, pdf 6 | видео вне аудита по указанию оператора 16 |
| `ensa` | `ensa` | issue | 1 | 2 | 1 | 1 | text 1, pdf 1 | ложное совпадение 1 |
| `v7` | `v7` | issue | 3 | 25 | 15 | 10 | text 12, filename 1, ocr-raster 1, pdf 11 | видео вне аудита по указанию оператора 10 |
| `scope and sequence` | `scope\s+and\s+sequence` | added | 1 | 1 | 1 | 0 | text 1 |  |
| `ilm` | `\bilm\b` | added | 6 | 24 | 24 | 0 | text 16, filename 8 |  |
| `packet tracer` | `packet[\s_-]*tra?cer` | issue | 88 | 1540 | 1537 | 3 | text 1478, filename 32, ocr-raster 3, docx 22, pdf 5 | видео вне аудита по указанию оператора 3 |
| `PT` | `\bPT\b` | issue | 168 | 3283 | 3281 | 2 | text 3221, filename 43, ocr-raster 16, docx 2, pdf 1 | ложное совпадение 1; видео вне аудита по указанию оператора 1 |
| `.pka` | `\.pka` | issue | 79 | 175 | 175 | 0 | text 128, filename 40, ocr-raster 1, docx 6 |  |
| `.pkt` | `\.pkt` | issue | 0 | 0 | 0 | 0 |  |  |
| `webex` | `webex` | issue | 0 | 0 | 0 | 0 |  |  |
| `meraki` | `meraki` | issue | 3 | 8 | 8 | 0 | text 4, ocr-raster 4 |  |
| `catalyst` | `catalyst` | issue | 27 | 69 | 67 | 2 | text 51, pdf 2, docx 16 | видео вне аудита по указанию оператора 2 |
| `ISR` | `\bISR\b` | issue | 3 | 5 | 5 | 0 | text 5 |  |
| `nexus` | `nexus` | issue | 0 | 0 | 0 | 0 |  |  |
| `ASA` | `\bASA\b` | issue | 1 | 3 | 3 | 0 | text 3 |  |
| `anyconnect` | `anyconnect` | issue | 0 | 0 | 0 | 0 |  |  |
| `dna center` | `dna\s+center` | issue | 0 | 0 | 0 | 0 |  |  |
| `IOS` | `\bIOS\b` | issue | 57 | 268 | 262 | 6 | text 168, pdf 10, docx 90 | видео вне аудита по указанию оператора 6 |
| `IOS XE` | `IOS[\s-]XE` | issue | 4 | 26 | 26 | 0 | text 8, pdf 2, docx 16 |  |
| `NX-OS` | `NX-OS` | issue | 0 | 0 | 0 | 0 |  |  |
| `aironet` | `aironet` | added | 1 | 1 | 1 | 0 | text 1 |  |
| `ESA/WSA` | `\bESA\b¦\bWSA\b¦email\s+security\s+appliance¦web\s+security\s+appliance` | added | 7 | 46 | 42 | 4 | text 41, ocr-svg 5 | видео вне аудита по указанию оператора 3; ложное совпадение 1 |
| `AMP` | `\bAMP\b` | added | 2 | 5 | 5 | 0 | text 4, ocr-svg 1 |  |
| `ISE` | `\bISE\b` | added | 3 | 5 | 3 | 2 | text 3, ocr-svg 1, ocr-raster 1 | видео вне аудита по указанию оператора 2 |
| `Secure ACS` | `\bACS\b` | added | 1 | 9 | 9 | 0 | text 9 |  |
| `RV130W` | `\bRV\s?\d{3}W?\b` | added | 2 | 7 | 0 | 7 | text 7 | видео вне аудита по указанию оператора 7 |
| `MX64W` | `\bMX64W?\b` | added | 1 | 2 | 2 | 0 | text 2 |  |
| `WRT300N` | `\bWRT\d+N?\b` | added | 0 | 1 | 1 | 0 | ocr-raster 1 |  |
| `models` | `\b(1941¦2901¦2911¦2960¦3560¦3650¦4221¦4321)\b` | issue | 27 | 134 | 134 | 0 | text 71, pdf 5, docx 58 |  |
| `models+` | `\b(1841¦2811¦2950¦3550¦3750¦3850¦4331¦3504¦1815)\b` | added | 9 | 30 | 12 | 18 | text 25, pdf 1, docx 4 | видео вне аудита по указанию оператора 18 |
| `WS-C` | `WS-C` | issue | 2 | 5 | 3 | 2 | text 3, ocr-raster 1, pdf 1 | видео вне аудита по указанию оператора 2 |
| `ISR\d` | `\bISR\d{3,4}` | added | 3 | 5 | 5 | 0 | text 4, pdf 1 |  |
| `c\d{4} (image/platform)` | `\bc\d{4}(?:[a-z0-9]*)` | added | 6 | 24 | 15 | 9 | text 21, ocr-raster 1, docx 1, pdf 1 | ложное совпадение 4; видео вне аудита по указанию оператора 5 |
| `IOS image` | `universalk9¦lanbase¦ipbase` | added | 7 | 62 | 62 | 0 | text 24, pdf 4, docx 34 |  |
| `IOS version` | `\b1[0-7]\.\d\(\d+\)[A-Z]*\d*` | added | 7 | 37 | 35 | 2 | text 12, pdf 2, docx 23 | видео вне аудита по указанию оператора 2 |
| `CDP` | `\bCDP\b` | issue | 17 | 135 | 79 | 56 | text 131, ocr-raster 1, docx 3 | видео вне аудита по указанию оператора 56 |
| `EIGRP` | `EIGRP` | issue | 15 | 79 | 79 | 0 | text 74, ocr-svg 1, docx 4 |  |
| `HSRP` | `HSRP` | issue | 19 | 239 | 239 | 0 | text 200, filename 4, docx 33, pdf 2 |  |
| `GLBP` | `GLBP` | issue | 5 | 71 | 71 | 0 | text 71 |  |
| `VTP` | `\bVTP\b` | issue | 5 | 12 | 11 | 1 | text 11, ocr-raster 1 | видео вне аудита по указанию оператора 1 |
| `DTP` | `\bDTP\b` | issue | 34 | 177 | 171 | 6 | text 149, filename 2, ocr-raster 1, docx 23, pdf 2 | видео вне аудита по указанию оператора 6 |
| `ISL` | `\bISL\b` | issue | 3 | 6 | 6 | 0 | text 5, ocr-raster 1 |  |
| `PVST` | `PVST` | issue | 11 | 69 | 69 | 0 | text 67, docx 1, pdf 1 |  |
| `PAgP` | `\bPAgP\b` | added | 11 | 225 | 224 | 1 | text 198, ocr-svg 1, ocr-raster 4, docx 22 | видео вне аудита по указанию оператора 1 |
| `CEF` | `\bCEF\b¦cisco\s+express\s+forwarding` | added | 8 | 35 | 35 | 0 | text 35 |  |
| `LWAPP/LAP` | `\bLWAPP\b¦\bLAP\b` | added | 11 | 53 | 51 | 2 | text 31, ocr-svg 1, ocr-raster 4, docx 17 | видео вне аудита по указанию оператора 2 |
| `FlexConnect` | `flexconnect` | added | 10 | 52 | 37 | 15 | text 38, ocr-svg 1, ocr-raster 3, docx 10 | видео вне аудита по указанию оператора 15 |
| `EtherChannel` | `etherchannel` | added | 40 | 866 | 833 | 33 | text 762, filename 13, ocr-svg 4, ocr-raster 4, docx 75, pdf 8 | синтаксис CLI в стиле IOS 33 |
| `PortFast` | `portfast` | added | 18 | 187 | 158 | 29 | text 176, ocr-svg 1, docx 9, pdf 1 | синтаксис CLI в стиле IOS 29 |
| `BPDU Guard` | `bpdu\s?guard` | added | 16 | 97 | 79 | 18 | text 89, ocr-svg 1, docx 6, pdf 1 | синтаксис CLI в стиле IOS 16; видео вне аудита по указанию оператора 2 |
| `Root/Loop Guard` | `root\s?guard¦loop\s?guard` | added | 5 | 18 | 17 | 1 | text 18 | синтаксис CLI в стиле IOS 1 |
| `UplinkFast/BackboneFast` | `uplinkfast¦backbonefast` | added | 3 | 5 | 3 | 2 | text 5 | синтаксис CLI в стиле IOS 2 |
| `SPAN/RSPAN` | `\bR?SPAN\b` | added | 3 | 7 | 0 | 7 | text 7 | ложное совпадение 4; синтаксис CLI 2; видео вне аудита по указанию оператора 1 |
| `UDLD` | `\bUDLD\b` | added | 1 | 1 | 0 | 1 | text 1 | видео вне аудита по указанию оператора 1 |
| `TACACS+` | `tacacs` | added | 7 | 30 | 29 | 1 | text 27, ocr-raster 3 | видео вне аудита по указанию оператора 1 |
| `©` | `©` | issue | 0 | 211 | 102 | 109 | ocr-svg 56, ocr-raster 55, pdf 12, docx 88 | OCR-артефакт 109 |
| `®` | `®` | issue | 0 | 35 | 2 | 33 | ocr-svg 18, ocr-raster 15, pdf 2 | OCR-артефакт 33 |
| `™` | `™` | issue | 0 | 7 | 1 | 6 | ocr-svg 4, ocr-raster 2, pdf 1 | OCR-артефакт 6 |
| `copyright` | `copyright` | issue | 0 | 1 | 1 | 0 | ocr-raster 1 |  |
| `товарн` | `товарн` | issue | 0 | 0 | 0 | 0 |  |  |
| `cisco.com` | `cisco\.com` | issue | 2 | 9 | 6 | 3 | text 5, ocr-raster 4 | видео вне аудита по указанию оператора 3 |
| `netacad.com` | `netacad\.com` | added | 0 | 105 | 105 | 0 | ocr-raster 3, pdf 14, docx 88 |  |
| `youtube` | `youtu\.?be` | added | 29 | 68 | 52 | 16 | text 68 | видео вне аудита по указанию оператора 16 |

Сверка с ориентирами issue (файлы без SVG): `cisco` 120 = 120, `netacad` 4 = 4, `networking academy` 16 = 16, `ccna` 88 = 88, `packet tracer` 87 = 87, `webex` 0 = 0, `catalyst` 27 = 27, `meraki` 3 = 3, `\.pka` 79 = 79. `\bIOS\b` даёт 57 текстовых файлов против 63 в issue: разница — бинарные файлы (`git grep` без `-I` даёт 76). В текстовых файлах ничего не потеряно, бинарные `.docx`/`.pdf` разобраны отдельно.

Пояснения к K:
- **синтаксис CLI** — по правилу issue. Ключевые слова команд и вывода в стиле IOS (`show etherchannel summary`, `spanning-tree portfast`, `Portfast Default is disabled`, `| begin span`) — синтаксис, который learn-netsim сохраняет. Названия протоколов (CDP, DTP, PAgP, HSRP…) внутри команд **не** исключены: при смене протокола (D4) эти строки меняются.
- **OCR-артефакты ©/®/™** — tesseract принимает круглые маркеры легенды, иконки портов и фавиконы вкладок за знаки. Каждый такой случай проверен глазами. Настоящие знаки в растрах есть только в 13.2.3-1 (© Cisco Systems) и 10.5.10 («Copyright (c) … Cisco Systems»), они в карте.
- **видео вне аудита** — попадания в `videos/*.md` (разборы роликов): по указанию оператора видео не входят в аудит, они уже классифицированы и будут пересобраны (D6).
- **ложные совпадения** — `ensa` в «Compensates», `c\d{4}` в шестнадцатеричном адресе `C80084AEF101`, `span` как имя переменной в `figma_sync.py`, `PT` в названии шрифта «PT Mono», ESA = Extended Service Area на рисунке 12.3.3-2.

**Не исключено, но по сути не вендор:** `youtube` — это не ссылки на вендора, а встраивания роликов NetAcad в README материалов. Они в карте как `link` с D6.

### Итоговый словарь

Из issue: `cisco`, `сиско`, `циско`, `netacad`, `networking academy`, `сетевая академия`, `академи`, `ccna`, `ccnp`, `ccent`, `itn`, `srwe`, `ensa`, `v7`, `packet tracer`, `PT`, `.pka`, `.pkt`, `webex`, `meraki`, `catalyst`, `ISR`, `nexus`, `ASA`, `anyconnect`, `dna center`, `IOS`, `IOS XE`, `NX-OS`, `models`, `WS-C`, `CDP`, `EIGRP`, `HSRP`, `GLBP`, `VTP`, `DTP`, `ISL`, `PVST`, `©`, `®`, `™`, `copyright`, `товарн`, `cisco.com`.

Добавлено по ходу работы: `linksys` (`linksys`), `talos` (`\btalos\b`), `scope and sequence` (`scope\s+and\s+sequence`), `ilm` (`\bilm\b`), `aironet` (`aironet`), `ESA/WSA` (`\bESA\b¦\bWSA\b¦email\s+security\s+appliance¦web\s+security\s+appliance`), `AMP` (`\bAMP\b`), `ISE` (`\bISE\b`), `Secure ACS` (`\bACS\b`), `RV130W` (`\bRV\s?\d{3}W?\b`), `MX64W` (`\bMX64W?\b`), `WRT300N` (`\bWRT\d+N?\b`), `models+` (`\b(1841¦2811¦2950¦3550¦3750¦3850¦4331¦3504¦1815)\b`), `ISR\d` (`\bISR\d{3,4}`), `c\d{4} (image/platform)` (`\bc\d{4}(?:[a-z0-9]*)`), `IOS image` (`universalk9¦lanbase¦ipbase`), `IOS version` (`\b1[0-7]\.\d\(\d+\)[A-Z]*\d*`), `PAgP` (`\bPAgP\b`), `CEF` (`\bCEF\b¦cisco\s+express\s+forwarding`), `LWAPP/LAP` (`\bLWAPP\b¦\bLAP\b`), `FlexConnect` (`flexconnect`), `EtherChannel` (`etherchannel`), `PortFast` (`portfast`), `BPDU Guard` (`bpdu\s?guard`), `Root/Loop Guard` (`root\s?guard¦loop\s?guard`), `UplinkFast/BackboneFast` (`uplinkfast¦backbonefast`), `SPAN/RSPAN` (`\bR?SPAN\b`), `UDLD` (`\bUDLD\b`), `TACACS+` (`tacacs`), `netacad.com` (`netacad\.com`), `youtube` (`youtu\.?be`).

Вне словаря, найдено глазами и внесено в карту:
- CDP в выноске рисунка 3.1.3;
- MAC HSRP `0000.0C07.AC01` на рисунке 9.2.2;
- вывод GLBP в 07-09-exam/9.png;
- маршрут EIGRP «D …» в final-exam/11.gif;
- `%CDP-4-…` в final-exam/2.png;
- логотипы на фото и в GUI.

Кандидаты на словарь следующих курсов: `Linksys`, `Aironet`, `AIR-AP`, `RV1\d\dW`, `MX\d\dW`, `WRT\d+N`, `CleanAir`, `0000\.0c07\.ac`, `0007\.b400`, `HomeRouter-PT`, `LAP-PT`, `CCNAv7`, `Ville\b`.

## 6. Таблица покрытия

| тип | всего в git | просмотрено | пропущено | как |
|---|---|---|---|---|
| `.tf` | 580 | 580 | 0 | словарь построчно (лабы — сводно, одна строка на лабу) |
| `.json` | 276 | 276 | 0 | словарь построчно; квизы — с номером вопроса |
| `.svg` | 206 | 206 | 0 | рендер `rsvg-convert -b white -w 1600` → OCR eng+rus → просмотр глазами (18 контакт-листов); встроенные `<image>` извлечены |
| `.png` | 170 | 170 | 0 | OCR eng+rus (мелкие ×2) + просмотр глазами (19 контакт-листов) |
| `.md` | 158 | 142 | 16 (`videos/` — по указанию оператора) | словарь построчно с контекстом: ограждённый код, HTML-комментарии |
| `.yaml` | 120 | 120 | 0 | словарь построчно |
| `.sh` | 120 | 120 | 0 | словарь построчно |
| `.docx` | 44 | 44 | 0 | текст тела, таблиц и колонтитулов (python-docx) + словарь; картинки колонтитулов просмотрены |
| `.pka` | 40 | 40 как файлы | содержимое 40 | не открывались (зашифрованный формат PT); покрыты строкой лабы и именем файла |
| `.tpl` | 40 | 40 | 0 | словарь построчно |
| `.jpg` | 24 | 24 | 0 | OCR + просмотр |
| `.jpeg` | 19 | 19 | 0 | OCR + просмотр |
| `.gif` | 12 | 12 | 0 | 1-й кадр (все GIF однокадровые) → OCR + просмотр |
| `.py` | 2 | 2 | 0 | словарь построчно |
| `.pdf` | 2 | 2 | 0 | `pdftotext` + словарь; список картинок `pdfimages` |
| `.yml` | 1 | 1 | 0 | словарь построчно |
| `.gitignore` | 1 | 1 | 0 | словарь построчно |
| `.txt` | 1 | 1 | 0 | словарь построчно |

Итого `git ls-files` = 1816 (без каталога `audit/` — это сам аудит). Не просмотрено содержимое 40 `.pka`: формат зашифрован. Они покрыты строками лаб и строками имён файлов, внутренние строки PT-топологий (имена хостов, пароли, URL серверов) видны по README и скриншотам `topology.png`.

Ассеты `figma-assets.json`:

| kind | в манифесте | просмотрено | как | не просмотрено |
|---|---|---|---|---|
| illustration | 197 | 187 | рендер + OCR + глазами (185 synced + 2 orphan, лежащих в git) | 10 orphan без файла в git (6.3.3, 10.1.2-1…-3, 14.3.3, 14.3.4, 15.2.3, 15.2.7, 15.3.2, 15.4.3): Figma недоступна. По `notes` манифеста это дубли просмотренных рисунков и три одиночные иконки |
| animation | 18 | 18 | 5 кадров каждой (SMIL, Chromium: `pauseAnimations` + `setCurrentTime` на 12/32/52/72/92 %) + OCR + тексты узлов из `animations/*/spec.json` | — |
| native | 73 | 73 | OCR + глазами, сверка с `design/raster-inventory-ccna2.md` | — |
| вне манифеста: SVG | 1 | 1 | `16.01.02-…-quiz/assets/16.1.2.svg` | — |
| вне манифеста: растры | 152 | 152 | экзамены 82, `topology.png` лаб 39, `readme-assets` 17, квизы и фото 14 | — |

| прочее | всего | просмотрено | как |
|---|---|---|---|
| видео (документы `videos/`) | 16 | 0 | пропущены по указанию оператора: уже классифицированы и будут пересобраны; попадания словаря — в журнале как исключённые |
| встроенные растры в SVG | 5 | 5 | 3 текстуры (в ~180 SVG), рентген 12.1.5, череп 12.6.5 — вендора нет |
| лист `_Библиотека` (Figma) | 1 | 0 | напрямую не открыт; вывод D7 — по иконкам в 206 экспортах |
| листы Figma «Видео · …» | ? | 0 | не проверены: Figma недоступна |

## 7. Ограничения и что осталось сделать

1. **Figma.** Не прочитаны `characters` узлов `TEXT` и имена инстансов. Нет токена, Figma MCP получил 403 от прокси сессии. Вместо этого — OCR и просмотр рендеров. Мелкий текст OCR может пропустить: так CDP в 3.1.3 нашёлся только глазами. **Рекомендация:** перед правками одним проходом `GET /v1/files/3FtCg22qFubpLBPOetQU03/nodes?ids=…` по 197 иллюстрациям собрать `characters` и сверить с разделом `surface=illustration`. Заодно открыть `_Библиотека` (D7) и листы «Видео · …».
2. **Имя узла Figma** в `locator` для иллюстраций не указано: есть `key` и `nodeId` из манифеста, имя узла без API не получить.
3. **`.pka` не открывались.** Значения внутри топологий PT (пароли, URL `www.cisco.pka`, имена `Cisco*`) видны только там, где они попали в README или в `topology.png`.
4. **Ветка и PR.** По инструкции сессии файлы лежат в ветке `claude/issue-21-analysis-ocqub8`, а не в `audit/vendor-mentions`. PR не открыт: оператор попросил результат комментарием. Если нужна PR — открыть её из этой ветки, она меняет только `audit/`.
5. **Хаб.** Сигналы «взял / PR открыт» в хаб не отправлены: доступа к хабу из этой сессии нет.

## 8. Замечено попутно (в материалах не правилось)

- `final-lab-part2/learn-metadata.json:3` — `shortName: "srwe-f1"`, совпадает с part1, должно быть `srwe-f2` (дефект).
- `learn-metadata.json:2` и `migration-instructions.md:2` — «**Ведение** в коммутацию…» → «Введение».
- `migration-instructions.md:278` — «Packet **Trcer**».
- `09-fhrp-concepts/09.03.03-lab-hsrp-configuration-guide/learn-metadata.json:5` — «отрабока».
- `03-vlans/03.04-vlan-trunks/README.md:20` — «На **риунке**»; `09-fhrp-concepts/09.03.04-…/README.md:118` — «на **торой** интерфейс»; `13-wlan-configuration/13.05.02-…/README.md:112` — «назначте».
- Каталог `08-slaac-and-dhcpv6-concepts/08.01-ipv6-global-unicast-address-**assigment**` (assignment).
- `readme-assets/video.png` — в кадре адрес электронной почты; `readme-assets/pt-menu.png` — локальный путь с именем пользователя.

## 9. Метод (для повторения на CCNA1/CCNA3)

Скрипты — `audit/tools/` (план снят; открытые пункты — kb#291). Шаги:

1. `git ls-files` → словарь по текстовым файлам построчно. Контекст строки: ограждённый код, HTML-комментарий, номер вопроса квиза, `answerSchema` лабы. Попадания в именах файлов и каталогов — отдельно.
2. Классификация: соседние попадания сливаются в фразу, фраза получает категорию по приоритету legal > link > cli-vendor-string > model > proprietary-tech > product > brand > certification > lab-infra. «cisco»/«ccna» в значении конфигурации (пароль, домен, хост) отделяются по токену (D11).
3. Картинки: рендер SVG → OCR; кадры анимаций → OCR; растры → OCR. Всё просмотрено глазами по контакт-листам. Встроенные растры извлечены и дедуплицированы по sha256.
4. `.docx`/`.pdf` → текст, включая колонтитулы, → словарь; картинки колонтитулов просмотрены.
5. Журнал попаданий → строка карты или исключение с причиной → N = M + K по каждому термину.

