# -*- coding: utf-8 -*-
"""
Задание 20.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию, значение None)
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, show='sh clock', filename='result.txt')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, config='logging 10.5.5.5', filename='result.txt')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: send_commands_to_devices(devices,
                                  config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0'],
                                  filename='result.txt')

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
#from itertools import repeat
from pprint import pprint
#--------------------------------------------------------------------------------------
def send_command(device, command, flag):
    '''
    Функция подключается по telnet к устройствам определённым в device
    и предаёт им command
    Если команда show переменная flag должна быть False
    '''
    with ConnectHandler(**device) as telnet:

        telnet.enable()

#strip_command - удалить саму команду из вывода (по умолчанию True)
#enter_config_mode - входить ли в конфигурационный режим (по умолчанию True)
        result = telnet.send_config_set(command, strip_command=False, enter_config_mode=flag)
        
#Убираем лишнее приглашение устройства -
#делаем срез до найденного приглашения
        result = result[0:result.find(telnet.find_prompt())]
        
#Формируем итоговый результат. У нас уже есть команда и вывод, добавим в начало приглашение.        
#find_prompt - возвращает текущее приглашение устройства
        result = telnet.find_prompt() + result

        telnet.disconnect()

        return(result)
#--------------------------------------------------------------------------------------
#Создадим функцию
def send_commands_to_devices(devices, filename, show=None, config=None, limit=3):
#Предполагаем, что передаётся либо команда show, либо команда конфигурации, если и та и другая передана будет только show
#Если show, то flag=False, функция send_command не переводит устройство
#в конфигурационный режим
    flag = True

    command = config

    if show:

        command = show

        flag = False

    f = open(filename, 'w')

    with ThreadPoolExecutor(max_workers=limit) as executor:

        future_list = []

        for device in devices:

            future = executor.submit(send_command, device, command, flag)

            future_list.append(future)

        for item in as_completed(future_list):

            f.write(item.result())

#            print(f.result())
    f.close()
#--------------------------------------------------------------------------------------
if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_devices.yml'
    filename = 'log.txt'
    config=['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']
#    config='logging 10.5.5.5'
    show='sh clock'
	
#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        devices = yaml.safe_load(f)

#Вызываем функцию
#    send_commands_to_devices(devices, show=show, config=config, filename=filename)
    send_commands_to_devices(devices, config=config, filename=filename)
#    send_commands_to_devices(devices, show=show, filename=filename)

