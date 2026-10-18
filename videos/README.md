# Встроенные видео курса CCNA 2 (SRWE) — классификация и сценарии для пересборки

В курсе встроено 15 видео YouTube (все — перезаливки роликов Cisco Networking Academy на канале оператора). Для каждого сделан документ: факты, цель для обучающегося, посценный сценарий (что на экране / что сказано / роль), предложение по пересборке (формат, сцены для генератора, ассеты, сессия для симулятора) и полный транскрипт. Язык документов — русский, команды и вывод — дословно.

Классы: `marketing` (реклама академии/продукта — убрать) · `explainer` (концепция на слайдах/схемах) · `cli-basics` (основы IOS CLI) · `lab-demo` (сквозная демонстрация в GUI / на реальном устройстве) · `other`.

## Видеоряд в Figma

Колонка «Видеоряд (Figma)» в таблице фиксирует прогресс пересборки: по каким видео собран новый видеоряд — анимация Figma Motion на нашей дизайн-системе, тем же методом, что в CCNA1. Голосовая дорожка — отдельный трек, пока не начат ни для одного видео.

**Готово: 5 из 15** (explainer — 5 из 8). Три explainer-ролика об атаках (`ye_f86EfTl8`, `JhiaFeH9ZOU`, `RhcFm7fBVH0`) в цепочку пересборки 2026-10-18 не вошли — решение по ним за оператором.

| статус | значит |
|---|---|
| — | пересборка не начата |
| Motion | анимация собрана и ждёт приёмки оператора; время — её хронометраж, ссылка ведёт на кадр анимации |
| **готов** | анимация Figma Motion принята оператором; время — её хронометраж (у оригинала — колонка «Длит.»), ссылка ведёт на кадр анимации |

Всё лежит в рабочем файле Figma `3FtCg22qFubpLBPOetQU03` (CCNA Design): по листу на видео «Видео · ‹videoId› · ‹название› · прототип» после листа своего модуля, с секциями «Motion · …» (анимация и набор-кит, из которого она собрана) и «Раскадровка · …» (базовая сцена и кадры раскадровки с описаниями). У этих листов нет курсового префикса и штампов `⟨id⟩`, поэтому синхронизация иллюстраций (`figma_sync.py`) их не читает. Метод сборки — `runbooks/video-motion-build.md` в learn-knowledge-base. Каждая анимация — самостоятельный explainer: титул задаёт вопрос, на который она отвечает, без отсылок к тексту лекции; примеры — из текста темы. Подробности по каждому видео — раздел «Видеоряд в Figma» в его документе.

`fi7Ss-_9LvY` встроен и в CCNA1 (7.3.4) — там тот же видеоряд, принятый оператором.

## Индекс

