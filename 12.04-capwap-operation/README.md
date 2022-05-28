<!-- 12.4.1 -->
## Видео: CAPWAP

В предыдущей теме вы узнали о принципах работы WLAN. Теперь мы расскажем о протоколе CAPWAP (Control And Provisioning of Wireless Access Points — управление и инициализация беспроводных точек доступа).

Нажмите «Воспроизвести», чтобы просмотреть видео о протоколе «Управление и обеспечение точек беспроводного доступа» (CAPWAP).

![youtube](https://www.youtube.com/watch?v=qXXGwkLZ6hI)

<!-- 12.4.2 -->
## Введение в CAPWAP

CAPWAP - это стандартный протокол IEEE, который позволяет WLC управлять несколькими точками доступа и WLAN. CAPWAP также отвечает за инкапсуляцию и пересылку клиентского трафика WLAN между AP и WLC.

CAPWAP основан на LWAPP, но добавляет дополнительную безопасность с защитой транспортного уровня дейтаграмм (DTLS). CAPWAP устанавливает туннели на портах протокола пользовательских дейтаграмм (UDP). CAPWAP может работать как по IPv4, так и по IPv6, как показано на рисунке, но по умолчанию использует IPv4.

IPv4 и IPv6 могут использовать UDP-порты 5246 и 5247. Однако, туннели CAPWAP используют разные IP-протоколы в заголовке кадра. IPv4 использует IP-протокол 17, а IPv6 использует IP-протокол 136.

![](./assets/12.4.2.png)
<!-- /courses/srwe-dl/af9ecea0-34fe-11eb-b1b2-9b1b0c1f7e0d/afb75fa8-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/ca853052-1c27-11ea-af09-3b2e6521927c.svg -->

<!-- 12.4.3 -->
## Разделенная MAC-архитектура

Ключевым компонентом CAPWAP является концепция раздельного управления доступом к среде (MAC). Концепция CAPWAP split MAC выполняет все функции, обычно выполняемые отдельными AP, и распределяет их между двумя функциональными компонентами:

* AP MAC Функции
* Функции WLC MAC

В таблице показаны некоторые функции MAC, выполняемые каждым из них.

| **AP MAC Функции** | **Функции WLC MAC** |
| --- | --- |
| Маяки и ответы от зондов | Аутентификация |
| Подтверждение пакетов и повторная передача | Объединение и повторное объединение роуминговых клиентов |
| Очередь кадров и расстановка приоритетов пакетов | Перевод кадра в другие протоколы |
| Шифрование и дешифрование данных на уровне MAC | Завершение трафика 802.11 на проводном интерфейсе |

<!-- 12.4.4 -->
## Шифрование DTLS

DTLS - это протокол, который обеспечивает безопасность между AP и WLC. Это позволяет им общаться с использованием шифрования и предотвращает подслушивание или вмешательство.

DTLS включен по умолчанию для защиты канала управления CAPWAP, но по умолчанию отключен для канала данных, как показано на рисунке. Весь трафик управления и контроля CAPWAP, которым обмениваются точка доступа и WLC, по умолчанию зашифрован и защищен для обеспечения конфиденциальности плоскости управления и предотвращения атак MITM.

Шифрование данных CAPWAP является необязательным и включено для каждой точки доступа. Шифрование данных требует, чтобы лицензия DTLS была установлена на WLC прежде, чем быть включенной на AP. Когда включено, весь трафик клиента WLAN шифруется в AP прежде, чем быть переданным к WLC и наоборот.

![](./assets/12.4.4.png)
<!-- /courses/srwe-dl/af9ecea0-34fe-11eb-b1b2-9b1b0c1f7e0d/afb75fa8-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/ca861ab0-1c27-11ea-af09-3b2e6521927c.svg -->

<!-- 12.4.5 -->
## FlexConnect AP

FlexConnect - это беспроводное решение для развертывания филиалов и удаленных офисов. Он позволяет настраивать и контролировать точки доступа в филиале из корпоративного офиса через канал WAN без развертывания контроллера в каждом офисе.

Для точки доступа FlexConnect существует два режима работы.

* **Connected mode (Подключенный режим)** - WLC достижим. В этом режиме точка доступа FlexConnect имеет соединение CAPWAP со своим WLC и может отправлять трафик через туннель CAPWAP, как показано на рисунке. WLC выполняет все свои функции CAPWAP.
* **Standalone mode (Автономный режим)** - WLC недоступен. FlexConnect потерял или не смог установить соединение CAPWAP со своим WLC. В этом режиме точка доступа FlexConnect может выполнять некоторые функции WLC, такие как локальное переключение трафика данных клиента и локальная аутентификация клиента.

![](./assets/12.4.5.png)
<!-- /courses/srwe-dl/af9ecea0-34fe-11eb-b1b2-9b1b0c1f7e0d/afb75fa8-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/ca868fe1-1c27-11ea-af09-3b2e6521927c.svg -->

<!-- 12.4.6 -->
<!-- quiz -->