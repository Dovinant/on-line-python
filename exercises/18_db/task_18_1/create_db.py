'''
Проверяем, что есть файл базы даных dhcp_snooping.db.
Если нет, то создаём БД по схеме из файла dhcp_snooping_schema.sql.

В БД должно быть две таблицы:
switches - в ней находятся данные о коммутаторах
dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Аргументы скрипту не передаём.
'''
#Импортируем модули
import sqlite3
import os

#Скрипту не передаём аргументы, поэтому присвоим переменным имена файлов
#data_filename = 'dhcp_snooping.txt'
db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

#Есть ли файл БД?
db_exists = os.path.exists(db_filename)

#Создаём соединение с БД

conn = sqlite3.connect(db_filename)

if not db_exists:

    print('Создаю базу данных...')

    with open(schema_filename) as f:

        schema = f.read()

    conn.executescript(schema)

else:

    print('База данных существует')
