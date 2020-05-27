# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

#Нам нужен модуль re
import re
# И модуль pprint чтобы красиво отображать вывод
from pprint import pprint

#Создадим функцию
def get_ints_without_description(file_input):

#Регулярное выражение ищет или строку interface или пробел и слово description
    regex = (r'(interface \S+)|(?P<description> +description)')
	
#Дальше нужена функция match - она ищет совпадение вначале строки
#Метод lastgroup возвращает ИМЯ последней найденной группы (поэтому вторая группа у нас именованная)
#в список сначала попадёт имя интерфейса, затем, если у интерфейса есть description,
#удалим это имя из списка методом pop(), если же description нет, имя останется в списке
    with open(file_input) as src:
        result = []
        for line in src:
            match = re.match(regex, line)
            if match:
                if match.lastgroup == 'description':
                    result.pop()
                else:
                    result.append(match.group(1))
    return(result)	
#
pprint(get_ints_without_description('config_r1.txt'))
