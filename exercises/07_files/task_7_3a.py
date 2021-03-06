# -*- coding: utf-8 -*-
'''
Задание 7.3a

Сделать копию скрипта задания 7.3.

Дополнить скрипт:
- Отсортировать вывод по номеру VLAN


Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
# Открываем файл
File = open('CAM_table.txt', 'r')

'''
Далее нам понадобятся два списка: List и List_Clear.
Перебираем файл построчно, методом rstrip() убираем символы перевода строки,
методом split() преобразуем текущую строку в список.
Список может оказаться пустым, но пустой список сам по себе считается ложным
в тестировании истинного значения: List = False, если он пустой.
Так же проверяем первый элемент списка и, если это число, т.е. номер VLAN,
добавляем строку как элемент в новый список List_Clear.
Внимание! Элементы List это слова текущей строки,
а элементы List_Clear - сами строки!
'''

List_Clear = []

for Line in File:
	List = Line.rstrip().split()
	if  (List and List[0].isdigit()):
		List_Clear.append(Line)

'''
Сортируем получившийся список, из элементов списка формируем строку
и выводим её на печать
'''
List_Clear.sort()
Line = ''.join(List_Clear)
print(Line)

File.close()
