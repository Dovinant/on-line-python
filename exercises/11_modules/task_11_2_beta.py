# -*- coding: utf-8 -*-
'''
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент список с именами файлов,
в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между устройствами.
Структура словаря такая же, как в задании 11.1:
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

В словаре, который возвращает функция create_network_map, не должно быть дублей.

С помощью функции draw_topology из файла draw_network_graph.py нарисовать схему на основании топологии,
полученной с помощью функции create_network_map.
Результат должен выглядеть так же, как схема в файле task_11_2a_topology.svg


При этом:
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме

Не копировать код функций parse_cdp_neighbors и draw_topology.

Ограничение: Все задания надо выполнять используя только пройденные темы.

> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz (внутри виртуального окружения именно так, без sudo!!)

'''
# Импортируем функции draw_topology и parse_cdp_neighbors
from draw_network_graph import draw_topology
from task_11_1 import parse_cdp_neighbors
# Создаём функцию
def create_network_map(filenames):
    # Создаём словари. result_right итоговый словарь
    # result_left принимает словарь от функции parse_cdp_neighbors
    result_right = {}
    result_left = {}
    key_list = []
    for item in filenames:
        file = open(item, 'r')
        result_left =  parse_cdp_neighbors(file.read())
        if result_right:
            for key, value in result_left.items():
                for k in result_right:
                    key_string = k

                    if key_string == value:
                        key_list.append(value)
                        break

        result_right.update(result_left)

    for items in key_list:
        del(result_right[items])
    return(result_right)
					

#
# Список с именами файлов
file_list = ['sh_cdp_n_sw1.txt', 'sh_cdp_n_r1.txt', 'sh_cdp_n_r2.txt', 'sh_cdp_n_r3.txt']
# Вызываем функцию. Принимаем результат в topology_dict
topology_dict = create_network_map(file_list)
#print(create_network_map(file_list))
# Рисуем схему
draw_topology(topology_dict)

'''
В цикле for item in filenames открываем файл из списка, считываем его содержимое в строку
и передаём её функции parse_cdp_neighbors. Функция возвращает словарь, помещаем его в result_left.
Проверяем итоговый словать result_right, и если он не пуст, циклом for считываем ключ и его значение
из словаря result_left. Внутренний цикл for перебирает ключи словаря result_right и сравниваем
со считанным знчением из словаря result_left. Если они совпали, значит строка в словаре result_left
описывает уже имеющееся в словаре result_right соседство. Запоминаем ключ этой строки (key) в 
переменную key_delete, делаем запись в списке key_list и останавливаем поиск в словаре result_right, совпадение может быть только одно.
Добавляем словарь result_left в result_right, проходим по списку key_list, берём ключи
и удаляем записи из словаря result_right
'''
