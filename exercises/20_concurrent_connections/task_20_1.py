# -*- coding: utf-8 -*-
"""
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
#Импортируем модули
from concurrent.futures import ThreadPoolExecutor
#Нам будет нужен модуль subprocess (описан в 12 главе)
import subprocess
from pprint import pprint
#--------------------------------------------------------------------------------------
#Создаём функцию
def ping_one_ip_only(ip_addr):
    '''
    Функция отправляет два ICMP пакета на один IP адрес
    Возвращает код ответа (0 - успех)
    '''
    reply = subprocess.run(['ping', '-c', '2', '-n', ip_addr],
                stdout=subprocess.DEVNULL)

    return(reply.returncode)
#--------------------------------------------------------------------------------------
#Создадим функцию
def ping_ip_addresses(ip_list, limit=3):

# В список Alive добавим доступные IP, в список Unreachable недоступные
# В кортеже result вернём получившиеся списки
    Alive_ls = []
    Unreachable_ls = []
    result = tuple()
    
    with ThreadPoolExecutor(max_workers=limit) as executor:

#  executor вызывает функцию ping_one_ip_only столько раз, сколько определено в limit
        result = executor.map(ping_one_ip_only, ip_list)

# У нас есть список IP-адресов и коды result, совмещаем их zip
# Если код '0', IP-адрес помещаем в список Alive_ls, иначе в Unreachable_ls
        for ip_addr, output in zip(ip_list, result):

            if output == 0:

                Alive_ls.append(ip_addr)

            else:

                Unreachable_ls.append(ip_addr)

    result = (Alive_ls, Unreachable_ls)

    return(result)
#--------------------------------------------------------------------------------------
if __name__ == '__main__':

#Создадим список IP-адресов, определим переменные:
#саму сеть, первое значение в четвёртом октете, максимальное число адресов
    ip_list = []
    ip_prefix = '10.0.3.'
    ip_start = 1
    ip_max = 5

#Заполним список IP-адресов. Предполагаем маску /24 и непрерывную последовательность адресов
    ip_list = [ip_prefix + str(num) for num in range(ip_start, ip_start + ip_max)]

    pprint(ping_ip_addresses(ip_list))
