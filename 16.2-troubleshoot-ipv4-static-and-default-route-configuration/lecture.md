# Поиск и устранение проблем с конфигурацией статических маршрутов IPv4 и маршрутов IPv4 по умолчанию

<!-- 16.2.1 -->
## Изменения в сети
Независимо от того, насколько хорошо вы настроили свою сеть, вы должны быть готовы к устранению некоторых проблем. Существуют факторы воздействия на сети, которые могут вызвать изменение их статуса, Например, может произойти сбой интерфейса или интернет провайдер обрывает соединение. Каналы могут стать перегруженными, или администратор может ввести неправильную конфигурацию.

При изменении в сети соединение может быть разорвано. Сетевые администраторы отвечают за выявление проблем и их устранение. Для того чтобы найти и устранить возможные проблемы, сетевой администратор должен быть знаком с инструментами, помогающими быстро изолировать проблемы с маршрутизацией.


<!-- 16.2.2 -->
## Часто используемые команды для поиска и устранения неполадок
Часто используемые команды ОС IOS для поиска и устранения неполадок:
- ping
- traceroute
- show ip route
- show ip interface brief
- show cdp neighbors detail

На рисунке показана топология, используемая для демонстрации этих трех команд.

![](./assets/16.2.2.PNG)
<!-- /courses/srwe-dl/af9ef5a6-34fe-11eb-b1b2-9b1b0c1f7e0d/afb822fa-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/cafc0e01-1c27-11ea-af09-3b2e6521927c.svg -->

**ping**

В примере показан результат выполнения расширенного эхо-запроса от исходного интерфейса маршрутизатора R1 к интерфейсу LAN маршрутизатора R3. Расширенный ping-запрос выполняется с помощью усовершенствованной версии утилиты ping. Расширенный ping-запрос позволяет определить IP-адрес источника для пакетов ping.

<pre><code>R1# ping 192.168.2.1 source 172.16.3.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.2.1, timeout is 2 seconds:
Packet sent with a source address of 172.16.3.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 3/3/5 ms
R1#
</code></pre>

**traceroute**

В этом примере показан результат выполнения команды traceroute от маршрутизатора R1 к сети LAN маршрутизатора R3. Обратите внимание, что каждый переход возвращает ответ ICMP.

<pre><code>R1# traceroute 192.168.2.1
Type escape sequence to abort.
Tracing the route to 192.168.2.1
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.2.2 1 msec 2 msec 1 msec
  2 192.168.1.1 2 msec 3 msec *
R1#
</code></pre>

**show ip route**

Команда **show ip route** в этом примере отображает таблицу маршрутизации R1.

<pre><code>R1# show ip route | begin Gateway
Gateway of last resort is not set
      172.16.0.0/16 is variably subnetted, 5 subnets, 2 masks
S 172.16.1.0/24 [1/0] via 172.16.2.2
C 172.16.2.0/24 is directly connected, Serial0/1/0
L 172.16.2.1/32 is directly connected, Serial0/1/0
C 172.16.3.0/24 is directly connected, GigabitEthernet0/0/0
L 172.16.3.1/32 is directly connected, GigabitEthernet0/0/0
S 192.168.1.0/24 [1/0] via 172.16.2.2
S 192.168.2.0/24 [1/0] via 172.16.2.2
R1#
</code></pre>

**show ip interface brief**

Быстрый статус всех интерфейсов маршрутизатора показан с помощью **show ip interface brief** команды в данном примере.

<pre><code>R1# show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0/0 172.16.3.1 YES manual up up
GigabitEthernet0/0/1 unassigned YES unset up up
Serial0/1/0 172.16.2.1 YES manual up up
Serial0/1/1 unassigned YES unset up up
R1#
</code></pre>

**show cdp neighbors**

Команда **show cdp neighbors** предоставляет список напрямую подключенных устройств Cisco. Команда show cdp neighbors detail выполняет проверку соединения второго уровня (и, как следствие, первого уровня). Например, если соседнее устройство указано в выходных данных команды, но эхо-запрос к нему не может быть выполнен, следует искать проблему в адресации третьего уровня.

<pre><code>R1# show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay
Device ID Local Intrfce Holdtme Capability Platform Port ID
Switch Gig 0/0/1 129 S I WS-C3560- Fas 0/5
R2 Ser 0/1/0 156 R S I ISR4221/K Ser 0/1/0
Total cdp entries displayed : 3
R1#
</code></pre>

<!-- 16.2.3 -->
## Устранение проблем соединения
Поиск отсутствующего (или неверно настроенного) маршрута представляет собой довольно простой процесс, если при этом последовательно используются правильно выбранные инструменты.

Пользователь компьютера PC1 сообщает о невозможности доступа к ресурсам в сети LAN маршрутизатора R3. Наличие проблемы можно проверить, отправив эхо-запрос в интерфейс LAN маршрутизатора R3, используя в качестве источника интерфейс LAN маршрутизатора R1. Мы снова будем использовать топологию на рисунке, чтобы продемонстрировать, как устранить эту проблему подключения.

![](./assets/16.2.3.PNG)
<!-- /courses/srwe-dl/af9ef5a6-34fe-11eb-b1b2-9b1b0c1f7e0d/afb822fa-34fe-11eb-b1b2-9b1b0c1f7e0d/assets/cafde2c0-1c27-11ea-af09-3b2e6521927c.svg -->

**Подключение к удаленной LAN**

