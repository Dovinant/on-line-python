# -*- coding: utf-8 -*-
"""
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

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
        result = telnet.send_command(command, strip_command=False)
        
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
    
    f.close()
#--------------------------------------------------------------------------------------
if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_devices.yml'
    
    commands = {
    "10.0.3.251:32769": "sh run | s ^router ospf",
    "10.0.3.251:32770": "sh ip int br",
    "10.0.3.251:32771": "sh int desc",
    }
    filename = 'log.txt'

#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        devices = yaml.safe_load(f)

#Вызываем функцию
    send_command_to_devices(devices, commands, filename, limit=3)

