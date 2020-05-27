# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''
#Нам нужен модуль re
import re
# И модуль pprint чтобы красиво отображать вывод
from pprint import pprint

#Создадим функцию
def parse_sh_ip_int_br(file_name):

#Определим регулярное выражение
#В первую группу поадёт всё до первого пробела
#Во вторую цифра с точкой один или более раз, либо цифра/буква/подчёркивание
#Во вторую группу поподёт IP либо слово 'unassigned'
#Далее символы до пробела, опять символы до пробела, пробелы
#В третью группу поподёт Status
#В четвёртую Protocol

    regex = (r'(\S+) +'
            r'([\d.]+|\w+) +'
            r'\w+ \w+ +'
            r'(up|down|administratively down) +'
            r'(up|down)')

#Файл разберём целиком, а не построчно
    with open(file_name) as f:
#Создадим список куда добавим кортежи	
        result = []
#Функция finditer отлично подходит для обработки тех команд, вывод которых отображается
#столбцами.	
        match = re.finditer(regex, f.read())
#В match теперь находится итератор, пройдём по нему
#Метод groups() возвращает кортеж со строками, в котором элементы - это те подстроки,
#которые попали в соответствующие группы
        for m in match:
            result.append(m.groups())

    return(result)

#Не экспортируем эту часть если кому-то понадобиться функция из этого файла
if __name__ == '__main__':
#Вызовем функцию
    pprint(parse_sh_ip_int_br('sh_ip_int_br.txt'))
