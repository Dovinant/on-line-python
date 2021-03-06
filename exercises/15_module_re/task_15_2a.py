# -*- coding: utf-8 -*-
'''
Задание 15.2a

Создать функцию convert_to_dict, которая ожидает два аргумента:
* список с названиями полей
* список кортежей со значениями

Функция возвращает результат в виде списка словарей, где ключи - взяты из первого списка,
а значения подставлены из второго.

Например, если функции передать как аргументы список headers и список
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 'FastEthernet0/1', '10.0.2.1', 'up', 'up')]

Функция должна вернуть такой список со словарями (порядок полей может быть другой):
[{'interface': 'FastEthernet0/0', 'address': '10.0.1.1', 'status': 'up', 'protocol': 'up'},
 {'interface': 'FastEthernet0/1', 'address': '10.0.2.1', 'status': 'up', 'protocol': 'up'}]

Проверить работу функции:
* первый аргумент - список headers
* второй аргумент - результат, который возвращает функция parse_sh_ip_int_br из задания 15.2, если ей как аргумент передать sh_ip_int_br.txt.

Функцию parse_sh_ip_int_br не нужно копировать.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# Нам нужен модуль pprint чтобы красиво отображать вывод
from pprint import pprint
# Импортируем функцию из предидущей задачи
from task_15_2 import parse_sh_ip_int_br

headers = ['interface', 'address', 'status', 'protocol']

#Заголовки у нас есть, получаем список кортежей со значениями
values_list = parse_sh_ip_int_br('sh_ip_int_br.txt')

#Создадим функцию
def convert_to_dict(h_list, v_list):
#Создаём пустые словарь и список
    dict_tmp = {}
    result = []
#Проходим по элементам (кортежам) списка, переданного нашей функции
    for tuples in v_list:
#О zip См. раздел "Полезные функции"
        dict_tmp = dict(zip(headers, tuples))
        result.append(dict_tmp)
    return(result)
#
pprint(convert_to_dict(headers, values_list))
