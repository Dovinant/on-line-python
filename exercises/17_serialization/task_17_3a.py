# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод команды show cdp neighbor из нескольких файлов
и записывает итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь в файл topology.yaml.

"""
#Нам нужны модули re pprint yaml
import re
from pprint import pprint
import yaml

#Модуль glob находит все пути, совпадающие с заданным шаблоном в соответствии с правилами, используемыми оболочкой Unix.
import glob

sh_cdp_files = glob.glob('sh_cdp_n_*')

#Создадим функцию
def generate_topology_from_cdp(list_of_files, save_to_filename=None):

    result = {}

#В первую группу попадает имя устройства, во вторую имя локального интерфейса, в третью его номер
#в четвёртую имя интерфейса соседнего устройства, в пятую его номер
    regex = r'(\w+)\s+(Eth|Fa[s]?|Gi|Ser) (\S+).*(Eth|Fa[s]?|Gi|Ser) (\S+)'
	
    for files in list_of_files: # Перебираем имена файлов

        with open(files) as f:
		
            dict_l_2 = {}

            line = f.read() #Считываем весь файл в одну строку

#Найдём имя нашего устройства.
            hostname = re.search(r'(\w+)[>#]', line).group(1)

#Список состоит из кортежей с нужной нам информацией
            list_result = re.findall(regex, line)
			
            for tuple_line in list_result:

                dict_l_3 = {}

                dict_l_3[f'{tuple_line[0]}'] = f'{tuple_line[3]} {tuple_line[4]}'

                dict_l_2[f'{tuple_line[1]} {tuple_line[2]}'] = dict_l_3

            result[hostname] = dict_l_2 # Итоговый (внешний) словарь
	
    if save_to_filename:

        with open(save_to_filename, 'w') as f_yaml:

            yaml.dump(result, f_yaml)
	
    return(result)
	
#Вызываем функцию. Т.к. вторй элемент необязателен, можем его не указывать
#pprint(generate_topology_from_cdp(sh_cdp_files))
pprint(generate_topology_from_cdp(sh_cdp_files, 'topology.yaml'))

'''
В словаре уровня три dict_l_3 ключ имя соседа, значение - его интерфейс.
В словаре уровня два dict_l_2 ключ имя локального интерфейса, значение - словарь уровня три

Функция re.findall возвращает список кортежей, если в регулярном выражении есть больше одной группы.
Первый элемент (индекс 0) получившегося списка есь имя соседа, второй (индекс 1) имя локального интерфейса (Eth),
третий элемент это номер локального интерфейса (0/0), четвёртый имя интерфейса соседа, пятый - номер этого интерфейса
'''