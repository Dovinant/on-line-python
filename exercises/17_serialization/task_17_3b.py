# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно, чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии, но и удалять дублирующиеся соединения
(их лучше всего видно на схеме, которую генерирует draw_topology).

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии с помощью функции draw_topology.
Не копировать код функции draw_topology.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть дублирующихся линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
#Нам нужны модули pprint yaml
from pprint import pprint

import yaml

#Импортируем функцию draw_topology из файла draw_network_graph.py
from draw_network_graph import draw_topology

#Создадим функцию
def transform_topology(topology_yaml):

    result = {}

    del_key = []

#Открываем файл, считываем его
    with open(topology_yaml) as f:

        templates = yaml.safe_load(f)

        for key, value in templates.items(): #Внешний словарь

            for intf_l, neighbors in value.items(): #Вложенный словарь уровня второго

                for hostname, intf_r in neighbors.items(): #Вложенный словарь уровня трерьего

                    result[(key, intf_l)] = (hostname, intf_r) #Итоговый словарь

                    del_key.append((hostname, intf_r)) #Контрольный список

                    for key_ls in del_key: #Проходим по списку

                        if (key, intf_l) == key_ls: #Если в списке обнаружили ключ словаря

                            del(result[(key, intf_l)]) #Удаляем эту запись из словаря

                            break

    return(result)
	

#Вызовем функцию, нарисуем топологию
topology_dict = transform_topology('topology.yaml')

draw_topology(topology_dict)

'''
Внешний словарь, его ключ имя локального устройства, значение - словарь уровня два.
Словарь уровня два, его ключ имя локального интерфейса, значение - словарь уровня три.
Словарь уровня три, его ключ имя соседа, значение - интерфейс соседа.

Записи в словаре дублируются когда ключ словаря и его значение меняются местами
т.е. когда в словарь помещается запись ключ-значение, а потом ещё одна запись
у которой ключ это значение нашей записи, а значение есть ключ нашей записи. Таким образом
описывается одно и тоже соединение между двумя устройствами.
Так получается когда мы последовательно обрабатываем вывод команды show cdp neighbors на соседних устройствах
Чтобы избавится от дублирования создаём список del_key, в него помещаем значения словаря

Дальше в цикле key_ls in del_key берём ключ из словаря result и последовательно сравниваем со всеми значениями
списка del_key). Совпадение говорит о том,
что в словарь result помещена запись описывающая уже имеющееся в нём соединение. Удаляем её.

Подобная задача уже была: смотри task_11_2.py
'''