# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'

# Сначала из исходной строки убираем ненужные символы '[', ']', ',' и заменяем 'O' на 'OSPF'.
# Для этого несколько раз применим метод replace() к исходной строке

ospf_route =  ospf_route.replace(',', '')
ospf_route =  ospf_route.replace('[', '')
ospf_route =  ospf_route.replace(']', '')
ospf_route =  ospf_route.replace('O', 'OSPF')

# Преобразуем строку в список

ospf_route_list = ospf_route.split()

# Создаём образец для вывода:

ip_template = '''
    ...: Protocol:             {:<18}
    ...: Prefix:               {:<18}
    ...: AD/Metric:            {:<18}
    ...: Next-Hop:             {:<18}
    ...: Last update:          {:<18}
    ...: Outbound Interface:   {:<18}
    ...: '''

# И выводим

print(ip_template.format(ospf_route_list[0], ospf_route_list[1], ospf_route_list[2], ospf_route_list[3], ospf_route_list[4], ospf_route_list[5]))

#
'''
Не придумал как красивее определить вывод. Конструкция типа

print(ip_template.format(ospf_route_list[i] for i in range(6)))

не работает
'''
