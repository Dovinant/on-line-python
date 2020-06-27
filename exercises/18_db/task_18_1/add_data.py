'''
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding и информацию о коммутаторах.

В таблицу switches из файла switches.yml пишем сведения о коммутаторах.
Информацию из вывода команды sh ip dhcp snooping binding пишем в таблицу dhcp.
Сам вывод команды берём из трёх файлов sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.
Таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять.
Имя коммутатора определим по имени файла с данными вывода.

Аргументы скрипту не передаём.
'''
#Импортируем модули
import sqlite3
import os
import sys
import yaml
import re
#from pprint import pprint

#Модуль glob находит все пути, совпадающие с заданным шаблоном в соответствии с правилами, используемыми оболочкой Unix.
import glob

def check_db_file_exists(db_exists):
    '''
    Функция проверяет есть ли файл базы данных, и, если нет, прерывает работу скрипта
    '''
    if not db_exists:

        sys.exit('База данных не существует. Перед добавлением данных, ее надо создать.')
#------------------------------------------------------------------------------------------
def read_yaml(file_yaml):
    '''
    Функция считывает yaml-файл, возвращает список кортежей
    '''
    result = []

    with open(file_yaml) as f:

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
    '''
#Создаём регулярное выражение. В первую группу попадёт mac, во вторую IP, в третью vlan, в четвёртую interface
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

    result = []

#Функция получает список файлов. Проходим по списку, открываем каждый файл, считываем его построчно в line,
#и применяем скомпилированное регулярное выражение. Функция search() вернёт все найденные группы в виде итератора

    for filename in dhcp_sng_files:
	
#Имя коммутатора получим из имени переданного нам файла
#Делаем срез до символа '_'
#line = 'sw1_dhcp_snooping.txt'
#line[:line.find('_')] вернёт 'sw1'
        host = filename[:filename.find('_')]
	
        with open(filename) as f:

            for line in f:
			
#Ищем информацию в очередной строке файла
                match = regex.search(line)

#Если нашли, match.groups() вернёт кортеж из значений попавших в группы
#Кортеж преобразуем в список, в список добавим имя хоста, превратим список обратно в кортеж
#и добавим всё это в result
                if match:

                    tuple_list = list(match.groups())

                    tuple_list.append(host)

                    result.append(tuple(tuple_list))

#result - это список кортежей			
    return(result)
#------------------------------------------------------------------------------------------
#Имя файла БД
db_filename = 'dhcp_snooping.db'

#Список с именами файлов
dhcp_sng_files = glob.glob('*_dhcp_snooping.txt')

#Есть ли файл БД?
db_exists = os.path.exists(db_filename)

#Функция проверит что файл ДБ есть
check_db_file_exists(db_exists)

#Запоминаем данные для записи в таблицы switches и dhcp
sw_data = read_yaml('switches.yml')
dhcp_data = read_dhcp_snooping(dhcp_sng_files)

#Открываем БД
conn = sqlite3.connect(db_filename)

#Добавим полученную информацию в таблицу switches и обработаем исключение
#По условиям задачи мы должны регистрировать каждую попытку записать данные с неуникальным ключом
#пройдём в цикле по переданным данным, используем execute()
print('\nДобавляю данные в таблицу switches...')

for row in sw_data:

    try:

        with conn:
	
            query = 'INSERT into switches values (?, ?)'
		
            conn.execute(query, row)

    except sqlite3.IntegrityError as e:

        print("При добавлении данных '{}' Возникла ошибка: ".format(', '.join(row)), e)
	
#Добавим полученную информацию в таблицу dhcp и обработаем исключение
#По условиям задачи мы должны регистрировать каждую попытку записать данные с неуникальным ключом
#пройдём в цикле по переданным данным, используем execute()
print('\nДобавляю данные в таблицу dhcp...')

for row in dhcp_data:

    try:

        with conn:
	
            query = 'INSERT INTO dhcp VALUES (?, ?, ?, ?, ?)'
		
            conn.execute(query, row)

    except sqlite3.IntegrityError as e:

        print("При добавлении данных '{}' Возникла ошибка: ".format(', '.join(row)), e)

#Закрываем БД
conn.close()


'''
Не было бы требования добыть имя хоста из имени файла и добавить его в таблицу, решение было бы простым:
Функция findall() вернёт все найденные группы в виде списка кортежей.
Объединяем этот список со списком result и возвращаем его.
Именно объединяем result.extend(), а не result.append(). append() создаст список списков.

    for filename in dhcp_sng_files:
	
        with open(filename) as f:

            line = f.read()
			
            result.extend(regex.findall(line))
			
    return(result)
	
Обработка исключений:
Функция executemany() записывает или не записывает итератор целиком,
поэтому решение не вполне отвечает условиям задачи. Нам нужно указывать в случае ошибки какие имено строки не попали в БД
'''
