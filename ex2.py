# Реализация задачи ОГЭ 2. Долго ломал себе голову о том, как правильно реализовать ее генератор
# В итоге пришет к такому решению. Оно соблюдает условие Фано, но декодируется задание гораздо легче,
# чем само задание из ОГЭ(так как в ОГЭ не соблюдается условие Фано, и на каком-то этапе декодирования
# могут существовать несколько вариантов декодирования
import random
import prettytable


letters = [i for i in 'АБВГДЕЖЗИКЛМНО']
random.shuffle(letters)
letters, v2_num = letters[:6], set()
table = prettytable.PrettyTable(letters)
while len(v2_num) != 2:
    v2_num.add(str(random.randint(0, 1)) + str(random.randint(0, 1)))
v4_num = v2_num.copy()
while len(v4_num) != 4:
     v4_num.add(str(random.randint(0, 1)) + str(random.randint(0, 1)))
v4_num -= v2_num
while len(v2_num) != len(letters):
    letter = random.choice(list(v4_num)) + str(random.randint(0, 1))
    v2_num.add(letter)
print(type(v2_num))
num_zip = dict(zip(letters, list(v2_num)))
word, decifer_word = '', ''
letters_digits = [num_zip[i] for i in letters]
for i in range(6):
    k = random.choice(letters)
    word += num_zip[k]
    decifer_word += k
table.add_row(letters_digits)
hello_2 = f'От разведчика было получено сообщение:\n' \
          f'{word}\n' \
          f'В этом сообщении зашифрован пароль – последовательность русских букв.' \
          f'В пароле использовались буквы {*letters,}.\n' \
          f'Расшифруйте сообщение, в ответе запишите пароль.\n' \
          f'{table}'
print(hello_2)
print(decifer_word)
