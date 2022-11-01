<!-- 1.5.1 -->
## Команды проверки интерфейса

Нет смысла настраивать маршрутизатор, если вы не проверите конфигурацию и подключение. В этом разделе рассматриваются команды, используемые для проверки непосредственно подключенных сетей. Он включает в себя две проверки синтаксиса и задание в Packet Tracer.

Для проверки работы и настройки интерфейса можно использовать несколько команд **show**. Топология на рисунке используется для демонстрации проверки параметров интерфейса маршрутизатора.

![](./assets/1.5.1.png)


Для того чтобы быстро определить состояние интерфейса, рекомендуется использовать следующие три команды:

Команда **show ip interface brief** и **show ipv6 interface brief** отображает краткую информацию обо всех интерфейсах, в том числе IPv4-адрес интерфейса и текущее рабочее состояние.
* **show running-config interface** идентификатор интерфейса — отображает команды, настроенные на указанном интерфейсе.
* **show ip route** и **show ipv6 route** - Они отображают содержимое таблицы маршрутизации IPv4 или IPv6, хранящейся в ОЗУ. В Cisco IOS 15 активные интерфейсы должны появляться в таблице маршрутизации с двумя связанными записями, идентифицированными кодом '**C**' (подключено) или '**L**' (локально). В предыдущих версиях IOS должна была появиться только одна запись с кодом '**C**'

<!-- 1.5.2 -->
## Проверка состояния интерфейса

Выходные данные команд **show ip interface brief** и **show ipv6 interface brief** можно использовать для быстрого выявления состояния всех интерфейсов маршрутизатора. Вы можете проверить, что интерфейсы активны и работают, как указано в состоянии «up» и протоколе «up», как показано в примере. Получение других выходных данных указывает на проблему с конфигурацией или кабельным соединением.

```
R1# show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0   192.168.10.1    YES manual up                    up
GigabitEthernet0/0/1   192.168.11.1    YES manual up                    up
Serial0/1/0            209.165.200.225 YES manual up                    up
Serial0/1/1            unassigned      YES unset  administratively down down
R1# show ipv6 interface brief
GigabitEthernet0/0/0   [up/up]
    FE80::7279:B3FF:FE92:3130
    2001:DB8:ACAD:1::1
GigabitEthernet0/0/1   [up/up]
    FE80::7279:B3FF:FE92:3131
    2001:DB8:ACAD:2::1
Serial0/1/0            [up/up]
    FE80::7279:B3FF:FE92:3130
    2001:DB8:ACAD:3::1
Serial0/1/1            [down/down]     Unassigned
```

<!-- 1.5.3 -->
## Проверка локальных адресов канала и многоадресных адресов IPv6

В выходных данных **show ipv6 interface brief** отображаются два настроенных IPv6-адреса на каждый интерфейс. Один из адресов — глобальный индивидуальный адрес IPv6, который был введен вручную. Другой адрес, который начинается с FE80, это локальный индивидуальный адрес канала для интерфейса. Локальный адрес канала автоматически добавляется на интерфейс при назначении глобального индивидуального адреса. Для сетевого интерфейса с IPv6-настройками требуется локальный адрес канала, но необязателен глобальный индивидуальный адрес.

Результат выполнения команды **show ipv6 interface gigabitethernet 0/0/0** отображает состояние интерфейса и все IPv6-адреса, принадлежащие этому интерфейсу. Кроме локального адреса канала и глобального индивидуального адреса, выходные данные содержат групповые адреса, назначенные интерфейсу и начинающиеся с префикса FF02.

```
R1# show ipv6 interface gigabitethernet 0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  IPv6 is enabled, link-local address is FE80::7279:B3FF:FE92:3130
  No Virtual link-local address(es):
  Global unicast address(es):
    2001:DB8:ACAD:1::1, subnet is 2001:DB8:ACAD:1::/64
  Joined group address(es):
    FF02::1
    FF02::1:FF00:1
    FF02::1:FF92:3130
  MTU is 1500 bytes
  ICMP error messages limited to one every 100 milliseconds
  ICMP redirects are enabled
  ICMP unreachables are sent
  ND DAD is enabled, number of DAD attempts: 1
  ND reachable time is 30000 milliseconds (using 30000)
  ND advertised reachable time is 0 (unspecified)
  ND advertised retransmit interval is 0 (unspecified)
  ND router advertisements are sent every 200 seconds
  ND router advertisements live for 1800 seconds
  ND advertised default router preference is Medium
```

