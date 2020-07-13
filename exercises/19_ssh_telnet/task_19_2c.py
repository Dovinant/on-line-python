# -*- coding: utf-8 -*-
"""
Задание 19.2c

Скопировать функцию send_config_commands из задания 19.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка,
спросить пользователя надо ли выполнять остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию, поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

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

#Принимаем ответ пользователя					
                    answer = input('Продолжать выполнять команды? [y]/n: ')
					
#Приводим ответ в нижний регистр					
                    answer = answer.lower()

#Проверяем, что ответ начинается с 'n'					
                    if answer.startswith('n'):
					
                        result = (good_dict, bad_dict)
					
                        telnet.disconnect()
					
                        return(result)
					
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