Администратор сети может проверить соединение между двумя локальными сетями с R1 вместо PC1. Это можно сделать, используя ping от интерфейса G0/0/0 на R1 к интерфейсу G0/0/0 на R3, как показано в примере. Результат команды ping показывает, что между данными сетями LAN нет соединения.

<pre><code>R1# ping 192.168.2.1 source g0/0/0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.2.1, timeout is 2 seconds:
Packet sent with a source address of 172.16.3.1
.....
Success rate is 0 percent (0/5)
</code></pre>

**Эхо-запрос маршрутизатора следующего перехода**

Затем выполняется эхо-запрос на интерфейс S0/1/0 на R2. Этот эхо-запрос получен из интерфейса S0/1/0 R1. Следовательно, проблема заключается не в потере связи между R1 и R2.

<pre><code>R1# ping  172.16.2.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 172.16.2.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 3/3/4 ms
</code></pre>

**Ping R3 LAN от S0/1/0**

Также успешно выполняется эхо-запрос от R1 к интерфейсу R3 192.168.2.1. Этот эхо-запрос получен из интерфейса S0/1/0 на R1. R3 имеет маршрут назад к сети между R1 и R2, 172.16.2.0/24. Это подтверждает, что R1 может достичь удаленной локальной сети на R3. Однако пакеты, исходящие из локальной сети на R1, не могут. Это означает, что R2 или R3 может иметь неверный или отсутствующий маршрут к локальной сети на R1.

<pre><code>R1# ping 192.168.2.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.2.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 3/3/4 ms
</code></pre>

**Проверка таблицы маршрутизации R2**

Следующим шагом является изучение таблиц маршрутизации R2 и R3. Таблица маршрутизации для R2 показана в примере. Обратите внимание, что сеть 172.16.3.0/24 настроена неправильно. Статический маршрут к сети 172.16.3.0/24 настроен с использованием адреса следующего перехода 192.168.1.1. Таким образом пакеты, предназначенные для сети 172.16.3.0/24, отправляются обратно в R3 вместо R1.

<pre><code>R2# show ip route | begin Gateway
Gateway of last resort is not set
      172.16.0.0/16 is variably subnetted, 5 subnets, 2 masks
C 172.16.1.0/24 is directly connected, GigabitEthernet0/0/0
L 172.16.1.1/32 is directly connected, GigabitEthernet0/0/0
C 172.16.2.0/24 is directly connected, Serial0/1/0
L 172.16.2.2/32 is directly connected, Serial0/1/0
S 172.16.3.0/24 [1/0] via 192.168.1.1
      192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks
C 192.168.1.0/24 is directly connected, Serial0/1/1
L 192.168.1.2/32 is directly connected, Serial0/1/1
S 192.168.2.0/24 [1/0] via 192.168.1.1
R2#</code></pre>

**Исправление конфигурации статического маршрута R2**

Далее, запущенная конфигурация фактически раскрывает неверное **ip route** утверждение. Неверный маршрут удаляется, после чего указывается верный маршрут.

<pre><code>R2# show running-config | include ip route ip route 172.16.3.0 255.255.255.0 192.168.1.1
ip route 192.168.2.0 255.255.255.0 192.168.1.1
R2#
R2# configure terminal
Введите построчно команды настройки.  В конце нажмите CNTL/Z.
R2(config)# no ip route 172.16.3.0 255.255.255.0 192.168.1.1
R2(config)# ip route 172.16.3.0 255.255.255.0 172.16.2.1
R2(config)#</code></pre>

**Убедитесь, что установлен новый статический маршрут**

Таблица маршрутизации на R2 проверяется еще раз, чтобы убедиться, что запись маршрута к локальной сети на R1, 172.16.3.0 верна и указывает на R1.

<pre><code>R2(config) # exit
R2#
*Sep 20 02:21:51.812: %SYS-5-CONFIG_I: Configured from console by console
R2# show ip route | begin Gateway
Gateway of last resort is not set
      172.16.0.0/16 is variably subnetted, 5 subnets, 2 masks
C 172.16.1.0/24 is directly connected, GigabitEthernet0/0/0
L 172.16.1.1/32 is directly connected, GigabitEthernet0/0/0
C 172.16.2.0/24 is directly connected, Serial0/1/0
L 172.16.2.2/32 is directly connected, Serial0/1/0
S 172.16.3.0/24 [1/0] via 172.16.2.1
      192.168.1.0/24 is variably subnetted, 2 subnets, 2 masks
C 192.168.1.0/24 is directly connected, Serial0/1/1
L 192.168.1.2/32 is directly connected, Serial0/1/1
S 192.168.2.0/24 [1/0] via 192.168.1.1
R2#</code></pre>

**Снова эхо-запрос удаленной локальной сети**

Затем для проверки того, что R1 теперь может достичь интерфейса локальной сети R3, используется эхо-запрос от R1 через G0/0/0. На последнем этапе проверки пользователь компьютера PC1 должен также выполнить проверку подключения к сети LAN 192.168.2.0/24.

<pre><code>R1# ping 192.168.2.1 source g0/0/0
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.2.1, timeout is 2 seconds:
Packet sent with a source address of 172.16.3.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 4/4/4 ms
</code></pre>

<!-- 16.2.4 Проверка синтаксиса - Поиск и устранение неполадок, связанных со статическими IPv4 маршрутами и маршрутами по умолчанию-->