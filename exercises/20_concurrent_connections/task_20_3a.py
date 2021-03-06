# -*- coding: utf-8 -*-
"""
Задание 20.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
#from itertools import repeat
from pprint import pprint
#--------------------------------------------------------------------------------------
def send_command(device, command):
    '''
    Функция подключается по telnet к устройствам определённым в device
    и предаёт им command
    '''
    with ConnectHandler(**device) as telnet:

        telnet.enable()

#strip_command - удалить саму команду из вывода (по умолчанию True)
#        result = telnet.send_command(command, strip_command=False)
#enter_config_mode - входить ли в конфигурационный режим (по умолчанию True)
        result = telnet.send_config_set(command, strip_prompt=True, enter_config_mode=False)
        
#Убираем лишнее приглашение устройства -
#делаем срез до найденного приглашения
#        result = result[0:result.find(telnet.find_prompt())]
        
#Формируем итоговый результат. У нас уже есть команда и вывод, добавим в начало приглашение.        
#find_prompt - возвращает текущее приглашение устройства
#Чтобы лишние приглашения не налезали друг на друга, добавляем '\n'
        result = telnet.find_prompt() + result + '\n'

        telnet.disconnect()

        return(result)
#--------------------------------------------------------------------------------------
#Создадим функцию
def send_command_to_devices(devices, commands_dict, filename, limit=3):

#Сюда поместим список команд
    command_list = []

#Проходим по устройствам из словаря устройств
    for device in devices:

#Для текущего устройства берём его IP и port, формируем ключ для словаря команд
        keys = f'{device["ip"]}:{device["port"]}'

#В список команд добавляем команду из словаря команд
        command_list.append(commands_dict[keys])

    f = open(filename, 'w')

    with ThreadPoolExecutor(max_workers=limit) as executor:

#Вызываем функцию send_command, передаём ей словарь устройств и в списке команды для этих устройств
        result = executor.map(send_command, devices, command_list)

        for output in result:

            f.write(output)
#            print(output)
    
    f.close()
#--------------------------------------------------------------------------------------
if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_devices.yml'
    filename = 'log.txt'
    
    commands = {
        "10.0.3.251:32769": ["sh ip int br", "sh ip route | ex -"],
        "10.0.3.251:32770": ["sh ip int br", "sh int desc"],
        "10.0.3.251:32771": ["sh int desc"],
    }

#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        devices = yaml.safe_load(f)

#Вызываем функцию
    send_command_to_devices(devices, commands, filename, limit=3)