<!-- 1.5.4 -->
## Проверка конфигурации интерфейса

Выходные данные отображают текущие команды **show running-config interface**, настроенные на указанном интерфейсе.

```
R1 show running-config interface gigabitethernet 0/0/0
Building configuration...
Current configuration : 158 bytes
!
interface GigabitEthernet0/0/0
 description Link to LAN 1
 ip address 192.168.10.1 255.255.255.0
 negotiation auto
 ipv6 address 2001:DB8:ACAD:1::1/64
end
R1#
```

Для получения дополнительной информации об интерфейсе используются следующие две команды:

* Команда **show interfaces** отображает информацию об интерфейсе и счетчик потока пакетов для всех интерфейсов на устройстве.
* **show ip interface** и **show ipv6 interface** — отображает информацию, связанную с IPv4, для всех интерфейсов маршрутизатора.

<!-- 1.5.5 -->
## Проверка маршрутов маршрутизатора

Выходные данные команд **show ip route** и **show ipv6 route** показывают три непосредственно подключенных сетевых элемента и три записи интерфейса локального узла маршрута, как показано в примере. Административное расстояние маршрута локального узла равно 0. Его маска для IPv4 равна /32, а для IPv6 — /128. Маршрут локального узла относится к маршрутам на маршрутизаторе с IP-адресом. Он используется для того, чтобы маршрутизатор мог обрабатывать пакеты, предназначенные для этого IP.

```
R1# show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP

Gateway of last resort is not set
      192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.10.0/24 is directly connected, GigabitEthernet0/0/0
L        192.168.10.1/32 is directly connected, GigabitEthernet0/0/0
      192.168.11.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.11.0/24 is directly connected, GigabitEthernet0/0/1
L        192.168.11.1/32 is directly connected, GigabitEthernet0/0/1
      209.165.200.0/24 is variably subnetted, 2 subnets, 2 masks
C        209.165.200.224/30 is directly connected, Serial0/1/0
L        209.165.200.225/32 is directly connected, Serial0/1/0
R1# show ipv6 route
IPv6 Routing Table - default - 7 entries
Codes: C - Connected, L - Local, S - Static, U - Per-user Static route
       
C   2001:DB8:ACAD:1::/64 [0/0]
     via GigabitEthernet0/0/0, directly connected
L   2001:DB8:ACAD:1::1/128 [0/0]
     via GigabitEthernet0/0/0, receive
C   2001:DB8:ACAD:2::/64 [0/0]
     via GigabitEthernet0/0/1, directly connected
L   2001:DB8:ACAD:2::1/128 [0/0]
     via GigabitEthernet0/0/1, receive
C   2001:DB8:ACAD:3::/64 [0/0]
     via Serial0/1/0, directly connected
L   2001:DB8:ACAD:3::1/128 [0/0]
     via Serial0/1/0, receive
L   FF00::/8 [0/0]
     via Null0, receive
R1#
```

В таблице маршрутизации символ **C** рядом с маршрутом означает, что это сеть с прямым подключением. Когда интерфейс маршрутизатора настраивается с глобальным индивидуальным адресом и находится в активном состоянии (up/up), IPv6-префикс и длина префикса добавляются в таблицу IPv6-маршрутизации в качестве подключенного маршрута.

Глобальный индивидуальный адрес IPv6, настраиваемый на интерфейсе, также заносится в таблицу маршрутизации в качестве локального маршрута. Локальный маршрут имеет префикс /128. Локальные маршруты используются таблицами маршрутизации для эффективной обработки пакетов с адресом интерфейса маршрутизатора в качестве назначения.

Команда **ping** для IPv6 идентична команде, используемой для IPv4, за исключением того, что используется IPv6-адрес. Как показано на примере, эта команда **ping** используется для проверки подключения 3-го уровня между маршрутизатором R1 и PC1.

```
R1# ping 2001:db8:acad:1::10
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 2001:DB8:ACAD:1::10, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms
```

<!-- 1.5.6 -->
## Фильтрация выходных данных команды show

