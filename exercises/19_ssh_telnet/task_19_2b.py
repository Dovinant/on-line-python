# -*- coding: utf-8 -*-
"""
Задание 19.2b

Скопировать функцию send_config_commands из задания 19.2a и добавить проверку на ошибки.

При выполнении каждой команды, скрипт должен проверять результат на такие ошибки:
 * Invalid input detected, Incomplete command, Ambiguous command

Если при выполнении какой-то из команд возникла ошибка,
функция должна выводить сообщение на стандартный поток вывода с информацией
о том, какая ошибка возникла, при выполнении какой команды и на каком устройстве, например:
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1

Ошибки должны выводиться всегда, независимо от значения параметра log.
При этом, параметр log по-прежнему должен контролировать будет ли выводиться сообщение:
Подключаюсь к 192.168.100.1...


Функция send_config_commands теперь должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате:
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.


Пример работы функции send_config_commands:

In [16]: commands
Out[16]:
['logging 0255.255.1',
 'logging',
 'a',
 'logging buffered 20010',
 'ip http server']

In [17]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Команда "a" выполнилась с ошибкой "Ambiguous command:  "a"" на устройстве 192.168.100.1

In [18]: pprint(result, width=120)
({'ip http server': 'config term\n'
                    'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                    'R1(config)#ip http server\n'
                    'R1(config)#',
  'logging buffered 20010': 'config term\n'
                            'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                            'R1(config)#logging buffered 20010\n'
                            'R1(config)#'},
 {'a': 'config term\n'
       'Enter configuration commands, one per line.  End with CNTL/Z.\n'
       'R1(config)#a\n'
       '% Ambiguous command:  "a"\n'
       'R1(config)#',
  'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

In [19]: good, bad = result

In [20]: good.keys()
Out[20]: dict_keys(['logging buffered 20010', 'ip http server'])

In [21]: bad.keys()
Out[21]: dict_keys(['logging 0255.255.1', 'logging', 'a'])


Примеры команд с ошибками:
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
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
#
def send_config_commands(device, config_commands, log=True):
    '''
    Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству и выполняет перечень команд в конфигурационном режиме
    на основании переданных аргументов.

    Параметры функции:
    * device - словарь с параметрами подключения к устройству
    * config_commands - список команд, которые надо выполнить

    Функция возвращает кортеж из двух словарей:
    * первый словарь с выводом команд, которые выполнились без ошибки
    * второй словарь с выводом команд, которые выполнились с ошибками
    '''
#Создаём регулярное выражение. Оно ловит текст ошибок	
    regex = re.compile(r'(% .+)')
	
#Создаём два словаря. В один попадут команды и результаты их выполнения с ошибками, в другой без ошибок	
    bad_dict = {}
    good_dict = {}
	
    try:

        with ConnectHandler(**device) as telnet:

            if log:

                print('Подключаюсь к {}...'.format(device['ip']))

            telnet.enable()

            for commands in config_commands:

#Метод send_config_set позволяет отправить команду или несколько команд конфигурационного режима.
#https://ktbyers.github.io/netmiko/docs/netmiko/index.html#netmiko.BaseConnection.send_config_set
#                result = telnet.send_config_set(commands, exit_config_mode=False)
                result = telnet.send_config_set(commands)

#Ищем сообщение об ошибке, записываем его в match
                match = regex.search(result)
				
                if match:
				
                    print(f'команда "{commands}" выполнилась с ошибкой "{match.groups()[0]}" на устройстве {device["ip"]}')
					
                    bad_dict[commands] = result
					
                else:
				
                    good_dict[commands] = result
					
                result = (good_dict, bad_dict)

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
    yaml_file = 'unl_device.yml'
    
# списки команд с ошибками и без:
    commands_with_errors = ["logging 0255.255.1", "logging", "a"]
	
    correct_commands = ["logging buffered 20010", "ip http server"]

    commands = commands_with_errors + correct_commands

#Читаем yaml файл, составляем список словарей
    with open(yaml_file) as f:

        templates = yaml.safe_load(f)

#Выбираем словарь из списка, отправляем функции send_config_commands(), принимаем вывод команды
    for dev_dict in templates:

        print('-' * 80)

        pprint(send_config_commands(dev_dict, commands, log=False))
#        send_config_commands(dev_dict, commands_with_errors, log=False)

