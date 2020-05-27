# -*- coding: utf-8 -*-
'''
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
'''

#Нам нужен модуль re
import re
# И модуль pprint чтобы красиво отображать вывод
from pprint import pprint

#Создадим функцию
def generate_description_from_cdp(file_input):

#В первую группу попадает имя устройства, во вторую имя локального интерфейса, в третью его номер
#в четвёртую имя интерфейса соседнего устройства, в пятую его номер
    regex = r'(\w+)\s+(Eth|Fas|Gi|Ser) (\S+).*(Eth|Fas|Gi|Ser) (\S+)'

    result = {}

    with open(file_input) as f:
	
#Функция finditer отлично подходит для обработки тех команд, вывод которых отображается
#столбцами.
        match = re.finditer(regex, f.read())

#В match теперь находится итератор, пройдём по нему
        for line in match:

#intf_key - ключ словаря, формируем его из имени и номера локального интерфейса
            intf_key = f'{line.group(2)} {line.group(3)}'

#command - значение ключа

            command = f'description Connected to {line.group(1)} port {line.group(4)} {line.group(5)}'

            result[intf_key] = command

    return(result)

#
pprint(generate_description_from_cdp('sh_cdp_n_sw1.txt'))

