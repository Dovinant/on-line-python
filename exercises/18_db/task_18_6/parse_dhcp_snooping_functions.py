#
#Импортируем модули
import sqlite3
import os
import sys
import yaml
import re
from tabulate import tabulate
#from datetime import timedelta, datetime
#from pprint import pprint

#Модуль glob находит все пути, совпадающие с заданным шаблоном в соответствии с правилами, используемыми оболочкой Unix.
#import glob

#------------------------------------------------------------------------------------------

def check_db_file_exists(db_file):
    '''
    Функция проверяет есть ли файл базы данных, и, если нет, прерывает работу скрипта
    '''
    #Есть ли файл БД?

    if not (os.path.exists(db_file)):

        sys.exit('Не могу найти файл базы данный "{}"!\nОперация прервана.'.format(db_file))

#------------------------------------------------------------------------------------------

def read_yaml(yaml_file):
    '''
    Функция считывает yaml-файл, возвращает список кортежей
    '''
    result = []

#Функция принимает список файлов. Проходим по списку, считываем каждый файл
    for next_file in yaml_file:

        with open(next_file) as f:

#В template будет словарь словарей
            template = yaml.safe_load(f)

#Проходим по словарям, извлекаем hostname и location,
#записываем их кортежами в список result
            for key, sw_l_dict in template.items():
	
                for key, value in sw_l_dict.items():
		
                    result.append((key, value))
			
    return(result)

#------------------------------------------------------------------------------------------

def read_dhcp_snooping(dhcp_sng_files):
    '''
    Функция считывает файлы вывода команды sh ip dhcp snooping binding
    Функция возвращает список котежей
    '''
#Создаём регулярное выражение. В первую группу попадёт mac, во вторую IP, в третью vlan, в четвёртую interface
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

    result = []

#Функция получает список файлов. Проходим по списку, открываем каждый файл, считываем его построчно в line,
#и применяем скомпилированное регулярное выражение. Функция search() вернёт все найденные группы в виде итератора

    for filename in dhcp_sng_files:
	
#Имя коммутатора получим из имени переданного нам файла
#метод os.path.basename() вернёт имя файла без пути к нему
        host = os.path.basename(filename)
		
#Делаем срез до символа '_'
#line = 'sw1_dhcp_snooping.txt'
#line[:line.find('_')] вернёт 'sw1'
        host = host[:host.find('_')]
	
        with open(filename) as f:

            for line in f:
			
#Ищем информацию в очередной строке файла
                match = regex.search(line)

#Если нашли, match.groups() вернёт кортеж из значений попавших в группы
#Кортеж преобразуем в список, в список добавим имя хоста и еднинцу для поля active
#превратим список обратно в кортеж и добавим всё это в result
                if match:

                    tuple_list = list(match.groups())

                    tuple_list.append(host)

                    tuple_list.append(1)

                    result.append(tuple(tuple_list))

#result - это список кортежей			
    return(result)
	
#------------------------------------------------------------------------------------------

def create_db(db_name, db_schema):
    '''
    На основе переданной схемы
    Функция создаёт базу данных, если её ещё нет.
    '''
#Проверяем, что есть файл схемы
    if not (os.path.exists(db_schema)):
	
        sys.exit('Не могу найти файл схемы "{}"!\nОперация прервана.'.format(db_schema))
	
#Проверяем, что ещё нет такой БД
    if not (os.path.exists(db_name)):

        conn = sqlite3.connect(db_name)

        with open(db_schema) as f:

            schema = f.read()

        conn.executescript(schema)

        conn.close()

    else:

        print('\nБаза данных {} уже существует'.format(db_name))
	
#------------------------------------------------------------------------------------------

def add_data_switches(db_file, yaml_file):
    '''
    Функция добавляет данные в таблицу switches.
    Функция принимает имя БД и список yaml-файлов.
    Список файлов функция отдаёт функции read_yaml(), получает от неё список кортежей.
    Функция записывает данные из кортежей в БД.
    '''
#Проверяем, что БД существует
    check_db_file_exists(db_file)

#Вызываем функцию read_yaml, запоминаем данные для записи в таблицу switches
    sw_data = read_yaml(yaml_file)

#Добавим полученную информацию в таблицу switches.
#Обрабатывать исключения нам не надо, применим 'INSERT OR REPLACE'
#Используем менеджер контекста with conn:

    conn = sqlite3.connect(db_file)

    with conn:
	
        query = 'INSERT OR REPLACE into switches values (?, ?)'
		
        conn.executemany(query, sw_data)
		
    conn.close()

#------------------------------------------------------------------------------------------

def add_data(db_file, filename):
    '''
    Функция добавляет данные в таблицу dhcp.
    Аргументы имя БД и список файлов содержащих вывод команды.
    Эта функция с помощью функцию read_dhcp_snooping() получает данные для записи.
    '''
#Проверяем, что БД существует
    check_db_file_exists(db_file)

#Запоминаем данные для записи в таблицу dhcp
    dhcp_data = read_dhcp_snooping(filename)

    conn = sqlite3.connect(db_file)

#Во всех записях поле active выставим в 0
#У новых данных в этом поле окажется единица см. функцию read_dhcp_snooping()
#У старых, т.е. не активных, останется ноль
    conn.execute('UPDATE dhcp SET active = 0')

#Обрабатывать каждую строку нам не надо, поэтому применим executemany()
    with conn:

#Просто добавили datetime('now'), вот и всё!	
        query = "INSERT OR REPLACE INTO dhcp VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"
		
        conn.executemany(query, dhcp_data)
		
    conn.close()

#------------------------------------------------------------------------------------------

def get_data(db_file, key, value):
    '''
    Функция извлекает данные из таблицы dhcp.
    Применяет фильтр на основе переданных параметров.
    '''
#query_a запрашивает активные записи, query_p неактивные
    query_a = 'SELECT * FROM dhcp WHERE {} = "{}" AND active = 1'.format(key, value)
    query_p = 'SELECT * FROM dhcp WHERE {} = "{}" AND active = 0'.format(key, value)

#Вызываем функцию print_data()
#Она выведет информацию на основе запросов	
    print_data(db_file, query_a, query_p)

#------------------------------------------------------------------------------------------

def get_all_data(db_file):
    '''
    Функция извлекает все данные из таблицы dhcp.
    '''
#query_a запрашивает активные записи, query_p неактивные
    query_a = 'SELECT * FROM dhcp WHERE active = 1'
    query_p = 'SELECT * FROM dhcp WHERE active = 0'
	
#Вызываем функцию print_data()
#Она выведет информацию на основе запросов	
    print_data(db_file, query_a, query_p)

#------------------------------------------------------------------------------------------

def print_data(db_file, query_a, query_p):
    '''
    Функция выводит информацию из БД.
    Функция принимает имя файла БД и запросы к ней.
    '''
#Проверяем, что БД существует
    check_db_file_exists(db_file)
	
#Подключаемся к БД
    conn = sqlite3.connect(db_file)

#Нам нужен будет метод fetchall(), а он есть только у курсора
    cursor = conn.cursor()

#Выполняем запрос, извлекаем все строки из запроса метод fetchall()
    cursor.execute(query_a)

    result_a = cursor.fetchall()

    cursor.execute(query_p)

    result_p = cursor.fetchall()

    print('\nАктивные записи:\n')
    print(tabulate(result_a))

    if result_p:
        print('\nНеактивные записи:\n')
        print(tabulate(result_p))

    conn.close()
