# -*- coding: utf-8 -*-
"""
Задание 19.1a

Скопировать функцию send_show_command из задания 19.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется
при ошибке аутентификации на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""
#Импортируем модули
import yaml
from netmiko import ConnectHandler
#Следующий модуль ловит ошибки аутентификации
from netmiko.ssh_exception import NetmikoAuthenticationException
#from pprint import pprint
#
def send_show_command(device, command):
    '''
    Функция подключается по SSH к ОДНОМУ устройству и выполняет указанную команду.
    Параметры функции:
    * device - словарь с параметрами подключения к устройству
    * command - команда, которую надо выполнить
    '''
    try:

        with ConnectHandler(**device) as telnet:

            telnet.enable()

            result = telnet.send_command(command)

            telnet.disconnect()

            return(result)

#Неправильный пароль SSH либо Telnet, или неверное имя пользователя
#генерируют исключение типа NetmikoAuthenticationException
#Если нужно вывести оригинальное сообщение применим такую конструкцию
    except NetmikoAuthenticationException as err:

        print(err)
        print('Authentication failure: unable to connect')
#        print('Authentication failure: unable to connect to {}'.format(device['ip']))

#Неверный пароль enable	приводит к исключению ValueError
    except ValueError as err:

        print(err)
#        print('Enable mode failure for {}.\nCheck the enable password'.format(device['ip']))
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
	
    result = send_show_command(dev_dict, command)

    if result:

        print(result)

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