Команды, которые производят несколько экранов выходных данных, по умолчанию приостанавливаются после 24 строк. В конце приостановленных выходных данных отображается текст --More--. Для вывода следующей строки нажмите **Enter**, а для отображения набора строк нажмите ПРОБЕЛ. Для указания количества отображаемых строк используйте команду **terminal length**. Значение 0 (ноль) позволяет просмотреть выходные данные без приостановки в процессе вывода данных на экран.

Удобство работы с интерфейсом командной строки также можно повысить с помощью фильтрации выходных данных команды **show**. Для отображения определенных разделов выходных данных можно использовать команды фильтрации. Чтобы включить фильтрацию, введите вертикальную черту **|** после команды **show**, а затем введите параметр и выражение фильтрации.

К параметрам фильтрации, которые следует указывать после вертикальной черты, относятся:

**section**

section — показать целый раздел, который начинается с заданного фильтра.

```
R1# show running-config | section line vty 
line vty 0 4
 password 7 110A1016141D
 login
 transport input all
```

**include**

include — включить все строки выходных данных, которые соответствуют заданному фильтру.

```
R1# show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0/0 192.168.10.1 YES manual up up
GigabitEthernet0/0/1 192.168.11.1 YES manual up up
Serial0/1/0 209.165.200.225 YES manual up up
Serial0/1/1 unassigned NO unset down down
R1#
R1# show ip interface brief | include up 
GigabitEthernet0/0/0 192.168.10.1 YES manual up up
GigabitEthernet0/0/1 192.168.11.1 YES manual up up
Serial0/1/0 209.165.200.225 YES manual up up
```

**exclude**

exclude — исключить все строки выходных данных, которые соответствуют заданному фильтру.

```
R1# show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0/0 192.168.10.1 YES manual up up
GigabitEthernet0/0/1 192.168.11.1 YES manual up up
Serial0/1/0 209.165.200.225 YES manual up up
Serial0/1/1 unassigned NO unset down down
R1#
R1# show ip interface brief | exclude unassigned
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0/0 192.168.10.1 YES manual up up
GigabitEthernet0/0/1 192.168.11.1 YES manual up up
Serial0/1/0 209.165.200.225 YES manual up up
```

**begin**

begin — показать все строки выходных данных от конкретного места, начиная с линии, которая соответствует заданному фильтру.

```
R1# show ip route | begin Gateway
Gateway of last resort is not set
      192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C 192.168.10.0/24 is directly connected, GigabitEthernet0/0/0
L 192.168.10.1/32 is directly connected, GigabitEthernet0/0/0
      192.168.11.0/24 is variably subnetted, 2 subnets, 2 masks
C 192.168.11.0/24 is directly connected, GigabitEthernet0/0/1
L 192.168.11.1/32 is directly connected, GigabitEthernet0/0/1
      209.165.200.0/24 is variably subnetted, 2 subnets, 2 masks
C 209.165.200.224/30 is directly connected, Serial0/1/0
L 209.165.200.225/32 is directly connected, Serial0/1/0
```

**Примечание**: Фильтры выходных данных можно использовать в сочетании с любой командой **show**.

<!-- 1.5.7 -->
<!-- syntax -->

<!-- 1.5.8 -->
## Функция истории команд

Функция истории команд обеспечивает возможность временного хранения списка выполненных команд для последующего просмотра.

Для вызова команды из буфера команд нажмите комбинацию клавиш **Ctrl**+**P** или клавишу **Up Arrow**. Отображение команд начинается с последней выполненной команды. Повторяйте это сочетание клавиш для вызова каждой последующей, более старой команды. Для возврата к последним выполненным командам нажмите комбинацию клавиш **Ctrl**+**N** или клавишу **Down Arrow**. Повторяйте это сочетание клавиш для вызова каждой последующей, более новой команды.

Функция истории команд включена по умолчанию; система записывает последние десять командных строк в своем буфере. Чтобы отобразить содержимое буфера, используйте команду привилегированного режима **show history**.

На время текущего сеанса можно увеличить количество командных строк, записываемых в буфер. Для того чтобы увеличить или уменьшить размер буфера, используйте команду пользовательского режима **terminal history size**.

Пример команд **terminal history size** и **show history** показан на рисунке.

```
R1# terminal history size 200
R1# show history
  show ip int brief
  show interface g0/0/0
  show ip route
  show running-config
  show history
  terminal history size 200
```

<!-- 1.5.9 -->
<!-- syntax -->