| videoId | Модуль / тема | Название | Длит. | Класс | Пересборка | Видеоряд (Figma) | Документ |
|---|---|---|---|---|---|---|---|
| `fi7Ss-_9LvY` | 02-switching-concepts / 02.01-frame-forwarding | Таблицы MAC-адресов на соединённых коммутаторах | 3:05 | explainer | анимация Figma ≤ 60 с (+ опц. озвученный ~2:30) | **готов** · 1:35 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=4933-8671) | [02.01--fi7Ss-_9LvY](02-switching-concepts/02.01-frame-forwarding--fi7Ss-_9LvY.md) |
| `TZrrTw5uhNI` | 05-stp / 05.01-purpose-of-stp | Наблюдение за работой STP | 6:18 | lab-demo | видео с голосом (код-рендер) ~4:30; часть 1 — анимация Figma | — | [05.01--TZrrTw5uhNI](05-stp/05.01-purpose-of-stp--TZrrTw5uhNI.md) |
| `ye_f86EfTl8` | 10-lan-security-concepts / 10.05-lan-attacks | Атаки на VLAN и DHCP | 5:41 | explainer | текст + иллюстрация; 2 анимации Figma ≤ 60 с (double-tagging, DHCP spoofing) | — | [10.05--ye_f86EfTl8](10-lan-security-concepts/10.05-lan-attacks--ye_f86EfTl8.md) |
| `JhiaFeH9ZOU` | 10-lan-security-concepts / 10.05-lan-attacks | ARP-атаки, STP-атаки, CDP-разведка | 6:14 | explainer | текст + иллюстрация; 2 анимации Figma ≤ 60 с (ARP poisoning, STP root) | — | [10.05--JhiaFeH9ZOU](10-lan-security-concepts/10.05-lan-attacks--JhiaFeH9ZOU.md) |
| `3bOfIlu0BzI` | 12-wlan-concepts / 12.02-components-of-wlans | Компоненты WLAN | 6:12 | explainer (ведущий с железом) | текст + иллюстрация (опц. Figma ≤ 45 с) | **готов** · 1:26 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5145-8215) | [12.02--3bOfIlu0BzI](12-wlan-concepts/12.02-components-of-wlans--3bOfIlu0BzI.md) |
| `XI_F7TvuDBs` | 12-wlan-concepts / 12.03-wlan-operation | Принципы работы WLAN | 11:50 | explainer (слайды) | текст + иллюстрация; опц. 2 анимации Figma ≤ 45 с (CSMA/CA, обнаружение) | **готов** · 2:12 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5158-9679) | [12.03--XI_F7TvuDBs](12-wlan-concepts/12.03-wlan-operation--XI_F7TvuDBs.md) |
| `qXXGwkLZ6hI` | 12-wlan-concepts / 12.04-capwap-operation | CAPWAP | 3:45 | explainer (слайды) | текст + иллюстрация (опц. Figma ≤ 45 с) | **готов** · 1:40 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5166-7871) | [12.04--qXXGwkLZ6hI](12-wlan-concepts/12.04-capwap-operation--qXXGwkLZ6hI.md) |
| `RhcFm7fBVH0` | 12-wlan-concepts / 12.06-wlan-threats | Угрозы безопасности WLAN | 5:41 | explainer (слайды) | текст + иллюстрация (опц. Figma «evil twin» ≤ 45 с) | — | [12.06--RhcFm7fBVH0](12-wlan-concepts/12.06-wlan-threats--RhcFm7fBVH0.md) |
| `Pl3u95xY2RQ` | 12-wlan-concepts / 12.07-secure-wlans | Защита беспроводных сетей | 7:09 | explainer | текст + иллюстрация (опц. Figma ≤ 45 с); поля GUI — в макет симулятора | **готов** · 1:56 · [Figma](https://www.figma.com/design/3FtCg22qFubpLBPOetQU03/CCNA-Design?node-id=5173-8272) | [12.07--Pl3u95xY2RQ](12-wlan-concepts/12.07-secure-wlans--Pl3u95xY2RQ.md) |
| `dzWPJ4Q57cg` | 13-wlan-configuration / 13.01-remote-site-wlan-configuration | Настройка домашнего роутера (Cisco RV130W) | 9:12 | lab-demo | видео с голосом (код-рендер) ~5:00; GUI-упражнение симулятора | — | [13.01--dzWPJ4Q57cg](13-wlan-configuration/13.01-remote-site-wlan-configuration--dzWPJ4Q57cg.md) |
| `O-KpLNWHQhA` | 13-wlan-configuration / 13.02-configure-a-basic-wlc-on-the-wlc | Базовая WLAN на WLC 3504 | 7:14 | lab-demo | видео с голосом (код-рендер) ~4:30; GUI-упражнение симулятора | — | [13.02--O-KpLNWHQhA](13-wlan-configuration/13.02-configure-a-basic-wlc-on-the-wlc--O-KpLNWHQhA.md) |
| `0f4OhO7N1mg` | 13-wlan-configuration / 13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc | SNMP и RADIUS на WLC | 5:36 | lab-demo | видео с голосом (код-рендер) ~3:00 (серия 13.3) | — | [13.03--0f4OhO7N1mg](13-wlan-configuration/13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc--0f4OhO7N1mg.md) |
| `DinzgbcB-So` | 13-wlan-configuration / 13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc | VLAN-интерфейс для новой WLAN | 5:05 | lab-demo | видео с голосом (код-рендер) ~3:00 (серия 13.3) | — | [13.03--DinzgbcB-So](13-wlan-configuration/13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc--DinzgbcB-So.md) |
| `j9nrRvV3JKo` | 13-wlan-configuration / 13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc | Область DHCP на WLC | 3:35 | lab-demo | видео с голосом (код-рендер) ~2:00 (серия 13.3) | — | [13.03--j9nrRvV3JKo](13-wlan-configuration/13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc--j9nrRvV3JKo.md) |
| `PF8gfBfJN8M` | 13-wlan-configuration / 13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc | WLAN с WPA2 Enterprise (+ `test aaa radius`) | 5:24 | lab-demo | видео с голосом (код-рендер) ~4:00 (серия 13.3); GUI + CLI симулятора | — | [13.03--PF8gfBfJN8M](13-wlan-configuration/13.03-configure-a-wpa2-enterprise-wlan-on-the-wlc--PF8gfBfJN8M.md) |

Ни одно видео не встроено в README лабораторной работы (путей с `-lab-` нет).

## Итоги

**По классам:** explainer — 8, lab-demo — 7, marketing — 0, cli-basics — 0, other — 0. Маркетинговых роликов в курсе нет: все 15 — учебные видео NetAcad. Убирать «как маркетинг» нечего; но восемь explainer-роликов дублируют текст темы (у шести из них слайды — те же рисунки, что уже лежат в `assets/`), поэтому для них предлагается **не** пересобирать видео, а оставить текст + иллюстрации и при желании добавить короткие анимации Figma только там, где важна динамика (double-tagging, DHCP spoofing, ARP poisoning, STP root attack, CSMA/CA, evil twin). Единственный explainer, который стоит превратить в полноценную анимацию, — `fi7Ss-_9LvY` (MAC-таблицы на двух коммутаторах): это чисто анимационный сюжет без дублирования в тексте.

**Самые ценные для симулятора (по убыванию):**

1. `TZrrTw5uhNI` — STP на трёх реальных Catalyst: `show spanning-tree vlan 1` до/после обрыва канала, переход Altn/BLK → Root/LRN → Root/FWD, syslog падения интерфейса, telnet на корневой мост, ping с ПК. Полностью воспроизводимая CLI-сессия для симулятора коммутаторов (блок в документе).
2. `PF8gfBfJN8M` — WLC: GUI-сценарий WPA2 Enterprise **и** CLI-проверка `show aaa auth` / `test aaa radius username … wlan-id 2` / `test aaa show radius` с детерминированным выводом.
3. `O-KpLNWHQhA` + `0f4OhO7N1mg` + `DinzgbcB-So` + `j9nrRvV3JKo` — единая серия на одной топологии (R1 / S1 / WLC 3504 / AP1 / PC-A RADIUS-SNMP / PC-B), покрывающая весь GUI контроллера: WLAN, интерфейсы, DHCP scope, SNMP trap receiver, RADIUS. В каждом документе — блок «путь › поле = значение» для будущего GUI-симулятора WLC; рекомендуется делать как один связный ролик ~10–12 мин.
4. `dzWPJ4Q57cg` — домашний роутер Cisco RV130W «из коробки»: кабели, вход, принудительная смена пароля, WAN/LAN/DHCP/DNS, Wireless (режим, канал, SSID, лимит клиентов), WPA2-Personal/AES, подключение клиента Windows. Прототип GUI-упражнения «SOHO-роутер».
5. `ye_f86EfTl8` / `JhiaFeH9ZOU` — дают команды для упражнений «закрыть порты» (`switchport mode access`, `no cdp run` / `no cdp enable`, `no lldp run` / `no lldp transmit` / `no lldp receive`), но сами по себе CLI-сессий не содержат.

**Качество исходных данных:** у двух загрузок видеодорожка неполная — `0f4OhO7N1mg` (видео обрывается на 4:00 из 5:36) и `PF8gfBfJN8M` (30 с ключевых экранов без тайминга на 5:24 звука); сцены восстановлены по транскрипту и по скриншотам тех же экранов в `assets/13.3.4-*.jpg` и `assets/13.3.11-*.png` — в документах это отмечено. У `XI_F7TvuDBs` детектор сцен нашёл только 8 кадров на 11:50 — слайды сняты вручную с шагом 20 с. Субтитры есть у всех видео (авто-сгенерированные en; у `3bOfIlu0BzI` дополнительно ru).

**Фактические неточности в оригиналах, которые стоит исправить при пересборке:** CAPWAP назван «стандартом IEEE» (на самом деле IETF, RFC 5415) — и в видео, и в тексте 12.4.2; в `dzWPJ4Q57cg` диктор говорит «LAN port» про WAN-порт; в `XI_F7TvuDBs` RTS расшифрован как «ready to send» (request to send); на слайде `JhiaFeH9ZOU` ARP-кэш R1 подписан «PC2 ARP Cache».
