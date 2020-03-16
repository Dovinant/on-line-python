# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

# Принимаем от пользователя имя файла

FileName = input('Type the file name, please: ')

# Открываем файл.
# Если файл не найден, сообщаем об этом
'''
Потом считываем строку из файла, выставляем Flag = True
Внутри запускаем ещё один цикл for - он берёт слово из списка ignore
Если это слово оказывается в текущей строке, Flag = False и
не выбирать другие слова  из списка ignore - оператор break
'''	

# Здесь применим конструкцию with

try:
	with open(FileName, 'r') as src, open('config_sw1_cleared.txt', 'w') as dest:
		for Line in src:
			Flag = True
			for World in ignore:
				if World in Line:
					Flag = False
					break
		# Если Flag = True, копируем строку в файл-приёмник
			if Flag:
				dest.write(Line)
		
except FileNotFoundError:
	
	print('File "{}" not found'.format(FileName))
