# -*- coding: utf-8 -*-
'''
Задание 18.5a

Для заданий 18 раздела нет тестов!

После выполнения задания 18.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active в некоторых записях и поставить
время 7 или более дней.

В файле задания описан пример работы с объектами модуля datetime.
Показано как получить дату 7 дней назад. С этой датой надо будет сравнивать время last_active.

Обратите внимание, что строки с датой, которые пишутся в БД, можно сравнивать между собой.

'''

from datetime import timedelta, datetime

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

#print(now)
#print(week_ago)
#print(now > week_ago)
#print(str(now) > str(week_ago))

#cursor = conn.cursor()

#correct_time = "UPDATE dhcp SET last_active = '2020-06-18 19:11:21' WHERE active = 0"
#cursor.execute(correct_time)

#--------------
#query = 'SELECT * FROM dhcp WHERE active = 0'
#cursor.execute(query)
#result_p = cursor.fetchall()

#for row in result_p:
#	print(str(week_ago) > row[6])

#--------------
#Нужен ли в этом случае cursor?
#query = 'SELECT * FROM dhcp WHERE last_active < ?'
##query = 'DELETE FROM dhcp WHERE last_active < ?'
#cursor.execute(query, (week_ago, ))

