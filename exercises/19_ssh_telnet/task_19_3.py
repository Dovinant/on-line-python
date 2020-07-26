# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к одному устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'

"""
#Импортируем модули
import yaml
import re
from netmiko import ConnectHandler
#Следующий модуль ловит ошибки аутентификации
from netmiko.ssh_exception import NetmikoAuthenticationException
#Следующий модуль ловит ошибки таймаута
import socket
from pprint import pprint

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
def send_config_commands(device, config_commands):
    '''
    Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству и выполняет перечень команд в конфигурационном режиме
    на основании переданных аргументов.

    Параметры функции:
    * device - словарь с параметрами подключения к устройству
    * config_commands - список команд, которые надо выполнить

    Функция возвращает строку с результатами выполнения команды.
    '''
    try:

        with ConnectHandler(**device) as telnet:

            telnet.enable()

#Метод send_config_set позволяет отправить команду или несколько команд конфигурационного режима.
#https://ktbyers.github.io/netmiko/docs/netmiko/index.html#netmiko.BaseConnection.send_config_set
            result = telnet.send_config_set(config_commands)

            telnet.disconnect()

            return(result)

#Неправильный пароль SSH либо Telnet, или неверное имя пользователя
#генерируют исключение типа NetmikoAuthenticationException
#Если нужно вывести оригинальное сообщение применим такую конструкцию
    except NetmikoAuthenticationException as err:

        print(err)

#        print('Authentication failure: unable to connect to {}'.format(device['ip']))

#Неверный пароль enable	приводит к исключению ValueError
    except ValueError as err:

        print(err)
#        print('Enable mode failure for {}.\nCheck the enable password'.format(device['ip']))
		
#Неверный либо недоступный IP приведёт к таймауту
    except socket.timeout:

        print(f"Unable to connect to {device['ip']}\nTime out!")

#Если IP доступен, но не открыт порт, выскакивает ошибка 'No route to host' либо 'Connection refused'
#Разные ошибки возникают, наверное, из-за особенностей работы firewall
#Ловим их так
    except OSError as err:

        print(err, device['ip'])
#------------------------------------------------------------------------------------------
#Создаём функцию
def send_commands(device, command):

    if type(command) is list:

        print(send_config_commands(device, command))

    elif type(command) is str:

        print(send_show_command(device, command))
#        print(command)
#------------------------------------------------------------------------------------------

if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_device.yml'
    
#Читаем yaml файл, составляем список словарей
with open(yaml_file) as f:

    templates = yaml.safe_load(f)    
	
#Список команд и команда
    commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
    command = "sh ip int br"

#Выбираем словарь из списка, отправляем функции send_config_commands(), принимаем вывод команды
    for dev_dict in templates:

        send_commands(dev_dict, commands)
