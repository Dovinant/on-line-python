# -*- coding: utf-8 -*-
'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# Создаём функцию
def get_int_vlan_map(config_filename):
    trunk_dict = {}
    access_dict = {}
    with open(config_filename, 'r') as file:
        for line in file:
            if 'interface' in line:
                intf = line.split()[1]
            elif 'access vlan' in line:
                access_dict[intf] = int(line.split()[-1])
            elif 'allowed vlan' in line:
                line = line.split()[-1]
                line = line.split(',')
                line = [int(item) for item in line]
                trunk_dict[intf] = line
# Создаём кортеж
    result = tuple()
    result = (access_dict, trunk_dict)
    return result

# Вызываем функцию, предаём ей аргумент - имя файла
tuple_dict = get_int_vlan_map('config_sw1.txt')
print(tuple_dict)

'''
Создаём два словаря: trunk_dict для портов в режиме trunk и access_dict для портов в режиме access
Конструкцией with открываем файл. Просматриваем файл построчно. Если в строке есть слово interface,
преобразуем строку в список и берём второй элемент, запоминаем это всё в переменную intf
intf = line.split()[1]

Иначе ищем в строке словосочетание access vlan и, если находим, преобразуем строку в список,
берём первый элемент с конца (это будет номер vlan), однако сейчас это для python не цифра, а слово,
поэтому преобразуем этот элемент в цифру и записываем в словарь. Ключ имя интерфейса, значение - номер vlan.
access_dict[intf] = int(line.split()[-1])

Иначе ищем в строке словосочетание allowed vlan, т.е. мы имеем дело с транковым портом.
Преобразуем строку в список, берём последний элемент и это будет строка vlan через запятую.
Преобразуем эту строку в список, но разделяем элементы не по пробелам, а по запятым.
Получили список номеров vlan в виде слов, а нам нужны цифры. Перезаписываем список меняя слова на цифры.
Делаем запись в словаре. Ключ имя интерфейса, значение список номеров vlan.
'''