<!-- 11.1.1 -->
## Защита неиспользуемых портов

Устройства уровня 2 считаются самым слабым звеном в инфраструктуре безопасности компании. Атаки 2-го уровня являются одними из самых простых для развертывания хакерами, но эти угрозы также можно нейтрализовать с помощью некоторых распространенных решений 2-го уровня.

Перед введением коммутатора в эксплуатацию необходимо обеспечить безопасность всех портов (интерфейсов) коммутатора. Как порт будет защищен, зависит от его функции.

Отключение неиспользуемых портов — это простой способ защиты сети от несанкционированного доступа, используемый многими администраторами. К примеру, если коммутатор Catalyst 2960 имеет 24 порта и при этом используются три подключения Fast Ethernet, рекомендуется отключить 21 неиспользуемый порт. Перейдите к каждому неиспользуемому порту и выполните команду выключения Cisco IOS **shutdown**. Если порт необходимо активировать позднее, его можно включить с помощью команды **no shutdown**.

Чтобы настроить для целого диапазона портов, используйте команду **interface range**.

```
Switch(config)# interface range type module/first-number – last-number 
```

Например, чтобы отключить порты для Fa0 / 8 через Fa0 / 24 на S1, вы должны ввести следующую команду.

```
S1(config)# interface range fa0/8 - 24
S1(config-if-range)# shutdown
%LINK-5-CHANGED: Interface FastEthernet0/8, changed state to administratively down
(output omitted)
%LINK-5-CHANGED: Interface FastEthernet0/24, changed state to administratively down
S1(config-if-range)#
```

<!-- 11.1.2 -->
## Нейтрализация атак таблицы MAC-адресов

Самый простой и эффективный метод предотвращения атак переполнения таблицы MAC-адресов — это обеспечение безопасности порта.

Данная функция ограничивает количество допустимых МАС-адресов на один порт, а также это позволяет администратору вручную настраивать MAC-адреса для порта или разрешать коммутатору динамически изучать ограниченное количество MAC-адресов. Когда порт, сконфигурированный с защитой порта, получает кадр, MAC-адрес источника кадра сравнивается со списком MAC-адресов защищенного источника, которые были настроены или динамически изучены на порту.

Ограничив число разрешенных MAC-адресов на порту одним адресом, можно использовать средства безопасности портов для контроля несанкционированного расширения сети, как показано на рисунке.

![](./assets/11.1.2.png)
<!-- /courses/srwe-dl/af9ece9e-34fe-11eb-b1b2-9b1b0c1f7e0d/afb71186-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/ca5c2482-1c27-11ea-af09-3b2e6521927c.svg -->

**Примечание**: MAC-адреса показаны как 24-х битные для простоты.

<!-- 11.1.3 -->
## Включите защиту портов

Обратите внимание, что в примере команда **switchport port-security** была отклонена. Это связано с тем, что безопасность портов можно настроить только на настроенных вручную портах доступа или настроенных вручную магистральных портах. По умолчанию порты коммутатора уровня 2 настроены на динамический автоматический режим (транкинг включен). Поэтому в примере порт настраивается с помощью команды настройки интерфейса **switchport mode access**.

**Примечание**: Безопасность магистрального порта выходит за рамки данного курса.

```
S1(config)# interface f0/1
S1(config-if)# switchport port-security
Command rejected: FastEthernet0/1 is a dynamic port.
S1(config-if)# switchport mode access
S1(config-if)# switchport port-security
S1(config-if)# end
S1#
```

Используйте команду **show port-security interface** для отображения текущих настроек безопасности порта для FastEthernet 0/1, как показано в примере. Обратите внимание на то, как включена защита порта, режим нарушения (violation mode) отключен, и максимальное количество MAC-адресов равно 1. Если устройство подключено к порту, коммутатор автоматически добавит MAC-адрес устройства в качестве защищенного MAC-адреса. В этом примере ни одно устройство не подключено к порту.

```
S1# show port-security interface f0/1
Port Security              : Enabled
Port Status                : Secure-down
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 1
Total MAC Addresses        : 0
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 0
Last Source Address:Vlan   : 0000.0000.0000:0
Security Violation Count   : 0
S1#
```

**Примечание**: Если активный порт настроен с помощью команды **switchport port-security** и к этому порту подключено более одного устройства, порт перейдет в состояние error-disabled. Это условие обсуждается позже в этой теме.

После включения защиты порта можно настроить другие особенности безопасности порта, как показано в примере.

```
S1(config-if)# switchport port-security ?
  aging        Port-security aging commands
  mac-address  Secure mac address
  maximum      Max secure addresses
  violation    Security violation mode  
S1(config-if)# switchport port-security
```

