<!-- 6.3.1 -->
## Проверка EtherChannel

Как всегда, при настройке устройств в сети необходимо проверить конфигурацию. Если есть проблемы, вы должны иметь возможность устранять и устранять их. В этом разделе приведены команды для проверки, а также некоторые распространенные проблемы сети EtherChannel и их решения.

Примеры команд проверки будут использовать топологию, показанную на рисунке.

![](./assets/6.3.1.svg)


**show interfaces port-channel**

С помощью команды **show interfaces port-channel** отображается общий статус интерфейса агрегированного канала. На рисунке интерфейс Port Channel 1 включен.

```
S1# show interfaces port-channel 1
Port-channel1 is up, line protocol is up (connected)
  Hardware is EtherChannel, address is c07b.bcc4.a981 (bia c07b.bcc4.a981)
  MTU 1500 bytes, BW 200000 Kbit/sec, DLY 100 usec,
     reliability 255/255, txload 1/255, rxload 1/255
(дальше выходные данные опущены)
```

**show etherchannel summary**

Когда на одном устройстве настроено несколько интерфейсов агрегированного канала, необходимо использовать команду **show etherchannel summary**, чтобы отобразить по одной строке данных на каждый канал. В выводе на коммутаторе настроен один канал EtherChannel; группа 1 использует LACP.

Группа интерфейсов состоит из интерфейсов FastEthernet0/1 и FastEthernet0/2. Группа является каналом EtherChannel 2-го уровня, и она задействована, на что указывают буквы SU рядом с номером агрегированного канала.

```
S1# show etherchannel summary
Flags: D - down P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3 S - Layer2
        U - in use N - not in use, no aggregation
        f - failed to allocate aggregator
        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port
        A - formed by Auto LAG
Number of channel-groups in use: 1
Number of aggregators: 1
Group Port-channel Protocol Ports
------+-------------+-----------+-----------------------------------------------
1 Po1(SU) LACP Fa0/1(P) Fa0/2(P)
```

**show etherchannel port-channel**

Используйте команду **show etherchannel port-channel** чтобы отобразить сведения о конкретном интерфейсе агрегированного канала, как показано в выводе. В рассматриваемом примере интерфейс Port Channel 1 состоит из двух физических интерфейсов — FastEthernet0/1 и FastEthernet0/2. Он использует LACP в активном режиме (active). Он правильно подключен к другому коммутатору с совместимой конфигурацией, и поэтому агрегированный канал считается задействованным.

```
S1# show etherchannel port-channel
                Channel-group listing:
                —
Group: 1
----------
                Port-channels in the group:
                ---------------------------
Port-channel: Po1 (Primary Aggregator)
------------
Age of the Port-channel = 0d:01h:02m:10s
Logical slot/port = 2/1 Number of ports = 2
HotStandBy port = null
Port state = Port-channel Ag-Inuse
Protocol = LACP
Port security = Disabled
Load share deferral = Disabled
Ports in the Port-channel:
Index Load Port EC state No of bits
------+------+------+------------------+-----------
  0 00 Fa0/1 Active 0
  0 00 Fa0/2 Active 0
Time since last port bundled: 0d:00h:09m:30s Fa0/2
```

**show interfaces etherchannel**

Чтобы просмотреть данные о роли физического интерфейса в работе EtherChannel, следует выполнить команду **show interfaces etherchannel**, как показано в выводе. Интерфейс FastEthernet0/1 относится к группе EtherChannel 1. Для данного канала EtherChannel используется протокол LACP.

```
S1# show interfaces f0/1 etherchannel
Port state = Up Mstr Assoc In-Bndl
Channel group = 1 Mode = Active Gcchange = -
Port-channel = Po1 GC = - Pseudo port-channel = Po1
Port index = 0 Load = 0x00 Protocol = LACP
Флаги: S - Устройство отправляет медленные LACPDU F - Устройство отправляет быстрые LACPDU.
        A - Device is in active mode.        P - Device is in passive mode.
Local information:
                            LACP port Admin Oper Port       
Port Flags State Priority Key Number State
Fa0/1 SA bndl 32768 0x1 0x1 0x102 0x3D
Partner's information:
                  LACP port Admin Oper Port Port
Port Flags Priority Dev ID Age key Key Number State
Fa0/1 SA 32768 c025.5cd7.ef00 12s 0x0 0x1 0x102 0x3Dof the port in the current state: 0d:00h:11m:51sllowed vlan 1,2,20
```

<!-- 6.3.2 -->
## Общие проблемы с конфигурациями EtherChannel

