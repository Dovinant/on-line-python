# -*- coding: utf-8 -*-
'''
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

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
    # Функция вернёт словарь, создадим его
    result = {}
	
    # Распаковываем словарь. Имя интерфейса в переменную intf, номера vlan в vlans
    for intf, vlans in intf_vlan_mapping.items():
    # Также нам понадобится список. В него мы поместим команды
	# Список обнуляется на начало каждого прохода по словарю
	# иначе он будет бесконтрольно разрастаться
        result_list = []
	# Проходим циклом по командам из trunk_mode_template
	# Если команда заканчивается на allowed vlan, добавляем в неё номера vlan,
	# но эти номера в trunk_config записаны как числа, поэтому
	# меняем числа на строки и перезаписываем их в новый список vlan_str
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                vlan_str = [str(vlan) for vlan in vlans]
	    	# Преобразуем список vlan_str в строку и окончательно формируем команду
                result_list.append(f"{command} {','.join(vlan_str)}")
            else:
                result_list.append(f'{command}')
#        Формируем словарь. Ключ - имя интерфейса, значение - список команд
        result[intf] = result_list
    return result

# Вызываем функцию, передаём ей аргументы, принимаем результат
interface_dict = generate_trunk_config(trunk_config, trunk_mode_template)

print(interface_dict)

# f-строка почему-то не хотела работать пока не запустил workon pyneng-py3