<!-- 11.1.4 -->
## Ограничение и изучение MAC-адресов

Для определения максимального числа MAC адресов, разрешенных для конкретного порта, используем следующую команду:

```
Switch(config-if)# switchport port-security maximum value 
```

Значение безопасности порта по умолчанию равно 1. Максимальное количество защищенных MAC-адресов, которые можно настроить, зависит от коммутатора и IOS. В этом примере максимум составляет 8192.

```
S1(config)# interface f0/1
S1(config-if)# switchport port-security maximum ? 
  <1-8192>  Maximum addresses
S1(config-if)# switchport port-security maximum
```

Коммутатор может быть настроен на изучение MAC-адресов на защищенном порту одним из трех способов:

**1\. Вручную**

Администратор вручную настраивает статический MAC-адрес (а) с помощью следующей команды для каждого безопасного MAC-адреса в порту:

```
Switch(config-if)# switchport port-security mac-address mac-address 
```

**2\. Динамически изученный**

Когда вводится команда **switchport port-security**, текущий MAC-адрес источника для устройства, подключенного к порту, автоматически защищается, но не добавляется в конфигурацию запуска. Если коммутатор перезагружен, порт должен будет повторно узнать MAC-адрес устройства.

**3\. Динамически изученный sticky MAC адрес**

Администратор может включить коммутатор для динамического изучения MAC-адреса и «привязать» их к работающей конфигурации с помощью следующей команды:

```
Switch(config-if)# switchport port-security mac-address sticky 
```

Сохранение текущей конфигурации передаст динамически изученный MAC-адрес в NVRAM.

В следующем примере демонстрируется полная конфигурация безопасности порта для FastEthernet 0/1. Администратор указывает максимум 2 MAC-адреса, вручную настраивает один безопасный MAC-адрес, а затем настраивает порт для динамического изучения дополнительных защищенных MAC-адресов до максимум 2 защищенных MAC-адресов. Используйте команды **show port-security interface** и **show port-security address** для проверки конфигурации.

```
*Mar  1 00:12:38.179: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to up
*Mar  1 00:12:39.194: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to up
S1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
S1(config)#
S1(config)# interface fa0/1
S1(config-if)# switchport mode access
S1(config-if)# switchport port-security
S1(config-if)# switchport port-security maximum 2
S1(config-if)# switchport port-security mac-address aaaa.bbbb.1234
S1(config-if)# switchport port-security mac-address sticky 
S1(config-if)# end
S1# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
S1# show port-security address
               Secure Mac Address Table
-----------------------------------------------------------------------------
Vlan    Mac Address       Type                          Ports   Remaining Age
                                                                   (mins)    
----    -----------       ----                          -----   -------------
1    a41f.7272.676a    SecureSticky                  Fa0/1        -
1    aaaa.bbbb.1234    SecureConfigured              Fa0/1        -
-----------------------------------------------------------------------------
Total Addresses in System (excluding one mac per port)     : 1
Max  Addresses limit in System (excluding one mac per port) : 8192
S1#
```

Вывод команды **show port-security interface** проверяет, включена ли функция port security, существует ли хост, подключенный к порту (т.е., Secure-up), всем двум MAC адресам будет разрешено подключиться, и S1 выучил один MAC адрес статически и один MAC адрес динамически (т.е., sticky).

Вывод команды **show port-security address** перечисляет два выученных MAC адреса.

<!-- 11.1.5 -->
## Устаревание безопасности порта

Устаревание безопасности порта может использоваться для установки времени устаревания статических и динамических защищенных адресов на порту. Для каждого порта поддерживается два типа старения:

- **Абсолютный** - Защищенные адреса порта удаляются по истечении указанного времени устаревания.
- **По таймеру неактивности** - безопасные адреса на порту удаляются, только если они неактивны в течение указанного времени.

Используйте устаревание для удаления защищенных MAC-адресов на защищенном порту без удаления существующих безопасных MAC-адресов вручную. Ограничения по времени старения также могут быть увеличены, чтобы гарантировать сохранение прежних, безопасных MAC-адресов, даже при добавлении новых MAC-адресов. Устаревание статически настроенных безопасных адресов может быть включено или отключено для каждого порта отдельно.

Используйте команду **switchport port-security aging**, чтобы включить или отключить статическое устаревание для защищенного порта или установить время или тип устаревания.

```
Switch(config-if)# switchport port-security aging {static | time time | тип {absolute | inactivity}}
```

Параметры для команды описаны в таблице приведённой ниже

