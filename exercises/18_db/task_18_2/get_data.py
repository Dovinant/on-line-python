import sqlite3
#from pprint import pprint
import sys
from tabulate import tabulate

def check_args(parametars):
    '''
    Функция проверяет переданные аргументы и возвращает SQL запрос
    '''
    if len(parametars) == 0:

        query = 'SELECT * FROM dhcp'

    elif len(parametars) == 2:

        key, value = parametars

        keys = ['mac', 'ip', 'vlan', 'interface', 'switch']

        try:

            keys.remove(key)

        except ValueError:

            print('Параметр "{}" не поддерживается'.format(key))

            print('Допустимые параметры: {}'.format(', '.join(keys)))

            sys.exit('!')
		
        query = 'SELECT * FROM dhcp WHERE {} = "{}"'.format(key, value)

    else:

        sys.exit('Пожалуйста, укажите либо два аргумента, либо ни одного.')

    return(query)

#------------------------------------------------------------------------------------------
#Получаем параметры, распакуем переменные
#в first попадёт имя нашего файла, в parametars всё остальное
first, *parametars = sys.argv[0:]

db_filename = 'dhcp_snooping.db'

#Отправляем параметры функции, забираем sql запрос
query = check_args(parametars)

conn = sqlite3.connect(db_filename)

#В result попадёт итератор
result = conn.execute(query)

#Если parametars не пуст, укажем какой получился фильтр вывода
#Правильность параметров уже проверили функцией check_args()
if parametars:

    print('\nИнформация об устройствах с таким значением {}: {}'.format(parametars[0], parametars[1]))

    print(tabulate(result))

else:

    print('\nЗаписи таблицы dhcp')

    print(tabulate(result))

conn.close()
