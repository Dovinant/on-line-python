# -*- coding: utf-8 -*-
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''

#Нам нужен модуль re
import re

#Создадим функцию
def convert_ios_nat_to_asa(file_input, file_output):
#Регулярное выражение ищет протокол, IP, оригинальный порт, маскирующий порт
#Группы здесь именованные
    regex = (r'static\s(?P<protocol>\w+) (?P<ip>\d+.\d+.\d+.\d+) (?P<port_in>\d+) \S+ \S+ (?P<port_out>\d+)')
#Открываем оба переданных нам файла
    with open(file_input) as src, open(file_output, 'w') as dest:
        for line in src:
            match = re.search(regex, line)

#Перезаписываем переменную line.
#Готовим f-строку, подставляем значениея из групп
            line = f"object network LOCAL_{match.group('ip')}\n host {match.group('ip')}\n nat (inside,outside) static interface service {match.group('protocol')} {match.group('port_in')} {match.group('port_out')}\n"
            dest.write(line)
#
#Вызываем функцию
convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_asa_config.txt')
