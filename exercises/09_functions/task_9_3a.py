# -*- coding: utf-8 -*-
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


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
            elif ('mode access' in line and not 'access vlan' in line):
                access_dict[intf] = 1
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
tuple_dict = get_int_vlan_map('config_sw2.txt')
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

Отличие от задания 9.3
Иначе проверяем, что в строке есть 'mode access' и нет 'access vlan'. Если да, запись в словаре:
ключ имя интерфейса, значение 1 (превый vlan)

Иначе ищем в строке словосочетание allowed vlan, т.е. мы имеем дело с транковым портом.
Преобразуем строку в список, берём последний элемент и это будет строка vlan через запятую.
Преобразуем эту строку в список, но разделяем элементы не по пробелам, а по запятым.
Получили список номеров vlan в виде слов, а нам нужны цифры. Перезаписываем список меняя слова на цифры.
Делаем запись в словаре. Ключ имя интерфейса, значение список номеров vlan.
'''
