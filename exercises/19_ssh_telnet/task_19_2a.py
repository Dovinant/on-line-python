# -*- coding: utf-8 -*-
"""
Задание 19.2a

Скопировать функцию send_config_commands из задания 19.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода
информация о том к какому устройству выполняется подключение.

По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства из файла devices.yaml с помощью функции send_config_commands.
"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
#Следующий модуль ловит ошибки аутентификации
from netmiko.ssh_exception import NetmikoAuthenticationException
#Следующий модуль ловит ошибки таймаута
import socket
#from pprint import pprint
#
def send_config_commands(device, config_commands, log=True):
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

            if log:

                print('Подключаюсь к {}...'.format(device['ip']))

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

if __name__ == '__main__':

#Определяем переменные
    yaml_file = 'unl_devices.yml'
    commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        templates = yaml.safe_load(f)

#Выбираем словарь из списка, отправляем функции send_config_commands(), принимаем вывод команды
    for dev_dict in templates:

        print('-' * 80)

        print(send_config_commands(dev_dict, commands, log=False))
