# -*- coding: utf-8 -*-
'''
Задание 4.3

Получить из строки CONFIG список VLANов вида:
['1', '3', '10', '20', '30', '100']

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

CONFIG = 'switchport trunk allowed vlan 1,3,10,20,30,100'

# Используем метод split - см. стр. 97 учебника. По-умолчанию этот медот делит строку по пробелам

commands = CONFIG.split() # Сохранили результат в переменную commands

# Теперь к переменной commands применяем опять метод split, только берём последний элемент (-1) и делим его по запятым

VLANS = commands[-1].split(',') # Результат сохраняем в переменную VLANS
print(VLANS) # смотрим что получилось