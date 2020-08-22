# -*- coding: utf-8 -*-
"""
Задание 20.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
#from pprint import pprint
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
#        result = telnet.find_prompt() + result + '\n'
        result = telnet.find_prompt() + result

        telnet.disconnect()

        return(result)
#--------------------------------------------------------------------------------------
#Создадим функцию
def send_show_command_to_devices(devices, command, filename, limit=3):

    f = open(filename, 'w')

    with ThreadPoolExecutor(max_workers=limit) as executor:
    
        result = executor.map(send_command, devices, repeat(command))
        
        for output in result:
        
            f.write(output)

    f.close()

#--------------------------------------------------------------------------------------
if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_devices.yml'
    command = "sh ip int br"
    filename = 'log.txt'

#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        devices = yaml.safe_load(f)

#Вызываем функцию
    send_show_command_to_devices(devices, command, filename, limit=3)
    
'''
Проверял работу скрипта на UNL стенде, подключался по telnet на один и тот же адрес, но на разные порты, смотри unl_devices.yml.
В выводе появляется приглашение устройства, как будто устройству передаётся лишний перевод строки, нажатие на клавишу Enter.
В учебнике такого нет, вероятно, это особенность такого подключения к стенду.
Лишнее приглашение удаляем командой
result = result[0:result.find(telnet.find_prompt())]
'''
