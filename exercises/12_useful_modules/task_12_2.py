# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''
#Нам понадобится модуль ipaddress
import ipaddress

#Создаём функцию
def convert_ranges_to_ip_list(ip_list_range):
#В ip_list запишем итоговые адреса
    ip_list = []
    for ip_addr in ip_list_range:
#Если есть символ "-", значит, нам передали диапазон
        if ip_addr.find('-') >= 0:
#Строку преобразуем в список, делим по "-"
            tmp_ls = ip_addr.split('-')
#Первый элемент списка есть IP адрес, записываем его в объект ip1
            ip1 = ipaddress.ip_address(tmp_ls[0])
#Если во втором элементе есть точка, значит это тоже IP, правая граница диапазона
            if (tmp_ls[1].find('.')) >= 0:
#Запоминаем правую границу в объект ip2
                ip2 = ipaddress.ip_address(tmp_ls[1])
            else:
#Иначе это конструкция типа '1.1.1.1-3', второй элемент списка tmp_ls просто число
#Формируем полноценный IP адрес, правую границу диапазона, запоминаем в ip2
                ip2 = ip1 + int(tmp_ls[1]) - 1
#В цикле while заполняем список адресами
            while ip1 <= ip2:
                ip_list.append(str(ip1))
                ip1 = ip1 + 1
#Иначе у нас просто IP адрес, записываем его в список
        else:
            ip_list.append(ip_addr)
#
    return(ip_list)

#Список для функции
ip_list_range = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']
#Вызываем функцию
print(convert_ranges_to_ip_list(ip_list_range))
