# Задание 10. Одно из самых простых в реализации.
import random


# Функция перевода num из системы счисления osn в десятичную
def converter_ss(num, osn):
    res, osn = '', int(osn)
    alphabet = '0123456789ABCDEF'
    while num > 0:
        res += alphabet[num % osn]
        num //= osn
    res = res[::-1] + f'({osn})'
    return res


first_num = random.randint(35, 100)
numbers = [random.randint(first_num - 10, first_num + 12) for i in range(3)]
average = sum(numbers) // len(numbers)
hello_10 = 'Заданы три числа, записанные в различных системах счисления (системы счисления указаны в скобках):'
variables = [f'Требуется найти минимальное из них, ответ запишите в десятичной системе счисления'
             f'Ответ запишите в десятичной системе счисления, не указывая ее основание.',
             f'Требуется найти максимальное из них, ответ запишите в десятичной системе счисления. '
             f'Ответ запишите в десятичной системе счисления, не указывая ее основание.',
             f'Требуется вычислить, сколько из указанных чисел больше числа {average},'
             f' записанного в десятичной системе счисления.'
             f' Если таких чисел больше одного, запишите их в порядке возрастания в десятичной системе счисления,'
             f' без указания основания']
exercise = random.choice(variables)
systems = [2, 3, 8, 4, 16]
random.shuffle(systems)
final_numbers = []
final_numbers.extend(list(map(converter_ss, numbers, systems)))
# ответ будет храниться в переменной result
result = max(numbers)
print(hello_10, *final_numbers, '.', exercise, sep=' ')
