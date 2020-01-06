# -*- coding: utf-8 -*-
'''
Задание 5.2d

Переделать скрипт из задания 5.2c таким образом, чтобы, при запросе параметра,
пользователь мог вводить название параметра в любом регистре.

Пример выполнения скрипта:
$ python task_5_2d.py
Enter device name: r1
Enter parameter name (ios, model, vendor, location, ip): IOS
15.4


Ограничение: нельзя изменять словарь london_co.

Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if.
'''

london_co = {
    'r1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.1'
    },
    'r2': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '4451',
        'ios': '15.4',
        'ip': '10.255.0.2'
    },
    'sw1': {
        'location': '21 New Globe Walk',
        'vendor': 'Cisco',
        'model': '3850',
        'ios': '3.6.XE',
        'ip': '10.255.0.101',
        'vlans': '10,20,30',
        'routing': True
    }
}

# Запрашиваем у пользоветеля имя устройства

DeviceName = input(("Enter device name: "))

# Используем метод keys() и преобразуем результат в список
# см. стр. 119

KeysList = list(london_co[DeviceName].keys())

# Методом join() получаем из списка строку. Стр. 108

KeyString = ', '.join(KeysList)

# Формируем строку приглашения

KeyString = "Enter parameter name (" + KeyString + "): "

# Просим ввести параметр и задействуем метод lower(). стр. 94

ParametrName = input(KeyString).lower()

# Выводим используя метод get() см. стр. 117

print(london_co.get(DeviceName).get(ParametrName, 'Такого параметра нет!'))