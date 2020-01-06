# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Enter VLAN number:'
* для trunk: 'Enter allowed VLANs:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''

access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]


# Запращиваем информацию у пользователя. См. пример на стр. 146

Mode = input('Enter interface mode (access/trunk): ').lower()
Interface = input('Enter interface type and number: ')

'''
Нам потребуется дополнительный словать, который
содержит варианты предложения пользователю.
Ключи 'access' и 'trunk'.
'''

Prompt_Dict = dict(access='Enter VLAN number: ', trunk='Enter allowed VLANs: ')

# Запращиваем номер VLAN или список VLANов

VLANs = input(Prompt_Dict.get(Mode))

'''
Далее преобразуем образцы вывода в строки и 
создаём словарь. После чего, выводим нужное значение из словаря
'''
###
## Преобразуем списки в строки и подставляем знечения VLANs
# см. стр. 146

Access_String = '\n'.join(access_template).format(VLANs)
Trunk_String = '\n'.join(trunk_template).format(VLANs)

# Создаём словарь с ключами 'access' и 'trunk'. См. стр. 121

DictInt = dict([('access',Access_String), ('trunk',Trunk_String)])

# Выводим знечения из словаря в зависимости от переданного пользователем значения

print('\n' + '-' * 30)
print('interface {}'.format(Interface))
print(DictInt.get(Mode, 'Oo-oops!'))

#
##
###