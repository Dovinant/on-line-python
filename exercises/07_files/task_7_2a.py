# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

# Принимаем от пользователя имя файла

FileName = input('Type the file name, please: ')

# Открываем файл.
# Если файл не найден, сообщаем об этом
'''
Дальше считываем строку из файла, выставляем Flag = True
Внутри запускаем ещё один цикл for - он берёт слово из списка ignore
Если это слово оказывается в текущей строке
или строка начинается с "!", то Flag = False и
не выбирать другие слова  из списка ignore - оператор break
'''	

try:

	File = open(FileName, 'r')
	for Line in File:
		Flag = True
		for World in ignore:
			if (World in Line or Line.startswith('!')):
				Flag = False
				break
		# Если Flag = True, печатаем содержимое файла, заменив '!' на пустую строку
		# и методом rstrip() убираем лишний перевод коретки
		if Flag:
			print(Line.rstrip())
	
	# Закрываем файл

	File.close()
	
except FileNotFoundError:
	
	print('File "{}" not found'.format(FileName))

