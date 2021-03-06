# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

# Создаём список символов, которые надо земенить в каждой строке

CharReplace = [',', '[', ']', 'O']

# Открываем файл конструкцией with

with open('ospf.txt', 'r') as f:
	# Для каждой строки
	for line in f:
		# Сначала из исходной строки убираем ненужные символы '[', ']', ',' и заменяем 'O' на 'OSPF'.
		# 'O' меняем на 'OSPF', остальные символы на пустую строку
		for Char in CharReplace:
			if Char == 'O':
				line = line.replace(Char, 'OSPF')
			else:
				line = line.replace(Char, '')

		# Преобразуем строку в список

		line_list = line.split()

		# Создаём образец для вывода:

		ip_template = '''
			Protocol:             {:<18}
			Prefix:               {:<18}
			AD/Metric:            {:<18}
			Next-Hop:             {:<18}
			Last update:          {:<18}
			Outbound Interface:   {:<18}
			'''

		# И выводим

		print('\n================================================================')
		print(ip_template.format(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]))

'''
На будущее.
Попробовать преобразовать строку в словарь, где ключи будут Protocol, Prefix, AD/Metric и так далее.
Потом выводить на печать словарь Ключ - Значение.
Пример есть в книге на стр. 166(там разбирается цикл for)
'''

