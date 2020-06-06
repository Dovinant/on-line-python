# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (пример mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.

Для части пользователей запись только одна и тогда в итоговый файл надо записать только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_datetimestr_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.

Функцию convert_datetimestr_to_datetime использовать не обязательно.

"""

import datetime


def convert_datetimestr_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

#-----------------------------------------------------------------------------------------

#Нам нужен модуль csv
import csv
#from pprint import pprint

#Создадим функцию
def write_last_log_to_csv(source_log, output):

    dict_tmp = {}
	
    result = []

#Открываем переданный файл, считываем, заголовки помещаем в отдельный объект headers
    with open(source_log) as src, open(output, 'w') as dest:

        reader = csv.reader(src)

        result.append(next(reader))

#Итератор reader преобразуем в список
        list_tmp = list(reader)

#Перебираем элементы списка списков. Берём очередной список, последний его элемент
#(дату) функцией convert_datetimestr_to_datetime преобразуем в объект datetime
#и вставляем его в конец текущего списка. Так мы получили элемент по которому будем сортировать списки
        for items in list_tmp:

            items.append(convert_datetimestr_to_datetime(items[2]))
			
#Отсортируем наш список списков. Параметру key функции sort() передаём последний элемент
#текущего списка - объект datetime. По ним и сортируем.
        list_tmp.sort(key = lambda row: row[-1])

        for row in list_tmp:
		
#Теперь удалим из каждого списка объект datetime
#функция pop() по умолчанию удаляет последний элемент списка
            row.pop()

#И создадим словарь с ключём почта пользователя. Так получим уникальные записи для каждого пользователя.
#А так как записи уже отсортированы по времени, получим для каждого пользователя последнюю запись смены имени

            dict_tmp[row[1]] = row
			
#Теперь в список result добавляем уникальные записи из словаря
        for key, value in dict_tmp.items():

            result.append(value)

#Печатаем список
        writer = csv.writer(dest, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerows(result)


#Вызовем функцию
write_last_log_to_csv('mail_log.csv', 'mail_log_filtred.csv')

'''
#Значение параметра key должно быть функцией, принимающей один аргумент и возвращающей ключ для сортировки.
#Применяем лямбда-функцию, передаём ей очередной элемент, список, и из этого списка берём последний элемент,
#т.е. объект datetime. По нему и сортируем наш список списков.
#Ещё есть функции модуля operator https://tproger.ru/translations/python-sorting/
#И ещё о сортировке списков https://www.rupython.com/python-1397-13965.html
'''
