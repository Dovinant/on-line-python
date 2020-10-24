# -*- coding: utf-8 -*-

"""
Задание 22.1b

Изменить класс Topology из задания 22.1a или 22.1.

Добавить метод delete_link, который удаляет указанное соединение.
Метод должен удалять и зеркальное соединение, если оно есть (ниже пример).

Если такого соединения нет, выводится сообщение "Такого соединения нет".

Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление линка:
In [9]: t.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление зеркального линка: в словаре есть запись ``('R3', 'Eth0/2'): ('R5', 'Eth0/0')``,
но вызов delete_link с указанием ключа и значения в обратном порядке, должно удалять соедине
ние:

In [11]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))

In [12]: t.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3')}

Если такого соединения нет, выводится сообщение:
In [13]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
Такого соединения нет

"""
from pprint import pprint


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        dict_result = {}
        for key, value in topology_dict.items():
            if value not in dict_result:
                dict_result[key] = value
        return dict_result

    def delete_link(self, link_left, link_right):
        if link_left in self.topology and self.topology[link_left] == link_right:
            pprint(self.topology[link_left])
        elif link_right in self.topology and self.topology[link_right] == link_left:
            pprint(self.topology[link_right])
        else:
            print('Такого соединения нет.')


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

top = Topology(topology_example)
# pprint(top.topology)
top.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
top.delete_link(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
top.delete_link(('R1', 'Eth0/0'), ('SW10', 'Eth0/1'))

'''
https://qastack.ru/programming/9323749/python-check-if-one-dictionary-is-a-subset-of-another-larger-dictionary
В python3 можно проверить что один словарь явлется подмножеством другого словаря
d1 = {'aa':'bb', 'cc':'dd', 'ee':'ff'}
d2 = {'aa':'bb'}
d2.items() <= d1.items()
True

Если бы метод delete_link принимал словарь, можно было бы воспользоваться.
'''