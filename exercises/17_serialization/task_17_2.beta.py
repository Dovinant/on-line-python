# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv), в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob

sh_version_files = glob.glob("sh_vers*")
# print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

#------------------------------------------------------------------------------------------------
#Нам нужны модули re csv
import re
import csv
from pprint import pprint

#Функция parse_sh_version:
#ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
def parse_sh_version(line):

    ios = r'Version ([1-9.()A-Z]+)'
    match  = re.search(ios, line)
    ios = match.group(1)

    image = r'((?:flash|disk)\d?:[a-zA-Z0-9-.]+)'
    match  = re.search(image, line)
    image = match.group(1)

    uptime = r'(\d+ days, \d+ hours, \d+ minutes)'
    match  = re.search(uptime, line)
    uptime = match.group(1)

    result = (ios, image, uptime)

    return(result)

#regex= r'(flash:\S+)|(\d+ days, \d+ hours, \d+ minutes)|Version ([1-9.()A-Z]+)'

#Функция write_inventory_to_csv должна делать следующее:
#обработать информацию из каждого файла с выводом sh version
def write_inventory_to_csv(data_filenames, csv_filename):

    list_csv = []
    list_tmp = []
    list_csv.append(headers)
	
    for filenames in data_filenames:
	
        hostname = re.search(r'sh_version_(\w+)', filenames).group(1)
	
#hostname = filenames[:filenames.find('.')]
#hostname = hostname.split('_')[-1]

        f = open(filenames)
		
        list_tmp = list(parse_sh_version(f.read()))
		
        list_tmp.insert(0, hostname)

        list_csv.append(list_tmp)
		
        f.close()

#    pprint(list_csv)

    with open(csv_filename, 'w') as f:

        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

        writer.writerows(list_csv)

#
write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')