| **Параметр**  | **Описание**  |
| --- | --- |
| `static` | Включение устаревания для статически настроенных безопасных адресов на порту. |
| `time time ` | Определяет время устаревания для порта. Диапазон составляет от 0 до 1440 минут. Если время равно 0, устаревание для этого порта отключено. |
| `type absolute` | Устанавливает абсолютное время устаревания. Срок действия всех защищенных адресов на этом порту истекает точно по истечении указанного времени (в минутах) и удаляется из списка защищенных адресов. |
| `type inactivity` | Устанавливает устаревание адресов по неактивности. Защищенные адреса на этом порту устаревают, только если в течение указанного периода времени отсутствует трафик с адреса защищенного источника. |

**Примечание**: MAC-адреса показаны как 24-х битные для простоты.

В этом примере показано, как администратор настраивает тип устаревания на 10 минут бездействия и использует команду **show port-security interface** для проверки конфигурации

```
S1(config)# interface fa0/1
S1(config-if)# switchport port-security aging time 10 
S1(config-if)# switchport port-security aging type inactivity 
S1(config-if)# end
S1# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
S1#
```

<!-- 11.1.6 -->
## Режимы нарушения безопасности порта

Если MAC-адрес устройства, подключенного к порту, отличается от списка защищенных адресов, происходит нарушение (violation) порта. По умолчанию порт переходит в состояние отключения по ошибке (error-disabled).

Чтобы установить режим нарушения безопасности порта, используйте следующую команду:

```
Switch(config-if)# switchport port-security violation {protect | restrict | shutdown} 
```

В следующих таблицах показано, как коммутатор реагирует в зависимости от настроенного режима нарушения.

**Описание режимов Security Violation**

| Режим | Описание |
| --- | --- |
| `shutdown` (default) | Порт сразу переходит в состояние отключения по ошибке, отключается, гаснет светодиод порта и отправляет сообщение системного журнала. Увеличивает счетчик нарушений нарушений Когда защищенный порт находится в состоянии отключения по ошибке, администратор должен повторно включить его, используя команы **shutdown** и **no shutdown** . |
| `restrict` (ограничение) | Порт отбрасывает пакеты с неизвестными адресами источника MAC, пока вы не удалите достаточное количество защищенных адресов MAC, чтобы опуститься ниже максимального значения или увеличить максимальное значение. Этот режим вызывает увеличение счетчика нарушений безопасности и генерирует сообщение системного журнала (syslog). |
| `protect` (защита) | Это наименее безопасный из режимов нарушения безопасности. Порт отбрасывает Порт отбрасывает пакеты с неизвестными адресами источника MAC, пока вы не удалите достаточное количество защищенных адресов MAC, чтобы опуститься ниже максимального значения или увеличить максимальное значение. Нет сообщений системного журнала (syslog). |

**Сравнение режимов Security Violation**

| Режим нарушения безопасности | Отбрасывает нежелательный трафик | Передаёт сообщение SYSLOG | Увеличивает счетчик нарушений | Выключает порт |
| --- | --- | --- | --- | --- |
| Protect (Защита) | Да | Нет | Нет | Нет |
| Restrict (Ограничение) | Да | Да | Да | Нет |
| Shutdown (Выключение) | Да | Да | Да | Да |

В следующем примере показано, как администратор изменил нарушение безопасности на «restrict». Выходные данные команды **show port-security interface** подтверждают, что изменение было внесено.

```
S1(config)# interface f0/1
S1(config-if)# switchport port-security violation restrict
S1(config-if)# end
S1#
S1# show port-security interface f0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Restrict
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
S1#
```

<!-- 11.1.7 -->
## Порт в состоянии error-disabled

Когда порт отключен и переведен в состояние error-disabled, трафик на этот порт не отправляется и не принимается. На консоли отображается ряд сообщений, связанных с безопасностью портов, как показано в следующем примере.

```
S1(config)# int fa0/1
S1(config-if)# switchport port-security violation shutdown
S1(config-if)# end
S1#
*Mar  1 00:24:15.599: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to down
*Mar  1 00:24:16.606: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to down
*Mar  1 00:24:19.114: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to up
*Mar  1 00:24:20.121: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to up
S1#
*Mar  1 00:24:32.829: %PM-4-ERR_DISABLE: psecure-violation error detected on Fa0/1, putting Fa0/1 in err-disable state
*Mar  1 00:24:32.838: %PORT_SECURITY-2-PSECURE_VIOLATION: Security violation occurred, caused by MAC address a41f.7273.018c on port FastEthernet0/1.
*Mar  1 00:24:33.836: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to down
*Mar  1 00:24:34.843: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to down
S1#
```

**Примечание**: Протокол порта и состояние соединения изменяются на «down», а индикатор порта гаснет.

В этом примере команда **show interface** определяет состояние порта как **err-disabled**. Выходные данные команды **show port-security interface** теперь показывают состояние порта как **secure-shutdown**. Счетчик нарушений безопасности увеличивается на 1.

