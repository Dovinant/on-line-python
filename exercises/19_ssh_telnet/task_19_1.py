# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству и выполняет указанную команду.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* command - команда, которую надо выполнить

Функция возвращает строку с выводом команды.

Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_show_command.

"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
#
def send_show_command(device, command):
    '''
    Функция подключается по SSH к ОДНОМУ устройству и выполняет указанную команду.
    Параметры функции:
    * device - словарь с параметрами подключения к устройству
    * command - команда, которую надо выполнить
    '''
    with ConnectHandler(**device) as telnet:

        telnet.enable()

        result = telnet.send_command(command)

        telnet.disconnect()

        return(result)
#------------------------------------------------------------------------------------------
#Определяем переменные
yaml_file = 'unl_devices.yml'
command = "sh ip int br"

#Читаем yaml файл, составляем список словарей
with open(yaml_file) as f:

    templates = yaml.safe_load(f)

#Выбираем словарь из списка, отправляем функции send_show_command(), принимаем вывод команды
for dev_dict in templates:
    
    print('-' * 80)
    
    print(send_show_command(dev_dict, command))

'''
Задание решено на UNL. Вывести стенд UNL в раеальную сеть пока не получилось,
поэтому подключаемся по telnet на один и тот же адрес, но на разные порты,
т.е. у нас КОНСОЛЬНОЕ подключение к каждому маршрутизатору и пароль - это пароль консоли.

Настройка маршрутизаторов:
enable
configure terminal
enable password cisco
username cisco password cisco
line con 0
login local

Файл yaml изменён под наши условия и называется unl_devices.yml

Когда подключаемся к устройствам UNL по консоли, возникает заметная пауза.
Хорошо бы сначала передать устройствам строку вида '\r\n'
'''
