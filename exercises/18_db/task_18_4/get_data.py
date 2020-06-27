import sqlite3
#from pprint import pprint
import sys
from tabulate import tabulate

def check_args(parametars):
    '''
    Функция проверяет переданные аргументы и возвращает SQL запрос
    '''
    if len(parametars) == 0:

        query_a = 'SELECT * FROM dhcp WHERE active = 1'
        query_p = 'SELECT * FROM dhcp WHERE active = 0'

    elif len(parametars) == 2:

        key, value = parametars

        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']

        try:

            keys.remove(key)

        except ValueError:

            print('Параметр "{}" не поддерживается'.format(key))

            print('Допустимые параметры: {}'.format(', '.join(keys)))

            sys.exit('!')
		
        query_a = 'SELECT * FROM dhcp WHERE {} = "{}" AND active = 1'.format(key, value)
        query_p = 'SELECT * FROM dhcp WHERE {} = "{}" AND active = 0'.format(key, value)

    else:

        sys.exit('Пожалуйста, укажите либо два аргумента, либо ни одного.')

    return(query_a, query_p)

#------------------------------------------------------------------------------------------
#Получаем параметры, распакуем переменные
#в first попадёт имя нашего файла, в parametars всё остальное
first, *parametars = sys.argv[0:]

db_filename = 'dhcp_snooping.db'

#Отправляем параметры функции, забираем sql запрос
query_a, query_p = check_args(parametars)

#Подключаемся к БД
conn = sqlite3.connect(db_filename)

#Нам нужен будет метод fetchall(), а он есть только у курсора
cursor = conn.cursor()

#В result попадёт итератор
#Выполняем запрос, извлекаем все строки из запроса метод fetchall()
cursor.execute(query_a)

result_a = cursor.fetchall()

cursor.execute(query_p)

result_p = cursor.fetchall()

#Если parametars не пуст, укажем какой получился фильтр вывода
#Правильность параметров уже проверили функцией check_args()
if parametars:

    print('\nИнформация об устройствах с таким значением {}: {}'.format(parametars[0], parametars[1]))

    print('\nАктивные записи:\n')
    print(tabulate(result_a))

#Если result_p не пуст, значит есть записи о неактивных MAC адресах
#выведем их.
#Поэтому нам и нужен cursor.fetchall(). Если просто написать result_p = conn.execute(query_p)
#в result_p будет курсор! Даже если в нём ничего нет, всё равно сам объект курсор есть!
#А через result_p = cursor.fetchall() в result_p окажется список кортежей или ничего.
    if result_p:

        print('\nНеактивные записи:\n')
        print(tabulate(result_p))


else:

    print('\nАктивные записи:\n')
    print(tabulate(result_a))

    if result_p:
        print('\nНеактивные записи:\n')
        print(tabulate(result_p))

conn.close()
'''
fetchmany(size=cursor.arraysize) - извлекает определённое число строк из выполненного запроса.
В учебники сказано, что по умолчанию size=cursor.arraysize,
однако, вот здесь https://codecamp.ru/documentation/python/4240/database-access
пишут If size is omitted, fetchmany returns a single row. 
'''