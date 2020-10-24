# -*- coding: utf-8 -*-

"""
Задание 22.1a

Скопировать класс Topology из задания 22.1 и изменить его.

Перенести функциональность удаления дублей в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:
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
topology_example_2 = {
    ("R10", "Eth0/0"): ("SW10", "Eth0/1"),
    ("R20", "Eth0/0"): ("SW10", "Eth0/2"),
    ("R20", "Eth0/1"): ("SW20", "Eth0/11"),
    ("R30", "Eth0/0"): ("SW10", "Eth0/3"),
    ("R30", "Eth0/1"): ("R40", "Eth0/0"),
    ("R30", "Eth0/2"): ("R50", "Eth0/0"),
    ("SW10", "Eth0/1"): ("R10", "Eth0/0"),
    ("SW10", "Eth0/2"): ("R20", "Eth0/0"),
    ("SW10", "Eth0/3"): ("R30", "Eth0/0"),
}

top = Topology(topology_example)
pprint(top.topology)
top_2 = Topology(topology_example_2)
pprint(top_2.topology)
