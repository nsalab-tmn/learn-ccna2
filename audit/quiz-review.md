# CCNA2 quiz and exam review (kb#275)

> **Status:** review done on 2026-10-18 at `origin/main` `7a5dcf0`, after all CCNA2 de-marketing and accuracy PRs were merged. Fixes are in the PRs listed below. Doubtful items wait for the operator on kb#275.

## What

A question-by-question review of every CCNA2 quiz and exam, and of the CCNA2 bank in learn-ccna1 `__exams/CCNA2`:

| Set | Files | Questions |
|---|---|---|
| module quizzes (`NN-module/*quiz*/`) | 52 | 380 |
| module and final exams (`*-exam/`, `final-exam/`) | 6 | 343 |
| bank copies (learn-ccna1 `__exams/CCNA2/*_Exam/`) | 6 | 386 |

The CCNA1 review is in learn-ccna1 `audit/quiz-review.md`; CCNA3 follows. Labs and `.pka` files are out of scope (kb#271).

## Why

The quizzes and exams are translations of the vendor's question banks. The de-marketing passes (kb#273) changed vendor names but did not check whether the questions are right. This review checks each question for:
1. **Correctness:** the key is right by the course text and the standards (RFC, IEEE). Every distractor is wrong, and the number of correct answers matches the stem.
2. **Course match:** the question can be answered from its module or an earlier one, in the module's terms.
3. **Language:** natural literary Russian, without machine-translation artefacts or English left in prose.
4. **Vendor and Packet Tracer leftovers** that the de-marketing missed.
5. **References:** images exist, and comments match the key.

## How

1. **Mechanical pass** over all files: answer counts against `answerType` and the stem, matching keys, image paths, Packet Tracer UI strings. In CCNA2 it found, all in the bank: two image paths with the wrong case (01-04 Q25, Q45), a matching key with no option (Practice Final Q44), two wrong `answerType` values (Practice Final Q45, Q47) and five `.pka` questions.
2. **Review:** six reviewers each took a block of modules or exams and wrote findings with evidence (`README.md:line`, RFC or IEEE) and a proposed minimal fix. The CCNA1 lessons went into their brief: check every claim of a rewritten comment, keep bank twins word for word, and don't swap «роутер» / «хост».
3. **Verification:** every finding was checked again before it went into a PR. The coordinator checked the quiz findings. Four second reviewers checked the exam findings, confirmed every key change on their own, and rewrote fixes where needed; the coordinator then read every error-severity fix. Fixes were checked against the glossary (`conventions/ru-glossary.md` in the knowledge base, with the rows decided in kb#279).
4. **Fix PRs:** one per module block, so no two open PRs share a line. The bank copies live in learn-ccna1, so each exam block has a paired PR there with the same wording.
5. **Doubtful items** are not changed. They go to the operator on kb#275: two defensible answers, content the course does not teach, a structural fix to the JSON, or a course text that is itself wrong.

Severity follows kb#275:
- `error`: a wrong key, a distractor that is actually right, a wrong statement in a question or comment, or a comment copied from another question;
- `style`: language, terms, typos, English or Cyrillic/Latin mix-ups;
- `unclear`: an ambiguous stem or two defensible answers.

## JSON structure (recorded, unchanged)

No PR changes keys, key order, the number of questions or answers, image paths or HTML comments. The one value change outside text is `answerType` in bank Practice Final Q45 and Q47, which now matches their number of correct answers.

- **Top level:** quizzes have `title`, `materialType`, `description`, `difficulty`, `duration`, `tags`, `skills`, `passingScore`, `assets`, `questions`. The exams have the same keys in another order, and the bank copies carry `assetsPath` instead of `assets`.
- **Question:** `question` (string, Markdown; an image as `![](./assets/x.png)`), `answerType` and `answers`. A `matching` question also has `options`.
  - `singleChoice`: 924 questions.
  - `multiChoice`: 145 questions; the stem says how many answers are right («верны два варианта»).
  - `matching`: 40 questions.
- **Answer:** `answer` (string) and `correct` (bool). Answers of a `matching` question carry `match` instead of `correct`. An optional `comment` is shown after a wrong answer, and by convention the same comment sits on every wrong answer of a question.

## Fix PRs

| PR | Scope |
|---|---|
| learn-ccna2#45 | quizzes, modules 01–04 |
| learn-ccna2#46 | quizzes, modules 05–09 |
| learn-ccna2#47 | quizzes, modules 10–13 |
| learn-ccna2#48 | quizzes, modules 14–16 |
| learn-ccna2#49 and learn-ccna1#120 | exams 01–04, 05–06, 07–09 and their bank copies |
| learn-ccna2#50 and learn-ccna1#121 | exams 10–13, 14–16, final and their bank copies (key changes: bank 14-16 Q55, bank Practice Final Q46, Q49–Q52, Q54) |

## Totals

Findings are counted per file. A bank copy's finding counts separately from its connected exam's, and a comment copied onto three wrong answers is one finding.

| | quizzes | exams | bank copies | all |
|---|---|---|---|---|
| error | 25 | 25 | 43 | 93 |
| style | 215 | 134 | 180 | 529 |
| unclear | 13 | 8 | 19 | 40 |
| **fixed** | 240 | 158 | 218 | 616 |
| **to the operator** | 13 | 9 | 24 | 46 |
| **rejected on verification** | 0 | 0 | 0 | 0 |
| **total findings** | 253 | 167 | 242 | 662 |

The fix PRs are listed in *Fix PRs* above. Doubtful items are listed again, with their reasons, in the kb#275 comment for the operator.


## Findings: Quizzes

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| 01.05.11-verify-directly-connected-networks-quiz | 1 | style | Comment names 'show ip route', but the option offered is 'show ipv6 route'. | #45 → «show ipv6 route и show running-config interface не предоставляют эту информацию» |
| 01.05.11-verify-directly-connected-networks-quiz | 2 | style | Broken MT construction: «для идентификации напрямую подключенных» has no noun, and the clause order is garbled. | #45 → «Каким кодом в таблице маршрутизации обозначаются напрямую подключенные маршруты?» |
| 01.05.11-verify-directly-connected-networks-quiz | 2 | style | MT artefact: «RIP означает протокол маршрутизации, который является одним из первых протоколов маршрутизации» (calque of 'RIP stands for ...', tautological). | #45 → «RIP (Routing Information Protocol) — один из первых протоколов маршрутизации» |
| 01.05.11-verify-directly-connected-networks-quiz | 3 | style | Mistranslation: «количество потоков пакетов» means 'number of packet flows'; the lecture says 'packet-flow counters'. | #45 → «счетчики потока пакетов» |
| 01.05.11-verify-directly-connected-networks-quiz | 5 | style | Leftover English in an answer option: «pipe \|». | #45 → «"answer": "вертикальная черта \\|"» |
| 01.05.11-verify-directly-connected-networks-quiz | 5 | style | Leftover English in an answer option: «comma ,». | #45 → «"answer": "запятая ,"» |
| 01.05.11-verify-directly-connected-networks-quiz | 5 | style | Leftover English in an answer option: «colon :». | #45 → «"answer": "двоеточие :"» |
| 01.05.11-verify-directly-connected-networks-quiz | 5 | style | Leftover English in an answer option: «semi colon ;». | #45 → «"answer": "точка с запятой ;"» |
| 01.05.11-verify-directly-connected-networks-quiz | 6 | style | Punctuation error: the conjunction «в то время как» is split by a comma («В то время, как»). | #45 → «Хотя все три выражения» |
| 01.06.04-quiz | 2 | style | MT artefact: «инструкция» for 'statement'. | #45 → «Какое утверждение описывает работу светодиода System» |
| 01.06.04-quiz | 2 | error | Key says the LED is blinking amber; the lecture and the question's own comment say steady amber. Distractor 1 also uses 'blinking amber' (for POST), so two opti… | #45 → «если светодиод горит желтым, система получает питание, но работает с перебоями» |
| 01.06.04-quiz | 2 | error | Distractor 'green = system operating normally' is true: the comment on this very question states it, and so does the switch documentation. Also an agreement err… | #45 → «если светодиод не горит, система работает нормально» |
| 01.06.04-quiz | 4 | style | Plural stem («Каковы преимущества») on a singleChoice question with one correct answer. | #45 → «Каково преимущество SSH по сравнению с Telnet?» |
| 01.06.04-quiz | 5 | style | Case error «настроил ... IP-адресом и маску» (instrumental instead of accusative); «ё» against the course convention. | #45 → «настроил для нее IP-адрес и маску подсети» |
| 01.06.04-quiz | 8 | unclear | The router boot sequence (and 'setup mode', «режим настройки») is not taught in the course; module 1 covers only the switch boot sequence, which the comment cit… | operator (kb#275) |
| 01.06.04-quiz | 11 | style | Punctuation error: comma after the introductory prepositional phrase before the question word. | #45 → «При настройке коммутатора для доступа SSH какую команду» |
| 02.02.04-switching-domains-quiz | 1 | style | Broken construction: «между узлом ..., подключенным к коммутатору ...» names only one party after «между». | #45 → «Какая скорость будет автоматически согласована между узлом с NIC 1 Гбит/с и портом коммутатора 100 Мбит/с?» |
| 02.02.04-switching-domains-quiz | 1 | style | Calque «согласовываться на более медленную скорость»; the comment calls the device «Хост» while the stem calls it «узел». | #45 → «Узел и коммутатор автоматически согласуют меньшую из двух скоростей — 100 Мбит/с» |
| 02.02.04-switching-domains-quiz | 2 | style | Agreement error: singular «отделяет домен» is followed by plural «их не разделяют»; «отделяет» is also the wrong verb (the router separates domains from each ot… | #45 → «разделяет домены широковещательной рассылки. Точки» |
| 02.03.02-quiz | 2 | style | Wrong antecedent: «ищет в нем номер порта» says the switch looks up the port number inside the MAC address; it looks it up in the table. | #45 → «ищет в таблице номер порта» |
| 02.03.02-quiz | 3 | style | MT artefact: «Какова значительная разница» (calque of 'What is a significant difference'). | #45 → «В чем существенное различие между концентратором» |
| 02.03.02-quiz | 7 | style | Garbled MT: «Один коммутатор доступа в стойку» (from 'a single rack-unit access switch'). | #45 → «Коммутатор доступа высотой в одну монтажную единицу (1U) может иметь до 48 портов» |
| 02.03.02-quiz | 11 | style | MT artefact: «Какой параметр» for 'Which statement'; the options are statements. | #45 → «Какое утверждение правильно описывает метод коммутации?» |
| 03.01.05-overview-of-vlans-quiz | 1 | style | Punctuation: the participial phrase «разделяя ... сети» is not opened by a comma after «что». | #45 → «Верно ли утверждение, что, разделяя крупные» |
| 03.01.05-overview-of-vlans-quiz | 3 | style | Leftover English answer label «default VLAN». | #45 → «"answer": "VLAN по умолчанию"» |
| 03.01.05-overview-of-vlans-quiz | 3 | style | English-only answer label «native VLAN»; the lecture gives the Russian term with the English one in brackets. | #45 → «"answer": "собственная VLAN (native VLAN)"» |
| 03.01.05-overview-of-vlans-quiz | 3 | style | Answer label «данные» is not a VLAN type name; the lecture calls it «VLAN данных». | #45 → «"answer": "VLAN данных"» |
| 03.02.09-vlans-in-a-multi-switched-environment-quiz | 1 | style | Typo «сформированое» (double н required). | #45 → «PC1 и PC4 находятся в одной и той же VLAN 10, а широковещательное сообщение, сформированное» |
| 03.02.09-vlans-in-a-multi-switched-environment-quiz | 2 | style | Agreement error «компьютерами, принимающий» and typo «сформированое». | #45 → «единственными компьютерами, принимающими широковещательную рассылку от PC2. Это связано с тем, что PC3, PC4 и PC6 находя…» |
| 03.02.09-vlans-in-a-multi-switched-environment-quiz | 3 | style | Typo «сформированое» (double н required). | #45 → «PC3 и PC5 находятся в одной и той же VLAN 10, а широковещательное сообщение, сформированное» |
| 03.06.04-quiz | 4 | style | Mistranslation: the file does not 'manage' the VLAN database, it holds it (the comment says «содержит»). | #45 → «"answer": "содержит базу данных VLAN"» |
| 03.06.04-quiz | 5 | style | Word order typo «от данных VLAN» ('from the VLAN data') instead of «от VLAN данных». | #45 → «поэтому должна отличаться от VLAN данных» |
| 03.06.04-quiz | 6 | style | Negation calque «не пересылаются в любую другую VLAN» (Russian requires «ни в какую другую»). | #45 → «не пересылаются ни в какую другую VLAN» |
| 03.06.04-quiz | 7 | style | Typo «адаптором». | #45 → «сетевым адаптером» |
| 03.06.04-quiz | 8 | error | Count mismatch: the stem says three correct answers, but only two of the four options are correct and marked (cost reduction, security). | #45 → «(верны два варианта)» |
| 03.06.04-quiz | 11 | style | Replacement artefact «на native VLAN (Native VLAN)»: the Russian term was overwritten by the English one, leaving it doubled. | #45 → «на собственной VLAN (Native VLAN)» |
| 03.06.04-quiz | 12 | error | Distractor «изучить согласование DTP» is defensible as correct: the module's own labs use show interface(s) trunk to confirm what DTP negotiated. The English or… | #45 → «"answer": "для наблюдения за согласованием DTP в реальном времени"» |
| 03.06.04-quiz | 12 | style | Typo «на канал.»; the same comment on the other wrong answers reads «на канале». | #45 → «разрешенные VLAN на канале» |
| 03.06.04-quiz | 14 | style | Mistranslation «встроенной VLAN» for native VLAN ('built-in VLAN'). | #45 → «должен быть тегирован в собственной VLAN» |
| 04.01.05-inter-vlan-routing-operation-quiz | 1 | style | Clumsy/ungrammatical lead-in «Посмотрите каждую из топологий сценария» (singular «сценария» for three scenarios). | #45 → «Рассмотрите топологии трех сценариев. **Сценарий А**» |
| 04.01.05-inter-vlan-routing-operation-quiz | 1 | style | Truncated name «router-on-stick»; the course and the operator decision use «router-on-a-stick». | #45 → «решения маршрутизации между VLAN с использованием router-on-a-stick» |
| 04.01.05-inter-vlan-routing-operation-quiz | 1 | style | Number error «Сценарии C — это решение» (plural noun, one scenario) and truncated «router-on-stick». | #45 → «Сценарий C — это решение маршрутизации между VLAN с использованием router-on-a-stick» |
| 04.01.05-inter-vlan-routing-operation-quiz | 1 | style | Same number error «Сценарии C» and truncated «Router-on-stick» in the full explanation. | #45 → «Сценарий C — это решение маршрутизации между VLAN с использованием router-on-a-stick» |
| 04.01.05-inter-vlan-routing-operation-quiz | 1 | style | Wrong answers 2 and 3 carry a truncated comment that only restates scenario A and does not say why B and C are misclassified; answer 1 has the full explanation.… | #45 comments rewritten: «Сценарий А — это решение для маршрутизации между VLAN уровня 3. Сценарий В — это устаревшее решение маршрутизации между …» |
| 04.04.07-troubleshoot-inter-vlan-routing-quiz | 1 | style | Calque «проблему между VLAN» ('inter-VLAN issue'): a problem 'between VLANs' instead of an inter-VLAN routing problem. | #45 → «Вы устраняете проблему маршрутизации между VLAN на роутере.» |
| 04.04.07-troubleshoot-inter-vlan-routing-quiz | 2 | style | Calque «проблему между VLAN» ('inter-VLAN issue'): a problem 'between VLANs' instead of an inter-VLAN routing problem. | #45 → «Вы устраняете проблему маршрутизации между VLAN на коммутаторе. Необходимо проверить список» |
| 04.04.07-troubleshoot-inter-vlan-routing-quiz | 3 | style | Calque «проблему между VLAN» ('inter-VLAN issue'): a problem 'between VLANs' instead of an inter-VLAN routing problem. | #45 → «Вы устраняете проблему маршрутизации между VLAN на коммутаторе. Необходимо проверить состояние» |
| 04.04.07-troubleshoot-inter-vlan-routing-quiz | 4 | style | Calque «проблему между VLAN» ('inter-VLAN issue'): a problem 'between VLANs' instead of an inter-VLAN routing problem. | #45 → «Вы устраняете проблему маршрутизации между сетями VLAN на роутере» |
| 04.04.07-troubleshoot-inter-vlan-routing-quiz | 4 | style | Comment names the command «show ip interfaces brief», which differs from the key «show ip interface brief». | #45 → «Команда show ip interface brief» |
| 04.05.04-quiz | 2 | error | Factually wrong comment: it says Layer 2 switches can do static routing; the course says a Layer 2 switch does not route. | #45 → «Коммутаторы уровня 2 не выполняют маршрутизацию, поэтому статические маршруты на них не обеспечат связь между VLAN» |
| 04.05.04-quiz | 2 | style | Word-order MT artefact «каждого интерфейса физического маршрутизатора» ('each interface of the physical router'). | #45 → «подключение каждого физического интерфейса маршрутизатора» |
| 04.05.04-quiz | 4 | style | Typo «подключеным». | #45 → «подключенным к SVI» |
| 04.05.04-quiz | 6 | style | Broken comment: typo «многуровневого», a verbless fragment «Если количество VLAN равно количеству портов на роутере.», and a garbled last sentence; the legacy o… | #45 → «При использовании многоуровневого коммутатора создается несколько SVI. При устаревшем методе каждой VLAN нужен отдельный…» |
| 04.05.04-quiz | 8 | style | Vendor leftover: ISL (Cisco-proprietary Inter-Switch Link) is not taught anywhere in the course; the module uses only IEEE 802.1Q. | #45 → «(IEEE 802.1Q)» |
| 04.05.04-quiz | 10 | style | MT artefact: «Другие параметры» for 'the other options' (answer choices). | #45 → «Другие варианты не описывают назначение этой команды» |
| 04.05.04-quiz | 15 | error | Wrong key: show ip interface does not display the 802.1Q VLAN ID of a subinterface; the course uses show interfaces (and show running-config) to find a wrong VL… | #45 → «"answer": "show interfaces"» |
| 04.05.04-quiz | 15 | error | Comment repeats the wrong command (show ip interface); align it with the corrected key. | #45 → «Команды show interfaces и show running-config» |
| 04.05.04-quiz | 15 | style | Case error «полезную информации». | #45 → «не выводит полезной информации» |
| 05.02.12-stp-operations-quiz | 1 | style | MT word order: comma between the introductory adverbial and the question word ("По умолчанию (...), что будет определять"). | #46 → «Что по умолчанию (без какой-либо конфигурации на коммутаторе) будет определять,» |
| 05.02.12-stp-operations-quiz | 1 | unclear | Distractor "идентификатор моста" is arguably correct: the root bridge is always the switch with the lowest BID; with default priorities the MAC address only bre… | operator (kb#275) |
| 05.02.12-stp-operations-quiz | 2 | error | Key says "lowest root bridge ID" (Root ID, the BID of the current root carried in BPDUs, which converges to the same value on every switch); the criterion is th… | #46 → «"answer": "самым низким идентификатором моста"» |
| 05.02.12-stp-operations-quiz | 3 | style | "к корневому мосту" repeated twice in one short stem. | #46 → «с точки зрения наименьшей общей стоимости пути (лучший путь) — это...» |
| 05.02.12-stp-operations-quiz | 3 | style | "невыделенный порт" (non-designated port): the module calls designated ports «назначенный» and the old role «неназначенный»; «выделенный» is not its term. Same … | #46 → «заблокированный порт или неназначенный порт» |
| 05.02.12-stp-operations-quiz | 4 | error | Comment defines the designated port as the port that "has root path cost" and drops "lowest", so it no longer distinguishes it (every port has a root path cost)… | #46 → «который имеет наименьшую стоимость внутреннего корневого пути к корневому мосту» |
| 05.02.12-stp-operations-quiz | 5 | style | Stem is singular ("Какой ... будет") though two answers are expected, and uses "перенаправлять" (redirect) for forwarding; the comment and module say "пересылат… | #46 → «Какие из следующих портов будут пересылать кадры Ethernet?» |
| 05.02.12-stp-operations-quiz | 5 | style | "не выделенный порт": same off-module term as Q3/Q4 (the module says «неназначенный»), and here also split into two words. | #46 → «заблокированный порт или неназначенный порт» |
| 05.03.06-evolution-of-stp-quiz | 2 | style | Mistranslation: "faster convergence" rendered as "более быстрое соединение" (faster connection), which misstates what RSTP improves. | #46 → «обеспечивает более быструю сходимость» |
| 05.04.02-quiz | 2 | style | Comma between the fronted adverbial and the question word ("После завершения выбора корневого моста, как ..."). | #46 → «После завершения выбора корневого моста как коммутаторы» |
| 05.04.02-quiz | 2 | style | Agreement error in all four answers: plural "проанализируют" followed by singular "использует". | #46 → «и используют» |
| 05.04.02-quiz | 5 | style | "возникновение цикла": the module calls a switching loop «петля» throughout; «цикл» reads as a calque of "loop". | #46 → «чтобы предотвратить возникновение петли» |
| 05.04.02-quiz | 6 | style | MT: "not intended to connect to another switch" is attached to the end devices instead of to the port, so the stem reads as end devices that are not meant to be… | #46 → «Какие понятия относятся к порту коммутатора, к которому предполагается подключать только оконечные устройства и никогда …» |
| 05.04.02-quiz | 6 | style | "состояние переадресации": «переадресация» means redirect; the port state is forwarding («пересылка»). | #46 → «состояние пересылки, пропуская таким образом состояния прослушивания и обучения» |
| 05.04.02-quiz | 6 | style | Copies on answers 4 and 5 differ from answer 1: missing spaces after periods ("коммутатору.Пограничные", "времени.PVST+"), "переадресации" for forwarding, and "… | #46 → «коммутатору. Пограничные порты RSTP должны немедленно перейти в состояние пересылки, пропуская таким образом состояния п…» |
| 05.04.02-quiz | 6 | unclear | Key "пограничный порт" (RSTP edge port) is not taught anywhere in the course; only the comment explains it, so the second key cannot be derived from the module. | operator (kb#275) |
| 05.04.02-quiz | 9 | style | "с более низкой стоимостью для корневого моста" is a calque ("lower cost to the root bridge"); the cost is the path cost to the root bridge. | #46 → «с более низкой стоимостью пути к корневому мосту» |
| 05.04.02-quiz | 10 | style | Typo "BDPU" (should be BPDU). | #46 → «блока BPDU» |
| 05.04.02-quiz | 11 | unclear | Recovering from an STP failure (manually removing redundant links) is not taught; the comment cites "Тема 5.3.0", but 05.03 has no such content. | operator (kb#275) |
| 05.04.02-quiz | 12 | style | Leftover English in an answer: "port ID". | #46 → «"answer": "идентификатор порта"» |
| 05.04.02-quiz | 12 | error | Comment says the BPDU has three fields (priority, extended system ID, MAC); those are the three fields of the bridge ID (BID) carried in the BPDU, not of the BP… | #46 → «Тема 5.2.0 - Идентификатор моста (BID) в BPDU имеет три поля:» |
| 05.04.02-quiz | 14 | style | "резерв" for redundancy; the module calls the concept «резервирование». | #46 → «наиболее точным описанием резервирования?» |
| 05.04.02-quiz | 14 | style | MT artefacts in the comment: "Резерв пытается удалить" (calque of "attempts to remove"), broken "физически кабельных путей", "в сети" twice. | #46 → «Резервирование устраняет единую точку отказа в сети за счет нескольких физических кабельных путей между коммутаторами» |
| 05.04.02-quiz | 14 | style | Answer is a subjectless 3rd-person verb ("проектирует сеть ...") calqued from an English gerund; as an answer to "which is the description" it needs a noun. | #46 → «"answer": "проектирование сети с использованием нескольких виртуальных устройств,» |
| 05.04.02-quiz | 14 | style | Subjectless finite verb ("настраивает коммутатор ...") instead of a noun phrase, as in answer 1. | #46 → «"answer": "настройка коммутатора с надлежащей безопасностью для фильтрации» |
| 05.04.02-quiz | 14 | style | Subjectless finite verb plus a "для ... для обеспечения отсутствия" chain. | #46 → «"answer": "проектирование сети с несколькими путями между коммутаторами, чтобы в ней не было единой точки отказа"» |
| 05.04.02-quiz | 14 | style | Subjectless finite verb ("настраивает роутер ...") instead of a noun phrase. | #46 → «"answer": "настройка маршрутизатора с полной базой данных MAC-адресов,» |
| 05.04.02-quiz | title | style | Typo "оставного дерева" (should be "связующего дерева"; also on the glossary forbidden list). | #46 → «связующего дерева (STP)» |
| 06.01.10-etherchannel-operation-quiz | 4 | style | Typo: stray hyphen before the dash ("Desirable -— режимы"). | #46 → «Desirable — режимы» |
| 06.01.10-etherchannel-operation-quiz | 6 | style | Agreement: two subjects ("On > On и Auto > Desirable") with a singular verb "образует". | #46 → «Auto > Desirable образуют EtherChannel» |
| 06.04.04-quiz | 1 | style | Comma between the fronted adverbial and the question word ("При проверке конфигурации, какая ..."). | #46 → «При проверке конфигурации какая комбинация» |
| 06.04.04-quiz | 2 | style | Comma between the fronted adverbial and the question word ("... для EtherChannel, в каком режиме"). | #46 → «диапазона портов для EtherChannel в каком режиме необходимо настроить PAgP» |
| 06.04.04-quiz | 5 | error | Comment says a "shortest-path tree" recalculation is not required; the protocol in question is STP (spanning tree). The shortest-path tree is a different (link-… | #46 → «пересчет связующего дерева не требуется» |
| 06.04.04-quiz | 5 | style | "один из входящих портов EtherChannel" reads as "one of the incoming ports"; meant: one of the ports that belong to the EtherChannel. | #46 → «Когда один из портов, входящих в EtherChannel, выходит из строя» |
| 06.04.04-quiz | 7 | style | Comma between the fronted adverbial and the question word ("... с помощью PAgP, какой режим"). | #46 → «с помощью PAgP какой режим» |
| 06.04.04-quiz | 8 | style | Case error ("MAC-адреса источника к MAC-адресу") that also sets the key apart from the distractors, which all read "MAC-адрес ... к ...". | #46 → «"answer": "MAC-адрес источника к MAC-адресу назначения"» |
| 06.04.04-quiz | 8 | style | Case error "IP-адреса источника к IP-адреса назначения" (should be "IP-адрес источника к IP-адресу назначения"); like answer 1, it makes the keys look different… | #46 → «"answer": "IP-адрес источника к IP-адресу назначения"» |
| 06.04.04-quiz | 11 | style | Comma before the final "и" in a list ("desirable/auto, и desirable/desirable"). | #46 → «desirable/auto и desirable/desirable» |
| 06.04.04-quiz | 12 | style | Grammar: "LACP, также известен как" needs the participle "известный". | #46 → «LACP, также известный как IEEE 802.3ad» |
| 06.04.04-quiz | 13 | style | Comma between the fronted adverbial and the question word ("... для EtherChannel, в каком режиме"). | #46 → «диапазона портов для EtherChannel в каком режиме необходимо настроить LACP» |
| 06.04.04-quiz | 14 | style | "в пакете EtherChannel": "bundle" calqued as «пакет» (packet), which is misleading; the module says «объединение». | #46 → «Все порты в объединении EtherChannel» |
| 06.04.04-quiz | 15 | style | Comma between the fronted adverbial and the question word ("... с помощью LACP, какой режим"). | #46 → «с помощью LACP какой режим» |
| 07.01.05-dhcpv4-concepts-quiz | 1 | style | Typo "DCHPOFFER" (should be DHCPOFFER), in Q1 and Q3. | #46 → «"answer": "DHCPOFFER"» |
| 07.01.05-dhcpv4-concepts-quiz | 2 | style | Typo "DCHPv4" (should be DHCPv4). | #46 → «Серверы DHCPv4» |
| 07.01.05-dhcpv4-concepts-quiz | 3 | style | Typo "DHCPAK" (should be DHCPACK). | #46 → «сервер отвечает DHCPACK» |
| 07.04.04-quiz | 1 | style | Case error: "для взаимодействии" (should be "для взаимодействия"). | #46 → «для взаимодействия с DHCP-сервером» |
| 07.04.04-quiz | 2 | style | "Чего добивается администратор?" requires a noun answer, but all answers are infinitives ("настроить роутер ..."). | #46 → «Что хочет сделать администратор?» |
| 07.04.04-quiz | 3 | style | Typo "предлржения" (should be "предложения"). | #46 → «предложения» |
| 07.04.04-quiz | 3 | style | Broken grammar: "Несколько серверов могут быть отправить ответ". | #46 → «Несколько серверов могут отправить ответ» |
| 07.04.04-quiz | 4 | style | Leftover English in the stem: the field list is in English ("Destination address", "Client IPv4 address", "Default gateway address", "Subnet mask"). | #46 → «Адрес назначения: 255.255.255.255. IPv4-адрес клиента: 0.0.0.0. Адрес шлюза по умолчанию: 0.0.0.0. Маска подсети: 0.0.0.…» |
| 07.04.04-quiz | 8 | style | "DHCPACKNOWLEDGMENT" is not a DHCP message name; the message is DHCPACK. | #46 → «сообщение DHCPACK» |
| 07.04.04-quiz | 9 | style | Agreement: "эти устройства могут быть настроены ..., но в то же время он может являться DHCP-сервером" (plural subject, singular pronoun). | #46 → «но в то же время могут являться DHCP-серверами» |
| 07.04.04-quiz | 13 | style | Mistranslation: "IP header" rendered as "заголовок IP-адреса" (header of the IP address). | #46 → «в IP-заголовке он укажет» |
| 07.04.04-quiz | 14 | style | Typo "врены" (should be "верны"). | #46 → «(верны два варианта)» |
| 08.01.05-ipv6-global-unicast-address-assigment-quiz | 2 | style | Broken word order: "метод без учета состояния распределения IPv6-адресов" (the qualifier splits "метод распределения"); also "DHCP-сервер" where the key says DH… | #46 → «SLAAC с сервером DHCPv6 — это метод распределения IPv6-адресов без сохранения состояния» |
| 08.02.07-slaac-quiz | 2 | style | Leftover English in prose: "multicast адрес". | #46 → «(адрес многоадресной рассылки ff02::2)» |
| 08.03.06-dhcpv6-quiz | 3 | style | Duplicated "DHCPv6" ("с сохранением состояния DHCPv6") and a missing comma before the second clause. | #46 → «с сохранением состояния, и сообщение» |
| 08.05.03-quiz | 1 | error | Key says the DAD Neighbor Solicitation is sent with the host's own IPv6 address as the destination; DAD sends it to the solicited-node multicast address, with t… | #46 → «отправить сообщение ICMPv6 «Запрос соседнего узла» (Neighbor Solicitation, NS) о собственном IPv6-адресе» |
| 08.05.03-quiz | 1 | error | Same error in the comment: NS "со своим собственным IPv6 в качестве адреса назначения", and NS called "Обнаружение соседей". | #46 → «Он отправляет сообщение ICMPv6 «Запрос соседнего узла» (Neighbor Solicitation, NS) о своем IPv6-адресе на адрес многоадр…» |
| 08.05.03-quiz | 2 | style | Calque "для изучения адреса шлюза по умолчанию" ("to learn the address"). | #46 → «чтобы узнать адрес шлюза по умолчанию?» |
| 08.05.03-quiz | 2 | style | Missing space: "роутера(RA)". | #46 → «а (RA)»» |
| 08.05.03-quiz | 3 | style | Calque "для создания идентификатора интерфейса с помощью хоста IPv6" ("by an IPv6 host"); reads as if the host were a tool. | #46 → «Какие методы может использовать хост IPv6, работающий по SLAAC, для создания идентификатора интерфейса?» |
| 08.05.03-quiz | 3 | style | Broken word order: "автоматическая настройка без сохранения состояния адреса"; and the second method is a random interface ID, not a "случайного адреса". | #46 → «автоматическая настройка адресов без сохранения состояния (SLAAC), может настраивать идентификатор интерфейса двумя спос…» |
| 08.05.03-quiz | 5 | style | Missing space: "интерфейсероутера". | #46 → «интерфейсе ро» |
| 08.05.03-quiz | 7 | error | Comment says FF02::1:2 corresponds to "all DHCP routers"; it is the All_DHCP_Relay_Agents_and_Servers group. Also "DHCP SOLICIT" for the DHCPv6 message. | #46 → «сообщение DHCPv6 SOLICIT на групповой адрес FF02::1:2, который прослушивают все серверы DHCPv6 и агенты ретрансляции» |
| 08.05.03-quiz | 10 | style | Calque "используется в ICMPv6 для хоста, чтобы проверить" and "настройкой в интерфейсе". | #46 → «Какой процесс на основе ICMPv6 используется хостом, чтобы проверить уникальность IPv6-адреса перед его назначением интер…» |
| 08.05.03-quiz | 10 | style | NS mistranslated as "Обнаружение соседей" (Neighbor Discovery, the protocol), and "на собственный IPv6-адрес" suggests it is addressed to the own address. | #46 → «сообщения «Запрос соседнего узла» (Neighbor Solicitation, NS) о собственном IPv6-адресе» |
| 08.05.03-quiz | 11 | style | Broken word order: "метод без учета состояния получения адреса IPv6". | #46 → «SLAAC — это метод получения адреса IPv6 без сохранения состояния, который не требует серверов» |
| 08.05.03-quiz | 13 | style | "без контроля состояния": a rendering of "stateless" the module never uses (and the comment says "с сохранением состояния или без"). | #46 → «сервера DHCPv6 без сохранения состояния» |
| 08.05.03-quiz | 13 | style | "с контролем состояния": a rendering of "stateful" the module never uses. | #46 → «сервера DHCPv6 с сохранением состояния» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 1 | style | Agreement: "для которого" attaches to "сегмента исходной сети", so the host lacks routing information for its own segment; it should refer to the remote segment… | #46 → «для которых у отправляющего узла» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 2 | style | Calque "представляет иллюзию" ("presents the illusion"), next to "представляет собой" in the same sentence. | #46 → «Какое устройство создает иллюзию» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 3 | style | "группа виртуальных роутеров" means a group made of virtual routers; the device is a physical member of the virtual router group. | #46 → «входящее в группу виртуального маршрутизатора, выполняет роль альтернативного» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 3 | style | Same calque in the comment: "входящее в группу виртуальных". | #46 → «входящее в группу виртуального маршрутизатора, которому назначена роль альтернативного» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 4 | style | Same "группа виртуальных роутеров" calque as Q3, and the stem lacks the question mark. | #46 → «входящее в группу виртуального маршрутизатора, выполняет роль шлюза по умолчанию?"» |
| 09.01.05-first-hop-redundancy-protocol-quiz | 4 | style | Same calque in the comment: "входящее в группу виртуальных". | #46 → «входящее в группу виртуального маршрутизатора, которому назначена роль шлюза» |
| 09.02.04-hsrp-quiz | 2 | style | Wrong government: "перенимает на себя роль активного с существующего устройства" (should be "у"). | #46 → «он перенимает роль активного у существующего устройства» |
| 09.03.02-quiz | 3 | style | Stem asks for characteristics (plural) but the question is singleChoice with one key. | #46 → «Укажите характеристику VRRPv3.» |
| 09.03.02-quiz | 4 | style | Missing noun: "а все остальные HSRP поддерживают состояние резервирования" (all other HSRP [routers]). | #46 → «а все остальные маршрутизаторы HSRP поддерживают состояние резервирования» |
| 09.03.02-quiz | 6 | style | Leftover English in an answer: "hostname" (the comment says "имя хоста"). | #46 → «"answer": "имя хоста"» |
| 09.03.02-quiz | 6 | style | Calque "представлял иллюзию" ("present the illusion"); the module and 09.01.05 say "создать иллюзию". | #46 → «создавал иллюзию» |
| 09.03.02-quiz | 7 | style | Clumsy calque "Чем представляется в терминологии FHRP набор роутеров"; meant: what the set is called. | #46 → «Как в терминологии FHRP называется набор» |
| 09.03.02-quiz | 11 | unclear | GLBP details (number of gateways, virtual MACs, IPv6) are not taught; the module only says GLBP balances load. The comment claims there is no four-gateway limit… | operator (kb#275) |
| 10.01.06-endpoint-security-quiz | 1 | unclear | Distractor 'вредоносное ПО' is defensible: the module classifies ransomware as a malware attack, and the comment on that option does not say why it is wrong | operator (kb#275) |
| 10.01.06-endpoint-security-quiz | 2 | style | Calque 'могут быть настроены с мерами безопасности' (configured with security measures) | #47 → «Хотя на коммутаторе и WLC можно настроить функции безопасности» |
| 10.01.06-endpoint-security-quiz | 3 | style | Broken purpose chain 'чтобы блокировать ... и шифровать ... и предотвратить': two 'и' and a perfective verb mixed with imperfectives; data-loss prevention is th… | #47 → «чтобы блокировать угрозы и шифровать исходящие сообщения для предотвращения потери данных?» |
| 10.02.07-access-control-quiz | 1 | style | Clumsy inversion 'Собирает данные и формирует отчеты учет AAA': the object 'отчеты' runs into the subject 'учет AAA' | #47 → «Сбор данных и формирование отчетов – задача учета AAA» |
| 10.02.07-access-control-quiz | 4 | style | English-style comma after the introductory phrase in a question | #47 → «В реализации 802.1X какое устройство» |
| 10.03.04-layer-2-security-threats-quiz | 1 | style | 'для защиты от 3 до 7 уровня' reads as 'protection against layers 3 to 7'; range should be 'уровней с 3 по 7' | #47 → «используются для защиты уровней с 3 по 7 модели OSI?» |
| 10.03.04-layer-2-security-threats-quiz | 1 | style | Comment says 'уровня с 3 до 7' (mixed range construction) and names option 1 in English 'DHCP Snooping' while the option says 'анализ DHCP-трафика' | #47 → «угроз на уровнях с 3 по 7. Анализ DHCP-трафика и IPSG» |
| 10.03.04-layer-2-security-threats-quiz | 1 | unclear | Options 'IPSG' and 'DAI' are abbreviations the 10.03 lecture never introduces (its table says 'IP Source Guard' and 'Динамический анализ ARP-трафика'); they fir… | operator (kb#275) |
| 10.03.04-layer-2-security-threats-quiz | 2 | style | Leftover English 'Port security' as an answer option; the module table names it 'Безопасность портов' | #47 → «"answer": "безопасность портов"» |
| 10.03.04-layer-2-security-threats-quiz | 2 | style | Leftover English 'Port security' in comment prose | #47 → «Безопасность портов предотвращает различные типы атак» |
| 10.03.04-layer-2-security-threats-quiz | 4 | style | 'подделку ARP-адресов': there are no 'ARP addresses'; the attack is ARP spoofing | #47 → «может предотвратить атаки подмены ARP и «отравление» ARP-кэша?» |
| 10.04.04-mac-address-table-attack-quiz | 2 | style | 'МАС' is typed in Cyrillic letters (М, А, С), unlike 'MAC' elsewhere; breaks search and screen-reader pronunciation | #47 → «таблицы MAC-адресов?» |
| 10.04.04-mac-address-table-attack-quiz | 3 | style | Leftover English 'Port security' as the key answer | #47 → «"answer": "безопасность портов"» |
| 10.04.04-mac-address-table-attack-quiz | 3 | style | Calque 'методом снижения атак' (mitigating attacks) and 'обеспечение безопасности порта' | #47 → «Основным методом защиты от атак на таблицу MAC-адресов является безопасность портов» |
| 10.05.11-lan-attacks-quiz | 1 | style | Broken government 'выдать себя за другое ... устройство, например, как шлюз' (should be 'за шлюз') | #47 → «чтобы выдать себя за другое легитимное устройство, например за шлюз по умолчанию» |
| 10.05.11-lan-attacks-quiz | 4 | style | Typo 'незапрощенный' and broken construction 'полагать, что его устройство является законным, например, как шлюз' | #47 → «Злоумышленник может отправить незапрошенный (gratuitous) ARP-ответ, заставляющий все устройства считать его устройство з…» |
| 10.06.02-quiz | 2 | unclear | Key CDP is a vendor-proprietary protocol; distractor LLDP is defensible in a vendor-neutral course, since many vendors ship LLDP enabled by default (the stem as… | operator (kb#275) |
| 10.06.02-quiz | 4 | style | 'МАС' typed in Cyrillic letters, plus a stray final period in the option | #47 → «"переполнение таблицы MAC-адресов"» |
| 10.06.02-quiz | 5 | style | Leftover English 'Topic' instead of 'Тема' (the other comments in the file use 'Тема') | #47 → «Тема 10.2.0 - Метод аутентификации» |
| 10.06.02-quiz | 6 | error | Answer 4 is text copied from Q12 ('подставной DHCP-сервер предоставляет ложные параметры...'), not a protocol; its own comment shows the intended option was TAC… | #47 comments emptied |
| 10.06.02-quiz | 6 | style | English-style comma after the introductory phrase in a question | #47 → «В серверной реализации AAA какой протокол» |
| 10.06.02-quiz | 7 | style | Comment mixes English feature names (Dynamic ARP Inspection, DHCP-Snooping, Port security) and the MT calque 'голодание DHCP'; options use the Russian names | #47 → «динамический анализ ARP-трафика (DAI) — предотвращает атаки подмены ARP и «отравление» ARP-кэша; отслеживание DHCP-сообщ…» |
| 10.06.02-quiz | 7 | style | Leftover English 'Port security' as an answer option | #47 → «"answer": "безопасность портов"» |
| 10.06.02-quiz | 8 | style | 'ААА' typed in Cyrillic letters, in English word order 'ААА аутентификация' | #47 → «Аутентификация AAA — это процесс» |
| 10.06.02-quiz | 9 | style | Leftover English 'Topic' instead of 'Тема' | #47 → «Тема 10.5.0 - Атака истощения» |
| 10.06.02-quiz | 9 | style | 'МАС' typed in Cyrillic letters | #47 → «"переполнение таблицы MAC-адресов"» |
| 10.06.02-quiz | 10 | style | Leftover English 'IPS Sensor' as an answer option | #47 → «"answer": "Сенсор IPS"» |
| 10.06.02-quiz | 11 | style | The question hinges on the term 'запрашивающее устройство', which the course never uses: the lecture calls the role 'Клиент (Supplicant)' | #47 → «называется запрашивающим устройством (supplicant)?» |
| 10.06.02-quiz | 11 | style | Leftover English 'Topic'; also tie the term to the lecture's 'Supplicant' | #47 → «Тема 10.2.0 - В терминологии стандарта 802.1X клиентская рабочая станция называется запрашивающим устройством (supplican…» |
| 10.06.02-quiz | 12 | style | Wrong case: the subject of 'включает в себя' is in the accusative ('атаку') | #47 → «Что включает в себя атака спуфинга IP-адреса?» |
| 10.06.02-quiz | 13 | style | 'архитектура аутентификации' mistranslates 'AAA framework': accounting and authorization are not services of an authentication architecture | #47 → «Какие сервисы предоставляет архитектура AAA?» |
| 10.06.02-quiz | 13 | style | Agreement error 'сервисы, помогающий' (should be plural) | #47 → «предоставляет сервисы, помогающие защитить» |
| 10.06.02-quiz | 14 | style | 'получить доступ только к серверу с FTP' changes the meaning (only to a server that has FTP); intended: access the server only over FTP | #47 → «пользователь может обращаться к серверу только по FTP.» |
| 10.06.02-quiz | 14 | style | 'ААА' typed in Cyrillic letters | #47 → «через AAA службы авторизации» |
| 10.06.02-quiz | 15 | style | Leftover English 'Topic' and 'port security' in comment prose | #47 → «Тема 10.3.0 - Атаке с переполнением таблицы MAC-адресов (CAM), переполнению буфера и спуфингу MAC-адресов можно противод…» |
| 10.06.02-quiz | 15 | style | Leftover English 'port security' in the key answer | #47 → «"answer": "включение безопасности портов"» |
| 11.06.04-quiz | 1 | error | Comment claims port security cannot be enabled on a trunk; the module says it can be set on manually configured access or trunk ports | #47 → «Тема 11.2.0 - Безопасность портов ограничивает число MAC-адресов на порту и не устраняет риски, связанные с Native VLAN.» |
| 11.06.04-quiz | 1 | style | Leftover English 'port security' in an answer option | #47 → «"answer": "использовать безопасность портов"» |
| 11.06.04-quiz | 2 | style | Key 'применимо ко всем портам конечного пользователя' does not answer 'На каких портах...' and does not match the other options' form | #47 → «"answer": "на всех портах конечного пользователя"» |
| 11.06.04-quiz | 4 | style | Leftover English 'port security' as the key answer (Q4 and Q12) | #47 → «"answer": "безопасность портов",» |
| 11.06.04-quiz | 4 | style | English 'port security' in prose and the ungrammatical calque 'блокировать вредоносные от выдачи информации' | #47 → «Функция безопасности портов может ограничивать количество динамически изучаемых MAC-адресов на порт или разрешать подклю…» |
| 11.06.04-quiz | 5 | error | Key is mistranslated: 'согласования внешних линий для внешних портов' (external lines/ports) instead of trunk negotiation on trunk ports, so the correct answer … | #47 → «отключение согласования магистрального канала на магистральных портах и статическая настройка немагистральных портов в к…» |
| 11.06.04-quiz | 5 | style | Distractor uses ISL, a vendor-proprietary trunking encapsulation that the course never mentions | #47 → «использование инкапсуляции 802.1Q на всех магистральных каналах» |
| 11.06.04-quiz | 5 | style | Tautology with leftover English 'протокола Spanning Tree Protocol (STP)' | #47 → «Отключение протокола связующего дерева (STP) на это не повлияет» |
| 11.06.04-quiz | 6 | style | Leftover English 'port security' in an answer option | #47 → «"answer": "включение безопасности портов глобально"» |
| 11.06.04-quiz | 7 | style | Redundant 'типы портов коммутаторов используются на коммутаторах' and the calque 'в составе средств защиты' | #47 → «Какие типы портов используются на коммутаторах для защиты от атак DHCP-спуфинга?» |
| 11.06.04-quiz | 9 | style | Leftover English 'port security' in an answer option | #47 → «а затем повторно включить безопасность портов» |
| 11.06.04-quiz | 9 | style | Leftover English 'port security' in comment prose | #47 → «на котором настроены функции безопасности портов» |
| 11.06.04-quiz | 9 | style | Truncated word 'интерфей' at the end of the comment | #47 → «чтобы активировать интерфейс"» |
| 11.06.04-quiz | 10 | style | Missing space 'DHCPнужно' | #47 → «отслеживания DHCP нужно» |
| 11.06.04-quiz | 12 | style | English 'port security' in prose and slang 'зафлудить' | #47 → «Функция безопасности портов ограничивает количество MAC-адресов источника, которым разрешено передавать данные через пор…» |
| 11.06.04-quiz | 13 | style | Option 3 'атаки путем подделки ARP' is the same attack as option 4 'ARP-spoofing'; the intended distractor is ARP-cache poisoning | #47 → «"answer": "«отравление» ARP-кэша"» |
| 12.04.06-capwap-operation-quiz | 3 | style | Missing space '136в' | #47 → «IP-протокол 136 в заголовке» |
| 12.04.06-capwap-operation-quiz | 3 | unclear | By RFC 5415 the CAPWAP control channel over IPv6 uses UDP (IP protocol 17) and only the data channel may use UDP-Lite (136), so distractor '17' is defensible; t… | operator (kb#275) |
| 12.04.06-capwap-operation-quiz | 4 | style | English-style comma after the introductory phrase and the calque 'является ответственностью AP' | #47 → «За что из перечисленного отвечает AP в разделенной архитектуре MAC для CAPWAP?» |
| 12.04.06-capwap-operation-quiz | 5 | style | English-style comma after the introductory phrase and the calque 'является ответственностью WLC' | #47 → «За что из перечисленного отвечает WLC в разделенной архитектуре MAC для CAPWAP?» |
| 12.04.06-capwap-operation-quiz | 6 | style | Spelling: predicative 'неверно' is written as one word here | #47 → «поэтому утверждение неверно» |
| 12.06.06-wlan-threats-quiz | 2 | style | Spelling: predicative 'неверно' is written as one word here | #47 → «поэтому утверждение неверно» |
| 12.07.09-secure-wlans-quiz | 5 | style | MT artefact: 'open (authentication)' rendered as the verb 'открыть' | #47 → «"answer": "открытая аутентификация"» |
| 12.08.02-quiz | 2 | error | Comment explains 'Single Point Setup (SPS)', but the option is 'система аварийного электропитания' (SPS mistranslated as a standby power system); the comment do… | #47 → «Система аварийного электропитания поддерживает работу устройства при отключении основного питания и не влияет на скорост…» |
| 12.08.02-quiz | 5 | unclear | Distractor 'широковещательно выполняет запрос SSID' also describes active mode: in active mode the client broadcasts probe requests carrying the SSID | operator (kb#275) |
| 12.08.02-quiz | 13 | style | 'работает на одноранговой основе без сети': an ad hoc WLAN is a network; it works without an access point | #47 → «работает на одноранговой основе без точки доступа» |
| 12.08.02-quiz | 13 | error | Comment says Wi-Fi Direct is unrelated to WLAN topologies; the module gives Wi-Fi Direct as an example of the ad hoc mode | #47 → «Wi-Fi Direct используется для прямого подключения устройств друг к другу без точки доступа и не объединяет несколько BSS» |
| 13.05.04-quiz | 2 | style | Key 'закрытая' does not match the module term 'частная' (private) addressing | #47 → «"answer": "частная"» |
| 13.05.04-quiz | 5 | style | English-style comma before the question word after a long introductory phrase | #47 → «Что необходимо создать на контроллере беспроводной локальной сети (WLC) перед формированием новой корпоративной WLAN WPA…» |
| 13.05.04-quiz | 9 | style | Letter 'ё' in 'удалённым'; the course writes 'е' | #47 → «удаленным» |
| 13.05.04-quiz | 10 | style | Letter 'ё' in 'нём'; the course writes 'е' | #47 → «на нем настроен» |
| 13.05.04-quiz | 12 | style | Typo 'устойствам' | #47 → «офисным устройствам» |
| 13.05.04-quiz | 14 | unclear | The question tests the tab layout of one vendor's WLC web GUI (Monitor / WLANs / Commands / Controller); in a vendor-neutral course the answer is model-specific | operator (kb#275) |
| 14.01.07-path-determination-quiz | 1 | style | Distractor renders "neighbor cache" as "кэш соседнего устройства" (a neighbouring device's cache); the module term is «кэш соседей». | #48 → «"answer": "кэш соседей"» |
| 14.01.07-path-determination-quiz | 3 | style | Participial phrase after the noun is not set off by a comma. | #48 → «"маршруты, полученные через протокол динамической маршрутизации"» |
| 14.02.04-packet-forwarding-quiz | 2 | style | Typo: "IPv4 пакета" lacks the hyphen used everywhere else ("IPv4-пакета", Q1). | #48 → «"на устройство с адресом назначения IPv4-пакета"» |
| 14.02.04-packet-forwarding-quiz | 3 | unclear | Asks for the default forwarding mechanism "in the router OS" with key CEF, a Cisco-proprietary mechanism and a vendor default. The lecture still teaches CEF, so… | operator (kb#275) |
| 14.04.13-ip-routing-table-quiz | 1 | style | Clumsy genitive chain and redundancy: «информация о маршруте пути … об обратном маршруте или пути возврата». | #48 → «информация о пути из одной сети в другую также предоставляет сведения об обратном пути» |
| 14.04.13-ip-routing-table-quiz | 3 | style | Comma before «и» joining two homogeneous clauses under one «если». | #48 → «доступен один маршрут и у роутера» |
| 14.04.13-ip-routing-table-quiz | 6 | style | Agreement error garbles the stem: masculine «который был автоматически определен» attaches to «статический маршрут», so it says the static route was learned by … | #48 → «Администратор настраивает статический маршрут к сети назначения, о которой маршрутизатор уже узнал автоматически с помощ…» |
| 14.05.06-static-and-dynamic-routing-quiz | 4 | style | Colloquial definition «— это когда роутер имеет …»; not literary Russian. | #48 → «Балансировка нагрузки с равной стоимостью — это отправка пакетов по двум или более путям к месту назначения с метриками …» |
| 14.06.02-quiz | 1 | style | English left in an answer option: "next-hop". | #48 → «"answer": "следующий переход"» |
| 14.06.02-quiz | 1 | style | MT artefact: «— это назначения для отправки трафика после его сопоставления в роутере». | #48 → «Следующий переход или выходной интерфейс указывают, куда отправить трафик после того, как для него найден маршрут» |
| 14.06.02-quiz | 2 | style | MT artefacts: calque «для размещения растущей сети» and tautology «Вмешательство требуется …, когда требуется изменение маршрута». | #48 → «Они плохо масштабируются, так как по мере роста сети их приходится перенастраивать вручную. Любое изменение маршрута тре…» |
| 14.06.02-quiz | 6 | unclear | Question is about CEF (FIB + adjacency table → "CEF"), a Cisco-proprietary mechanism. The lecture still teaches CEF; de-marketing item 2.5 renames it to «пересы… | operator (kb#275) |
| 14.06.02-quiz | 7 | style | Wrong case «используется на пограничный роутер» (should be prepositional), and English left in prose «маршрут quad zero»; the course term is «маршрут с четырьмя… | #48 → «Маршрут по умолчанию обычно используется на пограничном роутере компании для подключения к поставщику услуг Интернета. М…» |
| 14.06.02-quiz | 9 | style | Collocation error «самая быстрая пропускная способность» (calque of "fastest bandwidth"); bandwidth is high, not fast. | #48 → «"самая высокая пропускная способность исходящих интерфейсов"» |
| 14.06.02-quiz | 10 | style | Route-source code typed as Cyrillic «Н» (U+041D) instead of Latin "H" (the NHRP code in the table legend). | #48 → «"answer": "H"» |
| 14.06.02-quiz | 10 | style | Code for connected routes typed as Cyrillic «С» (U+0421) in «(С)»; the answer and the routing table use Latin "C". | #48 → «Непосредственно подключенные (C)» |
| 14.06.02-quiz | 11 | style | Grammar slip «цифры внутри скобки» (singular genitive for the pair of brackets). | #48 → «цифры в квадратных скобках указывают» |
| 14.06.02-quiz | 14 | style | Typo in the count hint: «(верный два варианта)». | #48 → «(верны два варианта)» |
| 14.06.02-quiz | 14 | style | Typo «ССтатические» (doubled letter). | #48 → «Тема 14.5.0 - Статические» |
| 14.06.02-quiz | 15 | error | The comment gives the IPv6 default route as ":/0" (invalid notation, contradicts the key "::/0"); the next sentence is a calque («Это представляет все нули…»). | #48 → «IPv6-адрес и префикс для статического маршрута по умолчанию — ::/0, то есть адрес из одних нулей с длиной префикса 0» |
| 15.01.08-static-routes-quiz | 1 | error | The key says the next hop is identified by the "destination IP address". The next hop is identified by its own IP address (and/or the exit interface), not by th… | #48 → «"answer": "IP-адрес следующего перехода"» |
| 15.01.08-static-routes-quiz | 1 | error | The comment repeats the error: «по IP-адресу назначения и/или выходному интерфейсу». | #48 → «по его IP-адресу и/или по выходному интерфейсу» |
| 15.01.08-static-routes-quiz | 2 | error | The distractor «сеть назначения определяется с помощью сетевого адреса и маски» is a true statement about an IPv4 static route, so the question has two correct … | #48 → «"сеть назначения определяется только сетевым адресом, без маски подсети"» |
| 15.01.08-static-routes-quiz | 3 | style | Stray comma between subject and predicate: «… в статическом маршруте IPv6, идентифицируется». | #48 → «Сеть назначения в статическом маршруте IPv6 идентифицируется» |
| 15.01.08-static-routes-quiz | 3 | style | Dangling gerund: «используя только префикс IPv6» answers a passive «Как определяется сеть…?», and breaks the parallel with the other options («с помощью …»). | #48 → «"только с помощью префикса IPv6"» |
| 15.06.04-quiz | 4 | error | The comment says a floating static route has a higher metric than dynamic routes; it has a higher administrative distance. | #48 → «Плавающий статический маршрут имеет более высокое административное расстояние, чем основной маршрут, и служит резервным» |
| 15.06.04-quiz | 5 | style | Undefined abbreviation «АР» for administrative distance; the course uses «административное расстояние (AD)». | #48 → «Административное расстояние плавающего статического маршрута указывается в конце команды» |
| 15.06.04-quiz | 6 | style | «Какое выражение создаст …» calques "statement"; the options are CLI commands. | #48 → «Какая команда создаст рекурсивный статический маршрут IPv6?» |
| 15.06.04-quiz | 7 | error | The second sentence applies the rationale for local (L) host routes (processing packets addressed to the router itself instead of forwarding them) to a static h… | #48 → «Статический маршрут к такому адресу настраивают вручную, чтобы направлять трафик к определенному устройству, например к …» |
| 15.06.04-quiz | 10 | style | Faulty comparison: «с административным расстоянием, превышающим динамически изучаемый … маршрут» compares a distance with a route. | #48 → «с административным расстоянием выше, чем у динамически изученного или другого статического маршрута» |
| 15.06.04-quiz | 12 | style | Broken code span «`show ip rout`e» and a meaningless MT phrase «выводит ее для компьютера». | #48 → «Команда `show ip route` показывает, какой из маршрутов сейчас установлен в таблице.» |
| 15.06.04-quiz | 13 | style | Broken grammar «Если задано большее административного расстояния для текущего протокола…» and MT nonsense «имеют специфику использования в качестве первичных». | #48 → «Если с помощью параметра `distance` задать административное расстояние больше, чем у работающего протокола маршрутизации…» |
| 15.06.04-quiz | 14 | style | The option does not fit the question «Почему …?»: «быть приоритетным маршрутом …» lacks «чтобы» (the other options read «для …»). | #48 → «"чтобы стать приоритетным маршрутом в таблице маршрутизации"» |
| 16.01.02-packet-processing-with-static-routes-quiz | 1 | style | Calque «находится на другом сегменте L2, чем PC1», English «L2» in prose, and word order «полученные пакеты от PC1». | #48 → «Поскольку PC1 и R2 находятся в разных сегментах второго уровня, R1 должен деинкапсулировать кадры, полученные от PC1, и …» |
| 16.01.02-packet-processing-with-static-routes-quiz | 2 | style | Typo «состоящийиз» (missing space) and missing comma before the participial phrase. | #48 → «использует адрес назначения, состоящий из всех единиц» |
| 16.03.04-quiz | 1 | style | MT artefacts: tautology «проверка MAC-адреса … для проверки того», dangling gerund «Предполагая, что …, поле «Тип Ethernet» проверяется», and a missing comma be… | #48 → «Когда роутер получает пакет, он сначала проверяет MAC-адрес назначения, чтобы решить, нужно ли обрабатывать пакет дальше…» |
| 16.03.04-quiz | 2 | style | MT error changes the meaning: «помогающие устранять статические маршруты» says the commands help remove static routes, not troubleshoot them. | #48 → «помогающие устранять неполадки статических маршрутов» |
| 16.03.04-quiz | 3 | style | «интерфейса, находящегося по адресу следующего перехода» says the interface at the next-hop address, which is on the neighbour; show ip interface brief shows on… | #48 → «интерфейса, подключенного к сети следующего перехода» |
| 16.03.04-quiz | 5 | style | «Какой оператор описывает …» mistranslates "statement"; «оператор» means operator. | #48 → «Какое утверждение описывает последовательность процессов» |
| 16.03.04-quiz | 6 | style | CDP leftover: the stem asks about `show cdp neighbor`, but the module now presents the standard LLDP (`show lldp neighbors`) for this check, and de-marketing it… | #48 → «вводит команду `show lldp neighbors` на нескольких устройствах при документировании сети» |
| 16.03.04-quiz | 6 | style | The comments name the CDP command; they follow the stem change to LLDP. | #48 → «Команда show lldp neighbors выводит сведения о напрямую подключенных соседних устройствах» |
| 16.03.04-quiz | 8 | style | MT errors: «статическая сеть» for a static route, and «этот маршрут не обязательно должен находиться в состоянии «up/up» … на удаленном роутере» (routes have no… | #48 → «правильно введенный статический маршрут не попадает в таблицу маршрутизации, если выходной интерфейс недоступен. 192.168…» |
| 16.03.04-quiz | 9 | style | The key says the router «удалит» (deletes) the packet; the course and this question's own comment say «отбрасывает» (drops). | #48 → «"answer": "отбросит его"» |

## Findings: Exams

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| 01-04-exam | 1 | style | Grammar: wrong preposition form "об настройке" (should be "о настройке"). | #49 → «информацию о настройке» |
| 01-04-exam | 3 | style | Comment calques "boot loader commands" as a single command "boot loader" and says "файловую флеш-систему" (flash file system). | #49 → «Команды загрузчика (boot loader) позволяют отформатировать файловую систему флэш-памяти» |
| 01-04-exam | 11 | style | Calque of "significant difference": «значительная разница» means a large difference in amount, not a key distinction. | #49 → «Каково главное различие» |
| 01-04-exam | 15 | style | Word-for-word calque of "application-specific integrated circuits"; the Russian term is «специализированные интегральные схемы». | #49 → «Специализированные интегральные схемы (ASIC)» |
| 01-04-exam | 16 | style | Option mistranslates "drops the frame" as «пропускает кадр», which reads as "lets the frame through". | #49 → «Коммутатор отбрасывает кадр.» |
| 01-04-exam | 17 | style | «в таблицу коммутаторов» (plural, "table of switches") is a mistranslation of the switch MAC address table. | #49 → «в таблицу MAC-адресов коммутатора» |
| 01-04-exam | 18 | style | Leftover English "and" in prose, missing spaces around the quoted terms, broken sentence. | #49 → «Коммутаторы используют два метода пересылки кадров: коммутацию с промежуточным хранением (store-and-forward) и сквозную …» |
| 01-04-exam | 21 | style | Duplicated term "management VLAN (management VLAN)" at sentence start (search-and-replace artefact). | #49 → «VLAN управления (management VLAN) настроена» |
| 01-04-exam | 22 | style | Command typo in the comment: stray space in "delete flash: vlan.dat". | #49 → «delete flash:vlan.dat» |
| 01-04-exam | 24 | error | Comment says VLAN broadcast domains span "several VLAN segments", which contradicts the key (only VLAN 20 sees the frame); the source says physical LAN segments… | #49 → «могут охватывать несколько физических сегментов LAN» |
| 01-04-exam | 25 | style | Comment quotes a Russian output line «Согласование магистральной связи» that does not exist on the exhibit; the exhibit shows "Negotiation of Trunking: On". | #49 → «Строка «Negotiation of Trunking: On» на рисунке» |
| 01-04-exam | 26 | style | Mistranslation "affected ports" -> «Поврежденные порты» (damaged ports); the comment then explains nothing. | #49 → «Порты остаются назначенными удаленной VLAN: они не отключаются, не переходят в режим магистрального канала и не перенося…» |
| 01-04-exam | 27 | unclear | Option «значение, которое поддерживает реализацию уровня или сервиса» is garbled ("level or service" for "level of service", i.e. QoS priority); the lecture has… | operator (kb#275) |
| 01-04-exam | 29 | style | Answer label "nonegotiated" is not the CLI keyword; the keyword is "nonegotiate". | #49 → «nonegotiate» |
| 01-04-exam | 32 | style | Comment sentence «связывает сеть с интерфейсом» ("links the network with the interface") is meaningless; it should explain why distractor 3 (command must point … | #49 → «Команда mls qos trust cos задается на интерфейсе и не указывает VLAN.» |
| 01-04-exam | 33 | error | Comment lists "switchport access vlan 150" as the command that assigns the voice VLAN; that is the very error q32 asks about. The voice VLAN is assigned with "s… | #49 → «SW3(config-if)# switchport voice vlan 150» |
| 01-04-exam | 34 | error | Marked answer lost its negation: it says G0/2 IS configured as a trunk, but the exhibit lists only Gig0/1 and the comment says G0/2 is not a trunk. | #49 → «интерфейс G0/2 не настроен в качестве магистрального канала» |
| 01-04-exam | 36 | style | Case agreement error: «на коммутаторе, подключенному» (should be prepositional «подключенном»). | #49 → «коммутаторе, подключенном к интерфейсу» |
| 01-04-exam | 36 | style | Gender agreement error in the comment: «должен использоваться команда». | #49 → «должна использоваться команда» |
| 01-04-exam | 39 | error | Comment says Gi1/1 must be an access port in VLAN 10, but the exhibit connects Gi1/1 to router Gi0/0 (172.16.20.254/24) and labels it VLAN 20. | #49 → «с назначенной VLAN 20» |
| 01-04-exam | 42 | error | Comment gives the subinterface networks as 172.168.1.0/27, .64/27, .96/27; the hosts and subinterfaces in the exhibit are in 172.18.1.0. | #49 → «172.18.1.» |
| 01-04-exam | 44 | style | Calque "is programmed with an IP address" -> «программируется по IP-адресу» ("by IP address"). | #49 → «Вместо этого ему назначается IP-адрес.» |
| 01-04-exam | 45 | style | Broken phrase «сеть management VLAN коммутатором» (instrumental case left from a partial replacement). | #49 → «сеть VLAN управления коммутатором» |
| 01-04-exam | 54 | style | Mistranslation: «трафик управления голосом и сетью» reads as "voice-management and network-management traffic"; the source means voice traffic and network manag… | #49 → «голосовой трафик и трафик управления сетью» |
| 01-04-exam | 56 | unclear | Two defensible answers: the stem asks which VLAN type is initially "the management VLAN", and the distractor "Management VLAN" / «VLAN управления» is tautologic… | operator (kb#275) |
| 01-04-exam | 66 | style | Duplicated term «Сеть native VLAN (native VLAN)» (search-and-replace artefact). | #49 → «Собственная VLAN (native VLAN)» |
| 05-06-exam | 0 | style | Typo in the exam description: «Протокол оставного дерева» (should be «связующего дерева»). | #49 → «Протокол связующего дерева (STP)» |
| 05-06-exam | 5 | error | Comment says VLANs reduce the NUMBER of broadcast domains; VLANs split a broadcast domain, i.e. they reduce the size (and increase the number). | #49 → «Виртуальные LAN уменьшают размер доменов широковещательной рассылки» |
| 05-06-exam | 5 | style | Distractor «для широковещательной адресации» ("for broadcast addressing") is a mistranslation of "to contain broadcasts". | #49 → «внедрение VLAN для ограничения широковещательной рассылки» |
| 05-06-exam | 7 | style | Matching item «динамичное усиление схождения IEEE 802.1D» is garbled ("dynamic strengthening of converging"); it describes RSTP, an 802.1D enhancement for faste… | #49 → «улучшение IEEE 802.1D, ускоряющее сходимость» |
| 05-06-exam | 11 | style | Comments end with «Протокол CDP используется для обнаружения информации о соседнем устройстве»: CDP is one vendor's protocol, and module 05 mentions neither CDP… | #49 → «Сведения о соседних устройствах собирают протоколы обнаружения соседей, например LLDP.» |
| 05-06-exam | 12 | style | Mistranslation: "faster convergence" rendered as «более быстрое взаимодействие» ("faster interaction"). | #49 → «802.1w или RSTP обеспечивает более быструю сходимость» |
| 05-06-exam | 13 | style | Case error in the option: «петель на роутер» (should be prepositional; new text uses «маршрутизатор» per the operator decision). | #49 → «образования петель на маршрутизаторе» |
| 05-06-exam | 15 | style | Stem asks «В каком из состояний» (which one state) while two answers are correct («верны два варианта»). | #49 → «В каких состояниях портов PVST+» |
| 05-06-exam | 15 | style | Comment calls the learning state «состояние сбора данных», which matches neither the answer option «обучение» nor the module term. | #49 → «это состояние обучения и состояние пересылки» |
| 05-06-exam | 18 | style | Case error: «при отключении … и образования» (the second noun must also be prepositional: «образовании»). | #49 → «и образовании нескольких путей» |
| 05-06-exam | 25 | error | Comment talks about ports on two routers; the question (and the EtherChannel being built) is between two switches. | #49 → «порты, имеющиеся на двух коммутаторах» |
| 05-06-exam | 26 | style | Mixed script: «МАС» in the comment is typed in Cyrillic letters. | #49 → «по MAC-адресу источника к MAC-адресу назначения» |
| 05-06-exam | 31 | style | Case agreement error: «двумя коммутаторами, соединенных» (should be instrumental «соединенными»). | #49 → «коммутаторами, соединенными» |
| 05-06-exam | 33 | style | Spelling: «не может включится» (infinitive needs «-ться»). | #49 → «не может включиться» |
| 05-06-exam | 36 | style | Comment calls the EtherChannel channel-group modes «магистральные режимы» (trunk modes), which is a different setting. | #49 → «совместимые режимы группы каналов» |
| 05-06-exam | 37 | style | Mixed script: «РРР» in the comment is typed in Cyrillic letters (the same comment later has Latin PPP). | #49 → «Многоканальный протокол PPP» |
| 05-06-exam | 38 | style | Single-choice stem asks for «требования» (plural), which suggests several answers; the connected copy also starts lowercase. | #49 → «Укажите требование для настройки транкинга» |
| 05-06-exam | 38 | error | Comment states that EtherChannel is a trunking mode (MT of "because this is a trunking EtherChannel"); an EtherChannel can be access, trunk or routed. | #49 → «Поскольку это магистральный канал EtherChannel» |
| 05-06-exam | 39 | style | MT artefact: the flag "D - down" rendered as «вниз» (direction). | #49 → «со статусом D (down)» |
| 05-06-exam | 50 | style | Broken agreement: «между каждым коммутаторами второго и третьего уровней». | #49 → «между каждым коммутатором 2-го уровня и коммутатором 3-го уровня» |
| 05-06-exam | 51 | style | Comment renders mode "on" as «оба коммутатора включены» ("both switches are powered on") and says mode on uses PAgP. | #49 → «формируется либо когда на обоих коммутаторах задан режим on (тогда PAgP не используется), либо через PAgP, когда один из…» |
| 07-09-exam | 1 | style | Stem says not all options are used, but all four options are matched (no unused option). | #49 → «Сопоставьте каждый тип с его описанием.» |
| 07-09-exam | 4 | style | Mixed script: «МАС» in the option is typed in Cyrillic letters. | #49 → «MAC-адрес и IPv4-адрес DHCP-сервера» |
| 07-09-exam | 7 | style | Case error: «для маршрутизаторе». | #49 → «разрешить на маршрутизаторе ретрансляцию DHCP» |
| 07-09-exam | 9 | error | Stem asks what the client sends AFTER the lease has expired, but the key is the unicast DHCPREQUEST renewal, which is sent BEFORE expiry. After expiry the clien… | #49 → «Какое сообщение отправляет DHCP-клиент, когда срок аренды IP-адреса подходит к концу?» |
| 07-09-exam | 9 | error | Comment repeats the wrong timing: the unicast DHCPREQUEST renewal is sent before the lease expires, not after. | #49 → «Перед окончанием срока аренды своего IP-адреса DHCP-клиент отправляет» |
| 07-09-exam | 14 | style | Case error: «между беспроводным роутере» (should be instrumental; new text uses «маршрутизатор» per the operator decision). | #49 → «между беспроводным маршрутизатором и модемом DSL» |
| 07-09-exam | 15 | style | Misspelling «брендмауере» and a calqued «ISP-…» compound in the option. | #49 → «простая настройка межсетевого экрана интернет-провайдера» |
| 07-09-exam | 15 | style | MT artefact: "if a client is dropped" rendered as «клиент отбрасывается» ("is discarded"). | #49 → «так что если клиент отключается» |
| 07-09-exam | 20 | error | Comment swaps the DHCP/BOOTP ports: 67 is the server port, 68 the client port (q16 of the same exam says so too). | #49 → «Порт 67: DHCP/BOOTP server Порт 68: DHCP/BOOTP client» |
| 07-09-exam | 21 | style | Comment uses «лизинг» (financial leasing) for a DHCP lease; the course term is «аренда». | #49 → «Это сообщение предлагает клиенту аренду, которая содержит информацию об IP-адресе и маске подсети для назначения, IP-адр…» |
| 07-09-exam | 23 | style | Case agreement error: «на маршрутизаторе, подключённому» (prepositional «подключенном»). | #49 → «маршрутизаторе, подключенном к сегменту» |
| 07-09-exam | 23 | error | Comment gives a non-existent command "unicast ipv6-routing"; the command (and the key) is "ipv6 unicast-routing". | #49 → «командой ipv6 unicast-routing» |
| 07-09-exam | 24 | style | Mixed script: the RA flags «М» and «О» in the stem are Cyrillic letters (the comment uses Latin M and O). | #49 → «флаг M равен 0, а флаг O равен 1» |
| 07-09-exam | 25 | style | Distractor has a malformed address «2001DB8:…» and names a DHCPv4 server; the exhibit shows a DHCPv6 server. | #49 → «2001:DB8:1234:5678::10/64 в конфигурацию интерфейса сервера DHCPv6» |
| 07-09-exam | 27 | style | Distractor names a DHCPv4 server in a DHCPv6 question. | #49 → «с сервером DHCPv6, о чем свидетельствует» |
| 07-09-exam | 29 | style | Garbled «длину префикса/префикса (prefix/prefix-length)» with leftover English. | #49 → «комбинируя префикс, длину префикса» |
| 07-09-exam | 34 | style | Wrong expansion of GLBP («для группы»); GLBP is the Gateway Load Balancing Protocol. | #49 → «GLBP (протокол распределения нагрузки для шлюзов)» |
| 07-09-exam | 39 | style | Calque «непатентованный» ("not patented") for "nonproprietary"; the module calls these protocols open («открытый»). | #49 → «является открытым протоколом только для IPv4 с ограниченной» |
| 07-09-exam | 42 | style | Calque «непатентованный» ("not patented") for "nonproprietary"; the module calls these protocols open («открытый»). | #49 → «является открытым протоколом, который использует ICMP» |
| 07-09-exam | 43 | style | Calque «непатентованный» ("not patented") for "nonproprietary"; the module calls these protocols open («открытый»). | #49 → «является открытым протоколом только для IPv4, который имеет» |
| 07-09-exam | 45 | style | Shared comment of q45-q48: calque «значения косой черты» (slash value), doubled «необходимые … необходимые», wrong numeral agreement («254 хостов», «62 хостов»)… | #49 → «Рассчитайте максимальное количество узлов для данной длины префикса и вычтите число статических IP-адресов, зарезервиров…» |
| 07-09-exam | 50 | style | MT artefact: "local link" rendered as «локальная ссылка» (hyperlink). | #49 → «в локальном канале» |
| 10-13-exam | 3 | style | Typo: «DCHP» for DHCP | #50 → «Атаки на исчерпание ресурсов DHCP» |
| 10-13-exam | 5 | style | Broken agreement: «Имя пользователя и пароль могут быть опознан» (plural subject, singular short participle); «опознан» is also the wrong verb (credentials are … | #50 → «Имя пользователя и пароль могут быть раскрыты, если передача данных перехвачена.» |
| 10-13-exam | 7 | style | MT artefact: «адресно-ориентированного пространства памяти» mistranslates content-addressable memory (CAM), which is addressed by content, not by address; the s… | #50 → «ограниченный размер ассоциативной памяти (CAM)» |
| 10-13-exam | 8 | style | Missing full stop between two sentences: «...исходный тег 802.1Q Важной характеристикой...» | #50 → «исходный тег 802.1Q. Важной» |
| 10-13-exam | 8 | style | Broken agreement «к порту, находящимся» (should be dative «находящемуся»), «ё», and the redundant «сеть native VLAN транкового порта» | #50 → «подключен к порту в той же VLAN, что и собственная VLAN (native VLAN) магистрального порта» |
| 10-13-exam | 14 | style | Missing space after the full stop: «MAC-адреса.PC1» | #50 → «MAC-адреса. PC1 имеет» |
| 10-13-exam | 15 | style | Stray space before the full stop after the mode label «Защита» (lost bold formatting) | #50 → «Защита. Пакеты» |
| 10-13-exam | 15 | style | Stray space before the full stop after the mode label «Ограничение» | #50 → «Ограничение. Пакеты» |
| 10-13-exam | 15 | style | Stray space before the full stop after the mode label «Отключение» | #50 → «Отключение. Интерфейс» |
| 10-13-exam | 16 | style | Typo: «BDPU Guard» for BPDU Guard | #50 → «BPDU Guard» |
| 10-13-exam | 18 | style | «достоверные порты» is a wrong word for trusted ports (the module says «доверенные»); missing spaces after two full stops; «подключен в AS3» | #50 → «назначение необходимых доверенных портов на коммутаторах. Доверенные порты ведут к легитимным серверам DHCP. В этом прое…» |
| 10-13-exam | 19 | style | Leftover English «IT» in prose (redundant after «информационной безопасности») and the tautology «обеспечивает безопасность портов на порту» | #50 → «Специалист по информационной безопасности настраивает безопасность порта на коммутаторе.» |
| 10-13-exam | 20 | style | Stray space before the full stop after the command (lost bold formatting) | #50 → «limit rate. Когда» |
| 10-13-exam | 22 | style | Stray space before the final full stop after the command | #50 → «bpduguard enable.» |
| 10-13-exam | 23 | style | MT artefact: «автоматического получения MAC-адреса каждого порта» reads as obtaining each port's own MAC address; the policy is about learning MAC addresses on … | #50 → «настроены на автоматическое изучение MAC-адресов на каждом порту» |
| 10-13-exam | 23 | error | «в последнем случае» limits storing in the running configuration to manually configured sticky addresses; in fact both learned and manually configured sticky ad… | #50 → «либо настраиваться вручную; в обоих случаях адреса хранятся» |
| 10-13-exam | 28 | style | Mixed script: «аd hoc» starts with a Cyrillic «а» | #50 → «(ad hoc)» |
| 10-13-exam | 30 | unclear | The comment states 802.11ad works in the 2.4, 5 and 60 GHz bands. IEEE 802.11ad defines a 60 GHz (DMG) PHY; tri-band operation comes from combining it with 802.… | operator (kb#275) |
| 10-13-exam | 32 | style | MT artefact: «чтобы клиенты знали SSID» says the mode makes clients know the SSID; the point is that clients must already know it | #50 → «Активный — это режим, при котором клиенты должны заранее знать SSID, чтобы подключиться к точке доступа.» |
| 10-13-exam | 33 | error | The comment says 802.11ac is fully compatible with 802.11a/b/g/n; 802.11ac is 5 GHz only and the module gives backward compatibility with 802.11a/n only. Also a… | #50 → «802.11ac обеспечивает скорость передачи данных до 1,3 Гбит/с и обратно совместим с устройствами стандартов 802.11a/n.» |
| 10-13-exam | 34 | style | MT artefact with inverted sense: «не обязательно приведет к тому, что сеть будет медленной» (should be: will not necessarily fix the slow network); missing spac… | #50 → «Замена беспроводных сетевых адаптеров не обязательно устранит медленную работу сети и может дорого обойтись компании. DH…» |
| 10-13-exam | 39 | style | Broken syntax (calque of «it is ... that»): «это большее количество каналов, ..., что позволит повысить» | #50 → «именно большее количество каналов, а не только меньшее количество пользователей, позволит повысить производительность се…» |
| 10-13-exam | 40 | style | Typo: «двухдиапазоном» (should be «двухдиапазонном») | #50 → «двухдиапазонном» |
| 10-13-exam | 41 | error | Distractor «убедиться, что точка доступа выбрана правильно» is effectively the same as the keyed «убедиться, что выбран SSID», so a third answer is defensible; … | #50 → «убедиться, что выбрана правильная среда передачи» |
| 10-13-exam | 41 | style | The comment calls the medium «носитель» (a forbidden calque for media), so it does not visibly match the corrected option «правильная среда передачи» | #50 → «в качестве среды передачи будут использоваться радиоволны» |
| 10-13-exam | 42 | style | «необходимо установить пароль устройства по умолчанию» reads as 'set the device password to its default'; the advice is to change the defaults | #50 → «необходимо изменить заданные по умолчанию пароль устройства, SSID и параметры безопасности» |
| 10-13-exam | 43 | style | Broken agreement in the stem shared by Q43-Q52: «Какой компонент контроля доступа, реализация или протокол ...» (masculine «Какой» with feminine «реализация»), … | #50 → «Какой компонент, механизм или протокол контроля доступа» |
| 10-13-exam | 44 | style | Plural «реализованы» after a singular subject | #50 → «реализуется локально» |
| 10-13-exam | 48 | style | Misplaced comma: «протокол, определяет кому разрешен» (comma before the predicate, none before the subordinate clause) | #50 → «определяет, кому разрешен доступ к сети?» |
| 10-13-exam | 53 | style | Leftover English «(wide-area network)» in the WWAN option of Q53-Q62; the module's term is «беспроводная глобальная сеть», parallel to the other three options | #50 → «беспроводная глобальная сеть» |
| 10-13-exam | 59 | style | «до 91,4 метра» is a converted 300 ft; the module gives the WLAN range as up to 100 m | #50 → «до 100 метров» |
| 10-13-exam | 62 | style | Stray closing parenthesis «метров)?» left after the feet were removed | #50 → «от 6 до 9 метров?» |
| 10-13-exam | 63 | style | MT artefact «Информационная безопасность портов» (port security) and a missing space after the dash | #50 → «Безопасность портов — предотвращает» |
| 10-13-exam | 65 | error | «Максимальное количество поддерживаемых MAC-адресов равно 50» is a device-specific figure that contradicts the module (the maximum depends on the switch and OS;… | #50 → «Secure-shutdown. Максимальное количество защищенных MAC-адресов зависит от коммутатора и ОС.» |
| 10-13-exam | 66 | unclear | Distractor «AAA» is defensible: the question asks which server checks the credentials, and the course calls exactly this a «сервер AAA» (a RADIUS server is an A… | operator (kb#275) |
| 10-13-exam | 68 | unclear | The comment calls CAPWAP «стандартный протокол IEEE»; CAPWAP is an IETF standard (RFC 5415). The lecture says the same, so the course text itself is wrong | operator (kb#275) |
| 14-16-exam | 10 | style | MT artefact «с исходным кодом R» (reads as program source code; meant: the route source code R) and «переадресация» for forwarding | #50 → «Маршрут RIP с кодом источника R используется для пересылки трафика» |
| 14-16-exam | 11 | style | The stem says not all options are used, but both options (static, dynamic) are used: each of the four items maps to one of them | #50 → «Сопоставьте характеристики и соответствующие типы маршрутизации.» |
| 14-16-exam | 14 | style | Stray space before the semicolon after the command | #50 → «no shutdown;» |
| 14-16-exam | 19 | error | Answers 1 and 4 are identical («создать полностью заданный статический маршрут через Fa0/0 с административным расстоянием 1»); in the source the first option is… | #50 comments emptied |
| 14-16-exam | 19 | error | The comment says a floating static route has a LOWER administrative distance than the route already in the table; it must be higher (the comment itself then say… | #50 → «если его административное расстояние больше административного расстояния другого маршрута» |
| 14-16-exam | 19 | style | Genitive chain / calque: «потенциальные проблемы следующих переходов в результате природы множественного доступа сегмента сети Ethernet через роутер B» | #50 → «предотвратит рекурсивный поиск маршрутов и возможные проблемы со следующим переходом, вызванные тем, что сегмент Etherne…» |
| 14-16-exam | 19 | style | «переадресация» for forwarding is a variant the glossary forbids (forwarding row): «пересылка» | #50 → «для пересылки пакета» |
| 14-16-exam | 22 | error | The comment gives EIGRP an administrative distance of 110; internal EIGRP has 90 | #50 → «EIGRP (административное расстояние 90)» |
| 14-16-exam | 22 | style | The comment repeats the same explanation twice (two merged translations of one source comment); the second copy is removed | #50 → «» |
| 14-16-exam | 23 | style | The comment repeats its first sentence («5 в конце команды означает/обозначает административное расстояние...») — two merged translations | #50 → «» |
| 14-16-exam | 23 | style | Typo «перходов» | #50 → «переходов» |
| 14-16-exam | 25 | style | Routing table run into the stem with semicolons; the bank copy shows it as a code block, one route per line | #50 → «Таблица маршрутизации для R2 выглядит следующим образом: ``` Gateway of last resort is not set 10.0.0.0/30 is subnetted,…» |
| 14-16-exam | 28 | style | Tautological calque «IPv6-маршрут статического маршрута ::/0 ...» | #50 → «Статический маршрут ::/0 G0/1 fe80::2» |
| 14-16-exam | 30 | style | MT artefacts: «Номер резервного канала должен быть больше 1» (the number meant is the administrative distance) and «выравнивание нагрузки пакетов для обоих кана… | #50 → «Административное расстояние маршрута через резервный канал должно быть больше 1. В правильном ответе административное ра…» |
| 14-16-exam | 30 | error | The comment calls answers 1 and 2 default routes («либо маршрут по умолчанию, либо плавающий…»); they are static routes to 198.133.219.24/30 and 64.100.210.80/3… | #50 → «Остальные ответы задают статические маршруты только к сетям 198.133.219.24/30 и 64.100.210.80/30, а не маршруты по умолч…» |
| 14-16-exam | 32 | style | Wrong case: «роутер R2 нужен» (needs the dative, as in the other options: «роутеру R1 нужен») | #50 → «роутеру R2 нужен статический маршрут» |
| 14-16-exam | 37 | style | Wrong case: «адрес следующего перехода должен быть адрес ...» (predicate noun needs the instrumental) | #50 → «адрес следующего перехода должен быть адресом последовательного интерфейса R2» |
| 14-16-exam | 38 | style | Typo in the command: mask «0.0.0» has three octets | #50 → «`ip route 0.0.0.0 0.0.0.0 S0/1/1 100`» |
| 14-16-exam | 38 | style | MT artefact: «использовать канал OSPF только в момент его подключения» (the point: the router uses the OSPF link whenever it is up) | #50 → «так что маршрутизатор будет использовать канал OSPF, пока тот работает» |
| 14-16-exam | 38 | style | Case agreement: «задано слишком низкое» → «задано слишком низким» | #50 → «административное расстояние задано слишком низким» |
| 14-16-exam | 39 | style | Calque «Какая структура завершает следующее утверждение» in the stems of Q39-Q42 («структура» for an answer option) | #50 → «Какой вариант завершает следующее утверждение:» |
| 14-16-exam | 45 | style | Malformed address «10.3.86.128.128/26» in the routing-table exhibit | #50 → «10.3.86.128/26» |
| 14-16-exam | 45 | style | Malformed addresses «10.3.2.4.4/30» and «10.3.2.5.5/32» in the routing-table exhibit | #50 → «C 10.3.2.4/30 is directly connected, Serial0/0/1 L 10.3.2.5/32» |
| 14-16-exam | 48 | style | The comment calls the Edge router «периметр» («к периметру», «на уровне периметра») while the options call it Edge; the exhibit labels it «Периметр». The fix na… | #50 → «маршрут по умолчанию на маршрутизаторе R1 к маршрутизатору Edge (на рисунке — «Периметр») и статический маршрут на Edge …» |
| 14-16-exam | 51 | style | Broken command in the comment: «маршрут ipv6 2001: db8: 10:12:: /64» (translated command name, spaces inside the address) | #50 → «Таким образом, нужна команда ipv6 route 2001:db8:10:12::/64 S0/0/0.» |
| 14-16-exam | 51 | style | Calque «адресовать трафик» (route traffic): «направлять трафик» | #50 → «который будет направлять трафик от PC2 к PC1» |
| 14-16-exam | 43–47 | style | Text follows the closing ``` on the same line, so by CommonMark the code block does not close and the question renders inside it; the bank copies put a blank li… | #50 → «R1# ``` Посмотрите на пример.» |
| final-exam | 2 | style | Stray spaces before «,» and «.» after the commands (lost bold formatting) | #50 → «Если интерфейс не был включен командой no shutdown, состояние интерфейса отображается как administratively down (отключе…» |
| final-exam | 4 | style | False causal link: «увеличивается размер широковещательного домена, следовательно, увеличивается и число доменов коллизий» (the number of collision domains grow… | #50 → «увеличивается размер широковещательного домена, а также число доменов коллизий» |
| final-exam | 5 | style | Broken agreement «если MAC-адреса назначения отсутствует» (genitive plural with a singular verb) | #50 → «если MAC-адрес назначения отсутствует» |
| final-exam | 7 | style | Typo «оправляться» for «отправляться» | #50 → «отправляться» |
| final-exam | 8 | style | Wrong preposition «Узел, соединенный к DLS1» (the next clause and the bank copy say «подключенный к») | #50 → «Узел, подключенный к DLS1» |
| final-exam | 9 | style | Stray space before the final full stop after the command | #50 → «show interfaces trunk.» |
| final-exam | 10 | style | Leftover English «management VLAN» as an option; the module calls it «Управляющая VLAN», the bank copy «VLAN управления» | #50 → «"answer": "VLAN управления"» |
| final-exam | 10 | style | Leftover English «voice VLAN» as an option; the module and the bank copy say «голосовая VLAN» | #50 → «"answer": "голосовая VLAN"» |
| final-exam | 11 | style | Duplicated term «По сети management VLAN (management VLAN)» — the Russian term was replaced by the English one inside its own gloss | #50 → «По сети VLAN управления (management VLAN)» |
| final-exam | 13 | style | Stray space before the full stop after the command | #50 → «switchport mode trunk. При» |
| final-exam | 14 | style | Mixed script: «Н2» is written with a Cyrillic «Н» while «H1» and the exhibit use Latin H | #50 → «с H2» |
| final-exam | 14 | style | Stray space before the final full stop after the command | #50 → «switchport access vlan 20.» |
| final-exam | 16 | unclear | The keyed benefit (PVST+ optimises the network through load balancing) and the comment's claims (more bandwidth and CPU, manual root placement) are not taught: … | operator (kb#275) |
| final-exam | 18 | style | Garbled item for RSTP: «динамичное ускорение схождения IEEE 802.1D» (bank: «Динамичное усиление схождения») for «an evolution of 802.1D with faster convergence»… | #50 → «развитие IEEE 802.1D, обеспечивающее более быструю сходимость» |
| final-exam | 19 | style | Garbled comment: stray spaces before «,», «;», «.», English «Layer 2», and «режима группы каналов 1 по команде» — a word-by-word rendering of the command «chann… | #50 → «Вывод команды показывает агрегированный канал с флагами SU: канал EtherChannel второго уровня задействован. Интерфейсы F…» |
| final-exam | 22 | style | Stray space before the comma after the command | #50 → «ip helper-address, после» |
| final-exam | 22 | style | Command listing mixes a line break and semicolons inside running text; the bank copy shows it as a code block | #50 → «выполнил следующие команды: ``` Router(config)# interface g0/0 Router(config-if)# ip address 10.0.1.1 255.255.255.0 Rout…» |
| final-exam | 25 | style | Stray space before the closing parenthesis | #50 → «managed-config-flag)» |
| final-exam | 30 | style | MT artefact «Информационная безопасность портов» (port security) and a missing space after the dash | #50 → «Безопасность портов — предотвращает» |
| final-exam | 31 | style | «Какой оператор описывает» — «оператор» mistranslates «statement» (10-13-exam Q6 says «Какое утверждение») | #50 → «Какое утверждение описывает» |
| final-exam | 33 | error | The comment speaks of rebooting a router; port security and sticky learning are switch features (the options say «перезагрузить коммутатор») | #50 → «но будут утрачены при перезагрузке коммутатора» |
| final-exam | 34 | error | «при вводе нескольких команд ... проверяет предыдущую команду» is wrong: each new ip arp inspection validate command replaces the previous one, which is why onl… | #50 → «Однако в конфигурации может быть только одна команда ip arp inspection validate, поэтому каждая следующая такая команда …» |
| final-exam | 35 | unclear | Two defensible answers: DAI inspects ARP on untrusted ports (option 2), while the only per-port DAI setting in the module is ip arp inspection trust on uplinks … | operator (kb#275) |
| final-exam | 36 | style | Distractor names ISL, a vendor-proprietary trunking encapsulation the course never mentions; a standard encapsulation keeps the option wrong | #50 → «использовать инкапсуляцию 802.1Q на всех магистральных каналах» |
| final-exam | 37 | style | Calque «запрос зонда» (probe request); the module calls it «запрос поиска» (10-13-exam Q27 also says «запрос поиска») | #50 → «поиска» |
| final-exam | 39 | style | Garbled sentences: «WPA2 — это Wi-FI версии 802.11i» (meant: the Wi-Fi Alliance implementation of 802.11i; «Wi-FI» typo) and «Стандарт AES совпадает с протоколо… | #50 → «WPA2 — это реализация стандарта 802.11i от Wi-Fi Alliance, отраслевой стандарт для аутентификации. Ни WEP, ни WPA не пре…» |
| final-exam | 40 | error | The comment says that changing the default SSID forces users to type the name manually; that is the effect of disabling SSID broadcast (the key), not of renamin… | #50 → «При изменении имени сети по умолчанию и отключении его широковещательной рассылки пользователям устройств приходится вру…» |
| final-exam | 40 | error | The comment says SSID broadcast prevents other devices from reaching the configuration or learning the MAC address; the point is the reverse: disabling the broa… | #50 → «Отключение широковещательной рассылки имени сети не мешает другим устройствам получить доступ к настройке точки доступа …» |
| final-exam | 41 | style | Typo «WAP2» and the mistranslation «предварительно открытый ключ» (pre-shared key) | #50 → «WPA2 Enterprise обеспечивает более надежную аутентификацию пользователей, чем WPA2 PSK. Вместо того, чтобы использовать …» |
| final-exam | 41 | unclear | Distractor «AAA» is defensible: the module says Enterprise mode requires a RADIUS server for AAA, and a RADIUS server is an AAA server | operator (kb#275) |
| final-exam | 44 | error | Matching item «маршруты, реализуемые администратором вручную» has match "0", which is not among the options (1-3), so it cannot be matched correctly. The unused… | operator (kb#275) |
| final-exam | 46 | style | Text follows the closing ``` on the same line, so the code block does not close; the bank copy puts a blank line there | #50 → «R1# ``` Посмотрите на пример.» |
| final-exam | 51 | style | The comment repeats its first sentence («5 в конце команды означает/обозначает административное расстояние...») — two merged translations | #50 → «» |
| final-exam | 51 | style | Typo «перходов» | #50 → «переходов» |
| final-exam | 52 | style | Routing table run into the stem with semicolons; the bank copy shows it as a code block, one route per line | #50 → «Таблица маршрутизации для R2 выглядит следующим образом: ``` Gateway of last resort is not set 10.0.0.0/30 is subnetted,…» |

## Findings: Bank copies (`__exams/CCNA2`)

The bank copies live in learn-ccna1 and have extra questions, so their numbering differs from the connected exams; twins were matched by content. 159 of their 242 findings mirror an exam finding above and get the same fix, with the same wording, in the paired learn-ccna1 PR; they are not repeated here. The table lists the 83 bank findings whose fix differs: the bank wording differs, or the problem exists only in the bank.

| File | Q | Sev | Issue | Fix |
|---|---|---|---|---|
| bank 01-04 | 12 | style | Bank-only: key says «трансляций портов» (port translations, a NAT term) for the MAC-to-port mapping of the CAM table. | learn-ccna1#120 → «MAC-адресов и соответствующих портов» |
| bank 01-04 | 16 | error | Bank-only: the stem says the steps are performed by a router («выполняемые маршрутизатором шаги»), but the question is about a switch. | learn-ccna1#120 → «выполняемые коммутатором шаги» |
| bank 01-04 | 28 | style | Bank-only: option «при разрешении по умолчанию» is garbled (a switchport mode is meant). | learn-ccna1#120 → «режим по умолчанию» |
| bank 01-04 | 34 | error | Marked answer lost its negation: it says G0/2 IS configured as a trunk, but the exhibit lists only Gig0/1 and the comment says G0/2 is not a trunk. (bank twin o… | learn-ccna1#120 → «Интерфейс G0/2 не настроен в качестве магистрального канала.» |
| bank 01-04 | 46 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». | learn-ccna1#120 → «Она автоматически настраивает порт таким образом» |
| bank 01-04 | 46 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». Same string in q46 answer 2 and q47 answer 1. | learn-ccna1#120 → «Она применяет IPv4 адрес к виртуальному интерфейсу.» |
| bank 01-04 | 46 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». Same string in q46 answer 3 and q47 answer 2. | learn-ccna1#120 → «Она применяет IPv6-адрес к виртуальному интерфейсу.» |
| bank 01-04 | 46 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». Same string in q46 answer 4 and q47 answer 4. | learn-ccna1#120 → «Она позволяет настроить IPv6-адрес на физическом интерфейсе коммутатора.» |
| bank 01-04 | 46 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». Same string in q46 answer 5 and q47 answer 5. | learn-ccna1#120 → «Она обновляет таблицу MAC-адресов для связанного порта.» |
| bank 01-04 | 47 | style | Bank-only: Gender agreement: the answer refers to «команда» (feminine) as «Он»; the connected twin uses «она». | learn-ccna1#120 → «Она активирует виртуальный или физический интерфейс коммутатора.» |
| bank 01-04 | 48 | style | Bank-only: wrong verb form «Она применяется IPv4 адрес» (reflexive verb with a direct object); same in q51 answer 2. | learn-ccna1#120 → «Она применяет» |
| bank 01-04 | 58 | style | Bank-only: «качества IP-телефона» (quality of the IP phone) for IP telephony quality. | learn-ccna1#120 → «качества IP-телефонии» |
| bank 01-04 | 62 | style | Bank-only: typo "HHTP" for HTTP (also in q63). | learn-ccna1#120 → «HTTP» |
| bank 05-06 | 15 | style | Stem asks «В каком из двух состояний» (which one) while two answers are correct (bank twin of 05-06-exam Q15) | learn-ccna1#120 → «В каких двух состояниях портов PVST+» |
| bank 05-06 | 35 | style | Bank-only: key «Это сделано путем объединения…» ("this is done by combining") does not answer "which statement describes EtherChannel" and drops "логическая". | learn-ccna1#120 → «Он представляет собой объединение нескольких физических связей, которые рассматриваются как одна логическая связь между …» |
| bank 05-06 | 53 | style | Bank-only: option uses «дублирование» instead of a port role. | learn-ccna1#120 → «назначенный, альтернативный, корневой, корневой» |
| bank 05-06 | 54 | style | Bank-only: missing word in «каждый канал коммутатора уровня будет агрегированным» (the layer number is lost). | learn-ccna1#120 → «коммутатора уровня 3 будет агрегированным» |
| bank 07-09 | 1 | style | Bank-only: missing space «принимаетIP-адрес». | learn-ccna1#120 → «клиент принимает IP-адрес» |
| bank 07-09 | 5 | style | Bank-only: garbled CLI «show running-config I section_dhcp» (letter I for the pipe, underscore). | learn-ccna1#120 → «show running-config \\| section dhcp» |
| bank 07-09 | 21 | style | Bank-only: option uses «лизинга» for the DHCP lease. | learn-ccna1#120 → «дождаться истечения срока аренды» |
| bank 07-09 | 25 | error | Bank-only: the stem asks how PC-A gets an IPv6 address from a DHCPv4 server; the exhibit and the key are about a DHCPv6 server. | learn-ccna1#120 → «получить IPv6-адрес от сервера DHCPv6» |
| bank 07-09 | 40 | style | Calque «непатентованный» ("not patented") for "nonproprietary"; the module calls these protocols open («открытый»). (bank twin of 07-09-exam q39) | learn-ccna1#120 → «является открытым протоколом выборов только для IPv4 с ограниченной» |
| bank 07-09 | 47 | style | Calque «непатентованный» ("not patented") for "nonproprietary"; the module calls these protocols open («открытый»). (bank twin of 07-09-exam q43; same stem in b… | learn-ccna1#120 → «является открытым протоколом выборов только для IPv4, который имеет» |
| bank 07-09 | 51 | style | Bank-only: numeral agreement «3 IP-адресов» (should be «3 IP-адреса»); same in q52. | learn-ccna1#120 → «резервирует 3 IP-адреса» |
| bank 10-13 | 0 | style | Bank only: typo «бузопасность» in the exam title (top-level field, not a question) | learn-ccna1#121 → «безопасность WLAN» |
| bank 10-13 | 6 | style | Bank only: «Какой оператор описывает» — «оператор» mistranslates «statement» (the connected copy has «утверждение») | learn-ccna1#121 → «Какое утверждение описывает поведение коммутатора при переполнении таблицы MAC-адресов?» |
| bank 10-13 | 12 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «switchport port-security aging.» |
| bank 10-13 | 14 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «switchport port-security violation.» |
| bank 10-13 | 15 | style | Bank options mix Russian words («выкл», «ограничение», «защита») with the CLI keyword «shutdown»; the connected copy and the module (11.01 README:236-247) use t… | learn-ccna1#121 → «"answer": "disabled"» |
| bank 10-13 | 15 | style | Bank option in Russian next to CLI keywords; aligned with the connected copy (see the «выкл» row) | learn-ccna1#121 → «"answer": "restrict"» |
| bank 10-13 | 15 | style | Bank key in Russian next to CLI keywords; aligned with the connected copy (see the «выкл» row) | learn-ccna1#121 → «"answer": "protect"» |
| bank 10-13 | 21 | style | Bank only: command not formatted and a stray space before the full stop (the connected copy uses `...`) | learn-ccna1#121 → «команды `ip arp inspection validate src-mac`. Зачем» |
| bank 10-13 | 29 | style | Bank only: «режим ..., требуемый сервером RADIUS» inverts the sense (the mode requires a RADIUS server, not the other way round) | learn-ccna1#121 → «использующий сервер RADIUS» |
| bank 10-13 | 36 | style | Bank only (question not in the connected exam): typo «Вредоносные токи» for «Вредоносные точки доступа» (rogue APs) | learn-ccna1#121 → «Вредоносные точки доступа» |
| bank 10-13 | 36 | style | Bank only: the key «Продвинутый уровень» does not match the button named in the comment («кнопку Дополнительно») or in the lecture («Advanced (дополнительно)»);… | learn-ccna1#121 → «Нажав кнопку Дополнительно, пользователь получит доступ к странице расширенной сводки и ко всем функциям WLC.» |
| bank 10-13 | 36 | style | Bank only: key label «Продвинутый уровень» → the button name used by the lecture | learn-ccna1#121 → «Дополнительно» |
| bank 10-13 | 37 | style | Bank only (question not in the connected exam): MT artefact «ИНФОРМАЦИОННАЯ БЕЗОПАСНОСТЬ» for the SECURITY tab | learn-ccna1#121 → «БЕЗОПАСНОСТЬ» |
| bank 10-13 | 41 | style | Bank only (question not in the connected exam): garbled option «Доступный сервер SNMP или создание сервера SNMP.» | learn-ccna1#121 → «Создайте сервер SNMP или убедитесь, что он доступен.» |
| bank 10-13 | 41 | style | Bank only: garbled option «Доступный сервер RADIUS или создание сервера RADIUS.» | learn-ccna1#121 → «Создайте сервер RADIUS или убедитесь, что он доступен.» |
| bank 10-13 | 42 | style | Bank only: nonsense «не требует помех» (the connected copy: «не подвержена помехам») | learn-ccna1#121 → «скорее всего, не подвержена помехам.» |
| bank 10-13 | 44 | style | Bank only (question not in the connected exam): «позволяет пользователям аутентифицировать» — the verb lacks its object; users pass authentication | learn-ccna1#121 → «Он позволяет пользователям пройти аутентификацию и получить доступ к WLAN.» |
| bank 10-13 | 45 | error | Nonsense distractor «прейскурант» (price list) — a mistranslation of the network medium; the comment explains the medium (bank twin of 10-13-exam Q41, where the… | learn-ccna1#121 → «Убедитесь, что выбрана правильная среда передачи.» |
| bank 10-13 | 52 | style | Garbled stem with no predicate: «...или протокол управления доступом, которым разрешен доступ к сети?» (bank twin of 10-13-exam Q48) | learn-ccna1#121 → «Какой компонент, механизм или протокол контроля доступа определяет, кому разрешен доступ к сети?» |
| bank 14-16 | 6 | style | Bank only: «Какая характеристика статического маршрута соответствует всем пакетам?» says the characteristic matches packets (the connected copy: «Какая характер… | learn-ccna1#121 → «Какая характеристика описывает статический маршрут, который соответствует всем пакетам?» |
| bank 14-16 | 6 | style | Bank only: «для отправки нескольких статических маршрутов по одному адресу назначения» — routes are not sent; the option describes a summary route | learn-ccna1#121 → «Использует один сетевой адрес для сопоставления нескольких статических маршрутов одному адресу назначения.» |
| bank 14-16 | 14 | style | Bank only: commands not formatted, stray spaces before «.» and «,» | learn-ccna1#121 → «с помощью команды `ip address 172.16.1.254 255.255.255.0`. Однако когда администратор вводит команду `show ip route`, в …» |
| bank 14-16 | 19 | error | Garbled option «полностью статический маршрут» that duplicates answer 4 in substance; the source option is a plain static route via Fa0/0 with AD 1 (bank twin o… | learn-ccna1#121 → «Создайте статический маршрут к Fa0/0 с административным расстоянием 1.» |
| bank 14-16 | 23 | style | Bank only: invalid mask «255.255.0» in the command (the connected copy and Q22/Q24 have 255.255.255.0) | learn-ccna1#121 → «ip route 192.168.10.0 255.255.255.0 10.10.10.2 5» |
| bank 14-16 | 35 | style | Bank only: mixed script «cервера» (Latin c) | learn-ccna1#121 → «сервера» |
| bank 14-16 | 38 | style | Typo in the command: mask «0.0.0» has three octets; the command is also not formatted (bank twin of 14-16-exam Q38) | learn-ccna1#121 → «Команда плавающего статического маршрута `ip route 0.0.0.0 0.0.0.0 S0/1/1 100` была» |
| bank 14-16 | 38 | style | Bank only: «чтобы трафик использовал канал OSPF только после его запуска» garbles the source («when it is up»); the connected copy ends «...использовал канал OS… | learn-ccna1#121 → «чтобы трафик использовал канал OSPF?» |
| bank 14-16 | 39 | style | Calque «Какая структура завершает следующее утверждение?» in the stems of Q39-Q48 (bank twins of 14-16-exam Q39-Q42 and their bank-only variants) | learn-ccna1#121 → «Какой вариант завершает следующее утверждение?» |
| bank 14-16 | 51 | style | Bank only: missing full stop «Посмотрите на пример Какой интерфейс» | learn-ccna1#121 → «Посмотрите на пример. Какой» |
| bank 14-16 | 54 | style | Bank only: malformed address «L 0.3.86.193/27» (leading 1 lost) | learn-ccna1#121 → «L 10.3.86.193/27» |
| bank 14-16 | 55 | error | Bank only: wrong key. 172.18.109.152 matches no route in the exhibit and there is no gateway of last resort, so the packet is dropped (answer 4); the bank marks… | learn-ccna1#121 key → answer 4 |
| bank 14-16 | 49–58 | style | Garbled word order «имеет назначение IP-адрес» (stems of bank Q49–Q58); the connected copy says «IP-адрес назначения» | learn-ccna1#121 → «имеет IP-адрес назначения» |
| bank Practice Final | 1 | style | Bank only: command garbled by spacing «BranchSw (config) #interface VLAN88 ?» | learn-ccna1#121 → «команды `BranchSw(config)# interface VLAN88`?» |
| bank Practice Final | 9 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «switchport nonegotiate.» |
| bank Practice Final | 10 | style | Bank only: typo «HHTP» for HTTP | learn-ccna1#121 → «HTTP» |
| bank Practice Final | 14 | style | Bank only: garbled option «порт на двух коммутаторах портов FastEthernet» (the connected copy: «режимы портов FastEthernet на коммутаторе») | learn-ccna1#121 → «режимы портов FastEthernet на коммутаторе» |
| bank Practice Final | 22 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «команда ip helper-address.» |
| bank Practice Final | 24 | style | Bank only: DHCPACK described as «определения успешности аренды»; it confirms the lease (the connected copy: «подтверждения») | learn-ccna1#121 → «сообщение, используемое для подтверждения успешности аренды» |
| bank Practice Final | 25 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «managed-config-flag. Как» |
| bank Practice Final | 28 | error | Bank only: without the load-balancing requirement HSRP and VRRP satisfy the stem equally well, so the key GLBP is not the only defensible answer; the connected … | learn-ccna1#121 → «чтобы повысить доступность сетевых ресурсов и обеспечить распределение нагрузки между маршрутизаторами. Какой протокол» |
| bank Practice Final | 32 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «команды switchport mode trunk.» |
| bank Practice Final | 32 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «команды switchport mode access.» |
| bank Practice Final | 32 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «команды no shutdown.» |
| bank Practice Final | 33 | style | Bank only: stray space before the full stop after the command | learn-ccna1#121 → «командой no shutdown.» |
| bank Practice Final | 34 | error | Bank only: the stem of Q32 (port security rejected) was copied onto this question; the exhibit (10.png) and the options are about three ip arp inspection valida… | learn-ccna1#121 → «![](./assert/10.png) Посмотрите на изображение. К какому результату приведет применение данной последовательности команд…» |
| bank Practice Final | 34 | style | Bank only: the second sentence has no verb («Если один набор параметров действителен, разрешение передачи пакета ARP.») | learn-ccna1#121 → «Если хотя бы один параметр действителен, то пакет ARP может быть передан.» |
| bank Practice Final | 36 | style | Distractor names ISL, a vendor-proprietary trunking encapsulation the course never mentions; a standard encapsulation keeps the option wrong (bank twin of final… | learn-ccna1#121 → «Использовать инкапсуляцию 802.1Q на всех магистральных каналах.» |
| bank Practice Final | 37 | style | Bank only: broken syntax «Какие два метода можно использовать беспроводной сетевой адаптер» | learn-ccna1#121 → «Какие два метода может использовать беспроводной сетевой адаптер» |
| bank Practice Final | 46 | error | Bank only: wrong key. 172.18.109.152 matches no route and there is no gateway of last resort, so the packet is dropped (answer 4); the bank marks Serial0/0/0. T… | learn-ccna1#121 key → answer 4 |
| bank Practice Final | 46 | style | Garbled word order «имеет назначение IP-адрес»; the connected copy says «IP-адрес назначения» | learn-ccna1#121 → «имеет IP-адрес назначения» |
| bank Practice Final | 47 | style | Bank only: missing space «CEF?(Выберите» | learn-ccna1#121 → «CEF? (Выберите» |
| bank Practice Final | 48 | style | Bank only: «показатель» for metric; the module and the connected copy say «метрика» | learn-ccna1#121 → «"answer": "метрика"» |
| bank Practice Final | 49 | error | Bank only: wrong key. The options were reordered but the key stayed on answer 1 («Добавить адрес следующего перехода 192.168.0.36.»); the fix is to raise the AD… | learn-ccna1#121 key → answer 4 |
| bank Practice Final | 49 | style | Bank only: stray space before the comma after the command | learn-ccna1#121 → «S0/0/1 100, и» |
| bank Practice Final | 50 | error | Bank only: wrong key. Answer 1 «ipv6 route ::/0 fe80::1» is invalid (a link-local next hop needs an exit interface, as the comment says); the valid default rout… | learn-ccna1#121 key → answer 3 |
| bank Practice Final | 51 | error | Bank only: wrong key. The trailing 5 is the administrative distance (answer 3), not the metric (answer 1, keyed), as the comment explains. Comments then need mo… | learn-ccna1#121 key → answer 3 |
| bank Practice Final | 51 | style | Bank only: invalid mask «255.255.0» in the command | learn-ccna1#121 → «ip route 192.168.10.0 255.255.255.0 10.10.10.2 5» |
| bank Practice Final | 52 | error | Bank only: wrong key. 192.168.10.129 matches S 192.168.10.128 via 10.0.0.6, which is reached through Serial0/0/1 (answer 3), as the comment explains; the bank k… | learn-ccna1#121 key → answer 3 |
| bank Practice Final | 54 | error | Bank only: wrong key. The exhibit shows «S 2001:DB8:CAFE:4::1/128 [1/0]», a static route entered by the administrator (answer 3), not a local route created auto… | learn-ccna1#121 key → answer 3 |

## Course text found on the way

Errors in the lecture text that the review ran into. None of them is changed by the quiz PRs, because the lectures are outside kb#275. They go to the operator with the doubtful items.

| Lecture | Problem |
|---|---|
| `01-basic-device-configuration/01.01-configure-a-switch-with-initial-settings/README.md:54` | «Если индикатор горит зеленым цветом, вентиляторы работают нормально» under the system LED; green means the system works normally. The quiz fix in 01.06.04 q2 does not depend on this sentence |
| `03-vlans/03.02-vlans-in-a-multi-switched-environment/README.md:47` | 802.1Q user priority «поддерживает реализацию уровня или сервиса», a garble of "level of service"; 01-04-exam Q27 repeats it and waits for this line |
| `10-lan-security-concepts/10.03-layer-2-security-threats/README.md:38` | «САМ таблицы» typed in Cyrillic letters; it should be Latin CAM |
| `10-lan-security-concepts/10.05-lan-attacks/README.md:46` | «к порту, находящимся» (should be «находящемуся»), and «транкового порта», a variant the glossary forbids |
| `11-switch-security-configuration/11.01-implement-port-security/README.md:99` | «значение безопасности порта по умолчанию равно 1» is clumsy; «максимальное число MAC-адресов по умолчанию» is meant (noted by kb's review of learn-ccna2#44) |
| `11-switch-security-configuration/11.04-mitigate-arp-attacks/README.md:53` | each new `ip arp inspection validate` command «просматривает предыдущую»; it replaces the previous one. The exam comments are fixed in learn-ccna2#50 |
| `12-wlan-concepts/12.04-capwap-operation/README.md:13` | CAPWAP called «стандартный протокол IEEE»; it is an IETF standard (RFC 5415). 10-13-exam Q68 repeats it and waits for this line |

Two vendor items in the lecture text are known and planned, not new: CEF is still taught in 14.02 (de-marketing item 2.5, which also lists 14.02.04 q3 and 14.06.02 q6), and CDP still appears in 03.02, 10.05, 10.06, 13.02 and 16.02 next to LLDP.

## Follow-ups

- **Images:** bank 01-04 Q25 and Q45 point to `assert/4.png` and `assert/15.png`, while the files are `4.PNG` and `15.PNG`. Image paths are out of scope, so they are logged in learn-ccna1#120's `audit/figma-followups/` file.
- **Packet Tracer items:** five bank questions are `.pka` activities (01-04 Q73, 05-06 Q56, 07-09 Q63, 10-13 Q75, 14-16 Q64). Files with `.pka` are out of scope, so the questions stay until the lab rework.
- **Structural fixes:** final-exam Q44 and its bank twin (a matching item with no option), bank 07-09 Q32 (an empty matching question), bank 10-13 Q67 and bank 14-16 Q12 (placeholder items) and bank 14-16 Q56 (no correct option) need changes to the JSON structure, which kb#275 does not make. They are on the operator list.
- **Term alignment:** existing «роутер», «хост» and «транк» are left to the kb#276 alignment PRs, which start after this course's kb#275 PRs are merged.
