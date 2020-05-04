# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

#Нам будет нужен модуль subprocess
import subprocess

#Создаём функцию
def ping_ip_addresses(ip_list):

# В список Alive добавим доступные IP, в список Unreachable недоступные
# В кортеже result вернём получившиеся списки
    Alive_ls = []
    Unreachable_ls = []
    result = tuple()

# Проходим по списку ip_list, проверяем адреса, помещаем их в нужный список
    for ip_addr in ip_list:
# Пишем какой IP проверяем
        print("Let's check the " + ip_addr)
        reply = subprocess.run(['ping', '-c', '2', '-n', ip_addr],
                stdout=subprocess.DEVNULL)
        if reply.returncode == 0:
            Alive_ls.append(ip_addr)
        else:
            Unreachable_ls.append(ip_addr)
#
    result = (Alive_ls, Unreachable_ls)
    return(result)
	
#Этот список адресов передадим функции
ip_list = ['8.8.8.8', '192.168.3.1', '10.0.3.1', '10.0.17.17']

#Вызываем функцию
print(ping_ip_addresses(ip_list))
