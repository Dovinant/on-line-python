# -*- coding: utf-8 -*-
'''
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое файла в строку.

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}

В словаре интерфейсы должны быть записаны без пробела между типом и именем. То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

# Создаём функцию
def parse_cdp_neighbors(command_output):
# Создаём словарь
    result = {}
# Убираем из полученой строки слева и справа '\n'.
# Или потом это придётся делать для local_host и neighbors
    command = command_output.strip()
# В local_host запишем имя нашего устройста. Оно будет перед '>' или '#'
# Здесь мы ищем только позицию '>' и делаем срез строки
    local_host = command[0:command.find('>')]
#    local_host.strip()
# В neighbors запишем только вывод соседей.
# Для этого ноходим номер позиции элемента 'ID\n', добавляем к нему 3
# и делаем срез строки начиная с полученной позиции.
# Срез начнётся с имени первого соседа
    neighbors = command[command.find('ID\n') + 3 ::]
# Преобразуем строку в список. Элементы разделяем по '\n'
    neighbors = neighbors.split('\n')
# В neighbors теперь список строк и каждая описывает конкретного соседа
# Дальше проходим по списку, каждую строку тоже преобразуем в список, но уже разделитель пробел
# и распаковываем переменные. Три слева и два справа: сосед, наш интерфейс, его номер,
# интерфейс соседа, его номер, объединяем имена интерфейсов с их номерами
# и, наконец, записываем всё в словарь.
    for line in neighbors:
        line = line.split()
        r_host, l_intf, l_intf_num, *other, r_intf, r_intf_num = line
        r_intf = r_intf + r_intf_num
        l_intf = l_intf + l_intf_num
        result[local_host, l_intf] = r_host, r_intf

    return(result)

# Открываем файл
if __name__ == '__main__':
    file = open('sh_cdp_n_sw1.txt', 'r')
# Считываем содержимое файла методом read() в одну строку и передаём его функции
#    parse_cdp_neighbors(file.read())
    result =  parse_cdp_neighbors(file.read())
# Закрываем файл
    file.close()

    print(result)
