# -*- coding: utf-8 -*-
'''
Задание 5.4

Найти индекс последнего вхождения элемента.

Например, для списка num_list, число 10 последний раз встречается с индексом 4; в списке word_list, слово 'ruby' последний раз встречается с индексом 6.

Сделать решение общим (то есть, не привязываться к конкретному элементу в конкретном списке) и проверить на двух списках, которые указаны и на разных элементах.

Для этого надо запросить у пользователя сначала ввод числа из списка num_list и затем вывести индекс его последнего появления в списке.
А затем аналогично для списка word_list.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

num_list = [10, 2, 30, 100, 10, 50, 11, 30, 15, 7]
word_list = [
    'python', 'ruby', 'perl', 'ruby', 'perl', 'python', 'ruby', 'perl'
]

# Запрашиваем у пользователя число

NUM = input('Type the number, please: ')

# Это мы получили строковое значение. Преобразуем в число

NUM = int(NUM)

# Запрашиваем у пользователя слово

WORD = input('Type the word, please: ').lower()

# Для начала создадим копии наших списков

num_list_tmp = 1 * num_list
word_list_tmp = 1 * word_list

# Обратим наши списки методом reverse()
# см. стр. 106

num_list_tmp.reverse()
word_list_tmp.reverse()

# Находим индекс интересующих нас элементов (последние теперь первые)

INDEX_NUM = len(num_list_tmp) - 1 - num_list_tmp.index(NUM)
INDEX_WORD = len(word_list_tmp) - 1 - word_list_tmp.index(WORD)

# Выводим результат, см. стр. 146

print('\n' + '-' * 30)
print('The index of the last {} is {}'.format(NUM, INDEX_NUM))
print('The index of the last {} is {}'.format(WORD, INDEX_WORD))
