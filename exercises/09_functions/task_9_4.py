# -*- coding: utf-8 -*-
'''
Задание 9.4

Создать функцию convert_config_to_dict, которая обрабатывает конфигурационный файл коммутатора и возвращает словарь:
* Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
* Если у команды верхнего уровня есть подкоманды, они должны быть в значении у соответствующего ключа, в виде списка (пробелы в начале строки надо удалить).
* Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

При обработке конфигурационного файла, надо игнорировать строки, которые начинаются с '!',
а также строки в которых содержатся слова из списка ignore.

Для проверки надо ли игнорировать строку, использовать функцию ignore_command.


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ignore = ['duplex', 'alias', 'Current configuration']


def ignore_command(command, ignore):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    '''
    return any(word in command for word in ignore)

# Создаём функцию
def convert_config_to_dict(config_filename):
# Функция вернёт словарь, создадим его
    dictionary = {}
    # Открываем файл конструкцией with
    with open(config_filename, 'r') as file:
        for line in file:
		# Проверяем, что в строке нет слова из списка ignore и она не начинается с '!'
            if (ignore_command(line, ignore) or line.startswith('!')):
#           С командой pass не работает, берём continue
                continue
            elif (line[0] != ' '):
# Если строка не начинается с пробела, значит это команда верхнего уровня.
                key_command = line.rstrip()
# Запомним её как ключ для словаря
                list = []
# А список подкоманд пока пустой
            else:
                list.append(line.strip())
# Метод strip()	удалит символ "\n" и/или пробелы слева и справа от строки
            if (key_command):
# Проверяем, что команда верхнего уровня не пустая строка			
                dictionary[key_command] = list
    return dictionary

#
result = convert_config_to_dict('config_sw1.txt')
print(result)

'''
В первой строке файла config_sw1.txt стоит "\n"
в строке 52-й нашей программы key_command = line.rstrip() метод rstrip()
удалит символ перевода строки и первая строка окажется пустой, т.е. первым ключём
в нашем словаре будет пустая строка со значением пустой список.
Чтобы этого избежать в строке 59 проверяем, что ключ словаря не пустая строка
и если да, то только тогда дополняем словарь.
'''