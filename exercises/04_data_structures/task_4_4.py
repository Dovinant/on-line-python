# -*- coding: utf-8 -*-
'''
Задание 4.4

Из строк command1 и command2 получить список VLANов,
которые есть и в команде command1 и в команде command2.

Для данного примера, результатом должен быть список: [1, 3, 100]
Этот список содержит подсказку по типу итоговых данных.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

command1 = 'switchport trunk allowed vlan 1,3,10,20,30,100'
command2 = 'switchport trunk allowed vlan 1,3,100,200,300'


# Опять задействуюем метод split() чтобы разделить строку на элементы и получить список
command11 = command1.split()
command22 = command2.split()

# К последнему элементу списока, содержащему VLANs опять прменяем метод split() только раздлителем будет запятая

VLANS11 = command11[-1].split(',')
VLANS22 = command22[-1].split(',')

# Создаём множества

SET1 = set(VLANS11)
SET2 = set(VLANS22)

# Получаем пересечение множеств

SET_Int = SET1.intersection(SET2)

# Из множества получаем список и каждый элемент списка преобразуем в число

LIST_FIN = [int(list(SET_Int)[i]) for i in range(3)]

'''
Можно было бы оптимизировать преобразование так:
Сначала узнаём число элеметов множества

A = len(SET_Int)

Затем подставляем это значение в комманду

LIST_FIN = [int(list(SET_Int)[i]) for i in range(A)]

или так

LIST_FIN = [int(list(SET_Int)[i]) for i in range(len(SET_Int))]

но мы метод len() не изучали
'''

# Сортируем список

LIST_FIN.sort()