```
S1# show interface fa0/1 | include down
FastEthernet0/18 is down, line protocol is down (err-disabled)
(output omitted)
S1# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7273.018c:1
Security Violation Count   : 1
S1#
```

Администратор должен определить причину нарушения безопасности. Если к безопасному порту подключено неавторизованное устройство, угроза безопасности устраняется до повторного включения порта.

Чтобы повторно включить порт, сначала используйте команду **shutdown**, затем используйте команду **no shutdown**, чтобы сделать порт работоспособным, как показано в примере.

```
S1(config)# interface fa0/1
S1(config-if)# shutdown
S1(config-if)#
*Mar  1 00:39:54.981: %LINK-5-CHANGED: Interface FastEthernet0/1, changed state to administratively down
S1(config-if)# no shutdown
S1(config-if)#
*Mar  1 00:40:04.275: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to up
*Mar  1 00:40:05.282: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to up
S1(config-if)#
```

<!-- 11.1.8 -->
## Проверка функции безопасности портов

После настройки функции безопасности портов на коммутаторе проверьте каждый интерфейс, чтобы убедиться в правильности настройки этой функции и статических МАС-адресов.

**Безопасность порта для всех интерфейсов**

Чтобы отобразить параметры безопасности порта для коммутатора, используйте команду **show port-security**. В примере показано, что все 24 интерфейса настроены с помощью команды **switchport port-security**, поскольку максимально допустимое значение равно 1, а режим нарушения отключен. Устройства не подключены. Следовательно, CurrentAddr (Count) равен 0 для каждого интерфейса.

```
S1# show port-security
Secure Port  MaxSecureAddr  CurrentAddr  SecurityViolation  Security Action
                (Count)       (Count)          (Count)
---------------------------------------------------------------------------
      Fa0/1              2            2                  0         Shutdown
---------------------------------------------------------------------------
Total Addresses in System (excluding one mac per port)     : 1
Max Addresses limit in System (excluding one mac per port) : 8192
S1#
```

**Безопасность порта для определенного интерфейса**

Используйте команду **show port-security interface** для просмотра сведений об определенном интерфейсе, как показано ранее и в этом примере.

```
S1# show port-security interface fastethernet 0/1
Port Security          	    : Enabled
Port Status            	    : Secure-up
Violation Mode              : Shutdown
Aging Time                  : 10 mins
Aging Type                  : Inactivity
SecureStatic Address Aging  : Disabled
Maximum MAC Addresses       : 2
Total MAC Addresses         : 2
Configured MAC Addresses    : 1
Sticky MAC Addresses        : 1
Last Source Address:Vlan    : a41f.7273.018c:1
Security Violation Count    : 0
S1#
```

**Проверка изученных MAC-адресов**

Чтобы убедиться, что MAC-адреса «прилипают» к конфигурации, используйте команду **show run**, как показано в примере для FastEthernet 0/19.

```
S1# show run interface fa0/1
Building configuration...

Current configuration : 365 bytes
!
interface FastEthernet0/1
 switchport mode access
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security mac-address sticky a41f.7272.676a
 switchport port-security mac-address aaaa.bbbb.1234
 switchport port-security aging time 10
 switchport port-security aging type inactivity
 switchport port-security
end

S1#
```

**Проверка защиты MAC-адресов**

Чтобы отобразить все защищенные MAC-адреса, которые настроены вручную или динамически запоминаются на всех интерфейсах коммутатора, используйте команду **show port-security address**, как показано в примере.

```
S1# show port-security address
               Secure Mac Address Table
-----------------------------------------------------------------------------
Vlan    Mac Address       Type                          Ports   Remaining Age
                                                                   (mins)
----    -----------       ----                          -----   -------------
   1    a41f.7272.676a    SecureSticky                  Fa0/1        -
   1    aaaa.bbbb.1234    SecureConfigured              Fa0/1        -
-----------------------------------------------------------------------------
Total Addresses in System (excluding one mac per port)     : 1
Max Addresses limit in System (excluding one mac per port) : 8192
S1#
```

<!-- 11.1.9 -->
<!-- syntax -->

<!-- 11.1.10 -->
## Работа в симуляторе: реализация безопасности порта

В рамках этого задания вам предстоит настроить и проверить функцию безопасности порта на коммутаторе. Функция безопасности порта позволяет ограничить входящий трафик порта за счёт ограничения числа MAC-адресов, которые могут посылать трафик через этот порт.

[Реализация безопасности порта (pdf)](./assets/11.1.10-packet-tracer---implement-port-security_ru-RU.pdf)

[Реализация безопасности порта (pka)](./assets/11.1.10-packet-tracer---implement-port-security_ru-RU.pka)
