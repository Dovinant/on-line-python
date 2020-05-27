# -*- coding: utf-8 -*-
'''
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''
#Нам нужен модуль re
import re

#Создадим функцию
def get_ip_from_cfg(file_name):

#Создаём регулярное выражение
#В первую группу (\d+.\d+.\d+.\d+) поподёт IP, во вторую MASK

    regex = (r'ip address (\d+.\d+.\d+.\d+) (\d+.\d+.\d+.\d+)')

#Создадим пустой список. Потом в него поместим кортежи

    result = []
	
#Открываем файл построчно

    with open(file_name) as f:
        for line in f:
            match = re.search(regex, line)
            if match:
#Создаём кортеж и добавляем его в список
                tuple_r = (match.group(1), match.group(2))
                result.append(tuple_r)
    return(result)
#

print(get_ip_from_cfg('config_r1.txt'))