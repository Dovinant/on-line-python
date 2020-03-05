# -*- coding: utf-8 -*-
'''
Задание 6.1a

Сделать копию скрипта задания 6.1.

Дополнить скрипт:
- Добавить проверку введенного IP-адреса.
- Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Incorrect IPv4 address'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

# Используем флаг, его проверяет цикл while
IP_CORRECT = False

while not IP_CORRECT:
# Цикл while повторяется пока IP_CORRECT = False
	IP_CORRECT = True
	print("Please input IP address")

	# Аргумент надо обязательно передавать в кавычках!
	Net = input(("For example '10.1.1.1': "))

	# Преобразуем строку в список, элементы разделяем по точке

	IP_LIST = Net.split('.')

	# Получаем длину списка

	LEN_IP = len(IP_LIST)
		
	if LEN_IP != 4:
	# Проверяем, что адрес содержит четыре октета
		print('Incorrect IPv4 address')
		IP_CORRECT = False
	else:
	# Преобразуем текстовые значения в цифровые

		IP_LIST = [int(IP_LIST[I]) for I in range(LEN_IP)]
		# Проходим по списку
		for OCT in IP_LIST:
			# Проверяем, что очередной октет больше нуля и меньше 255 
			if (OCT < 0 or OCT > 255):
				print('Incorrect IPv4 address')
				IP_CORRECT = False
				# прерываем цикл for и возобновляем цикл while
				break
	
'''
Проверяем, что первый октет в диапазоне больше 0, но меньше либо равно 223
Далее что он больше 223, но меньше либо равен 239
Потом что все октеты равны нулю, потом что все равны 255
'''

if (IP_LIST[0] > 0 and IP_LIST[0] <= 223):
	 print('unicast')
elif (IP_LIST[0] > 223 and IP_LIST[0] <= 239):
	 print('multicast')
elif (IP_LIST[0] == 0 and IP_LIST[1] == 0 and IP_LIST[2] == 0 and IP_LIST[3] == 0):
	 print('unassigned')
elif (IP_LIST[0] == 255 and IP_LIST[1] == 255 and IP_LIST[2] == 255 and IP_LIST[3] == 255):
	 print('local broadcast')
else:
	print('unused')