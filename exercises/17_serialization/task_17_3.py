# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

#Нам нужны модули re pprint
import re
from pprint import pprint

#Создадим функцию
def parse_sh_cdp_neighbors(line):

#Найдём имя нашего устройства.	
    hostname = re.search(r'(\w+)[>#]', line).group(1)

    dict_l_2 = {}
	
    result = {}

#В первую группу попадает имя устройства, во вторую имя локального интерфейса, в третью его номер
#в четвёртую имя интерфейса соседнего устройства, в пятую его номер
    regex = r'(\w+)\s+(Eth|Fa[s]?|Gi|Ser) (\S+).*(Eth|Fa[s]?|Gi|Ser) (\S+)'

#Список состоит из кортежей с нужной нам информацией	
    list_result = re.findall(regex, line)

#Перебираем кортежи из списка
    for tuple_line in list_result:

        dict_l_3 = {}

        dict_l_3[f'{tuple_line[0]}'] = f'{tuple_line[3]} {tuple_line[4]}'

        dict_l_2[f'{tuple_line[1]} {tuple_line[2]}'] = dict_l_3

    result[hostname] = dict_l_2	

    return(result)
	

#Откроем файл, вызовем функцию
with open('sh_cdp_n_sw1.txt') as f:

    pprint(parse_sh_cdp_neighbors(f.read()))

'''
В словаре уровня три dict_l_3 ключ имя соседа, значение - его интерфейс.
В словаре уровня два dict_l_2 ключ имя локального интерфейса, значение - словарь уровня три

Функция re.findall возвращает список кортежей, если в регулярном выражении есть больше одной группы.
Первый элемент (индекс 0) получившегося списка есь имя соседа, второй (индекс 1) имя локального интерфейса (Eth),
третий элемент это номер локального интерфейса (0/0), четвёртый имя интерфейса соседа, пятый - номер этого интерфейса
'''