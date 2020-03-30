# -*- coding: utf-8 -*-
'''
Задание 9.2

Создать функцию generate_trunk_config, которая генерирует конфигурацию для trunk-портов.

У функции должны быть такие параметры:

- intf_vlan_mapping: ожидает как аргумент словарь с соответствием интерфейс-VLANы такого вида:
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}
- trunk_template: ожидает как аргумент шаблон конфигурации trunk-портов в виде списка команд (список trunk_mode_template)

Функция должна возвращать список команд с конфигурацией
на основе указанных портов и шаблона trunk_mode_template.
В конце строк в списке не должно быть символа перевода строки.

Проверить работу функции на примере словаря trunk_config.

Пример итогового списка (перевод строки после каждого элемента сделан для удобства чтения):
[
'interface FastEthernet0/1',
'switchport mode trunk',
'switchport trunk native vlan 999',
'switchport trunk allowed vlan 10,20,30',
'interface FastEthernet0/2',
'switchport mode trunk',
'switchport trunk native vlan 999',
'switchport trunk allowed vlan 11,30',
...]


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

trunk_mode_template = [
    'switchport mode trunk', 'switchport trunk native vlan 999',
    'switchport trunk allowed vlan'
]

trunk_config = {
    'FastEthernet0/1': [10, 20, 30],
    'FastEthernet0/2': [11, 30],
    'FastEthernet0/4': [17]
}

# Создаём функцию
def generate_trunk_config(intf_vlan_mapping, trunk_template):
    #Функция вернёт список, создадим его
    result = []
	
    # Распаковываем словарь. Имя интерфейса в переменную intf, номера vlan в vlans
    for intf, vlans in intf_vlan_mapping.items():
	# Записываем имя интерфейса
        result.append('interface ' + intf)
		# Проходим циклом по командам из trunk_mode_template
		# Если команда заканчивается на allowed vlan, добавляем в неё номера vlan,
		# но эти номера в trunk_config записаны как числа, поэтому
		# меняем числа на строки и перезаписываем их в новый список vlan_str
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                vlan_str = [str(vlan) for vlan in vlans]
		# Преобразуем список vlan_str в строку и окончательно формируем команду
                result.append(f"{command} {','.join(vlan_str)}")
            else:
                result.append(f'{command}')
    return result

# Вызываем функцию, передаём ей аргументы, принимаем результат
interface_list = generate_trunk_config(trunk_config, trunk_mode_template)

print(interface_list)

# f-строка почему-то не хотела работать пока не запустил workon pyneng-py3
