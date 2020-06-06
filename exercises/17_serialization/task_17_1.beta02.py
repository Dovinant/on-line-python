# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает
вывод команды show dhcp snooping binding из разных файлов и записывает обработанные данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21


Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
Первый столбец в csv файле имя коммутатора надо получить из имени файла, остальные - из содержимого в файлах.

"""

#Нам нужны модули re csv
import re
import csv
# И модуль pprint чтобы красиво отображать вывод
#from pprint import pprint

#Создадим функцию
def write_dhcp_snooping_to_csv(filenames, output):

#В первую группу попадёт МАС, во вторую IP, третья группа без захвата, потом номер VLAN, потом интерфейс
    regex = r'(\S+)\s+(\d+\.\d+\.\d+.\d+)\s+(?:\S+\s+\S+\s+)(\d+)\s+(\S+)'

#Создадим список заголовков
    headers = ['switch', 'mac', 'ip', 'vlan', 'interface']

#Откроем целевой файл для записи
    dest = open(output, 'w')

#Запишем в файл заголовки в формате csv
    writer = csv.writer(dest)
    writer.writerow(headers)

#Закроем файл. Пока он содержит только заголовки
    dest.close()

#Перебираем имена файлов с выводом команды 'show dhcp snooping binding'
    for names in filenames:
	
#Имя коммутатора получим из имени переданного нам файла
#Делаем срез до символа '_'
#line = 'sw1_dhcp_snooping.txt'
#line[:line.find('_')] вернёт 'sw1'
        host = names[:names.find('_')]
		
#Теперь откроем файл с выводом команды 'show dhcp snooping binding'
#и файл для записи результата. Последний файл открываем в режиме 'a'(append)
#В нём уже есть заголовки, теперь дописываем в него результат обработки исходного файла
        with open(names) as src, open(output, 'a') as dest:
		
#Функция finditer отлично подходит для обработки тех команд, вывод которых отображается
#столбцами.
            match = re.finditer(regex, src.read())
            list_tmp = []
			
#В match теперь находится итератор, пройдём по нему
#Метод groups() возвращает кортеж со строками, в котором элементы - это те подстроки,
#которые попали в соответствующие группы
#Кортеж преобразуем в список, в начало списка добавим имя устройства
            for m in match:
                list_tmp = list(m.groups())
                list_tmp.insert(0, host)
				
#Запишем в файл результат обработки
                writer = csv.writer(dest)
                writer.writerow(list_tmp)
	
#
#Формируем список файлов и вызываем функцию
filenames = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']

write_dhcp_snooping_to_csv(filenames, 'dhcp_snooping.csv')