Все интерфейсы в EtherChannel должны иметь одинаковые настройки скорости и дуплексного режима, одинаковые сети VLAN с нетегированным трафиком, разрешенные сети VLAN в магистралях и одинаковые сети VLAN доступа на портах доступа. Обеспечение этих конфигураций значительно снизит сетевые проблемы, связанные с EtherChannel. К числу распространенных проблем EtherChannel относятся следующие:

* Назначенные порты в EtherChannel не являются частью одной VLAN или не настроены как транки. Порты с различными native VLAN не могут образовать EtherChannel.
* Транк был настроен на некоторых портах, которые составляют EtherChannel, но не на всех из них. Не рекомендуется настраивать режим транкинга на отдельных портах, составляющих EtherChannel. При настройке магистрального канала в EtherChannel проверьте режим транкинга в EtherChannel.
* Если допустимый диапазон VLAN не совпадает, порты не формируют EtherChannel, даже если PAgP установлен в режим **auto** или **desirable**.
* Параметры динамического согласования для PAgP и LACP не совместимы на обоих концах EtherChannel.

**Примечание**: Легко спутать протокол PAgP или LACP с DTP, поскольку оба протокола используются для автоматизации поведения на транковых каналах. Протоколы PAgP и LACP используются для агрегирования каналов (EtherChannel). DTP используется для автоматизации создания транковых каналов. Как правило, если настроен транковый канал EtherChannel, то EtherChannel (PAgP или LACP) настраивается в первую очередь, и только после этого настраивается DTP.

<!-- 6.3.3 -->
## Пример поиска и устранения неисправностей в работе EtherChannel

На рисунке интерфейсы F0/1 и F0/2 на коммутаторах S1 и S2 соединены с помощью EtherChannel. Тем не менее EtherChannel не работает.

![](./assets/6.3.1.svg)
<-- same as 6.3.3 -->


**Шаг 1. Просмотр сводной информации EtherChannel**

В выходных данных команды **show etherchannel summary** показано, что EtherChannel выключен.

```
S1# show etherchannel summary
Flags: D - down P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3 S - Layer2
        U - in use N - not in use, no aggregation
        f - failed to allocate aggregator
        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port
        A - formed by Auto LAG
Number of channel-groups in use: 1
Number of aggregators: 1
Group Port-channel Protocol Ports
------+-------------+-----------+-----------------------------------------------
1 Po1(SD) - Fa0/1(D) Fa0/2(D)
```

**Шаг 2. Просмотр конфигурации Port Channel**

В **show run | begin interface port-channel** выводе представлены более подробные выходные данные, в которых указано, что на коммутаторах S1 и S2 настроены несовместимые режимы PAgP.

```
S1# show run | begin interface port-channel
interface Port-channel1
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
!
interface FastEthernet0/1
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
 channel-group 1 mode on
!
interface FastEthernet0/2
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
 channel-group 1 mode on
! ====================================
S2# show run | begin interface port-channel
interface Port-channel1
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
!
interface FastEthernet0/1
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
 channel-group 1 mode desirable
!
interface FastEthernet0/2
 switchport trunk allowed vlan 1,2,20
 switchport mode trunk
 channel-group 1 mode desirable
```

**Шаг 3. Исправление всех неправильно выполненных настроек**

Чтобы устранить проблему, режим PAgP на EtherChannel изменен на desirable.

**Примечание**: EtherChannel и STP должны быть совместимыми. По этой причине важен порядок, в котором вводятся команды, относящиеся к EtherChannel, поэтому вы видите, что интерфейс Port-Channel 1 удален, а затем снова добавлен с командой **channel-group**, а не изменен напрямую. При попытке изменить конфигурацию интерфейса напрямую ошибки STP приводят к тому, что связанные порты переходят в состояние блокировки или в состояние errdisable.

```
S1(config)# no interface port-channel 1
S1(config)# interface range fa0/1 - 2
S1(config-if-range)# channel-group 1 mode desirable
Creating a port-channel interface Port-channel 1
S1(config-if-range)# no shutdown
S1(config-if-range)# exit
S1(config)# interface range fa0/1 - 2
S1(config-if-range)# channel-group 1 mode desirable
S1(config-if-range)# no shutdown
S1(config-if-range)# interface port-channel 1
S1(config-if)# switchport mode trunk
S1(config-if)# end
S1# 
```

**Шаг 4. Проверка работоспособности EtherChannel**

EtherChannel теперь активен, как проверено выходными данными **show etherchannel summary** команды.

```
S1# show etherchannel summary
Flags: D - down P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3 S - Layer2
        U - in use N - not in use, no aggregation
        f - failed to allocate aggregator
        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port
        A - formed by Auto LAG
Number of channel-groups in use: 1
Number of aggregators: 1
Group Port-channel Protocol Ports
------+-------------+-----------+-----------------------------------------------
1 Po1(SU) PAgP Fa0/1(P) Fa0/2(P)
```

