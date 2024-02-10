import random


def sum_parts(num, var):
    right_side = sum([int(i) for i in str(num)])
    if var:
        right_side += random.randint(1, 2)
        left_side = f'x > {num}'
        hello_3 = f'Найдите наименьшее положительное значение числа X,' \
                  f' для которого высказывание ниже будет истинным:\n' \
                  f'{left_side} и сумма цифр числа X больше {right_side}'
    else:
        right_side -= random.randint(1, 2)
        left_side = f'x < {num}'
        hello_3 = f'Найдите наименьшее положительное значение числа X,' \
                  f' для которого высказывание ниже будет ложным:\n' \
                  f'{left_side} и сумма цифр числа X меньше {right_side}'
    return hello_3


def chetnost(num, var):
    right_side = sum([int(i) for i in str(num)])
    if var:
        left_side = f'x > {num}'
        hello_3 = f'Найдите наименьшее положительное значение числа X,' \
                  f' для которого высказывание ниже будет истинным: \n' \
                  f'{left_side} и сумма цифр числа X четная'
    else:
        left_side = f'x < {num}'
        hello_3 = f'Найдите наибольшее положительное значение числа X,' \
                  f' для которого высказывание ниже будет истинным:\n' \
                  f'{left_side} и сумма цифр числа X нечетная'
    return hello_3


def simple(number):
    def simple1(num):
        num2 = random.randint(num, num + 7)
        for x in range(100, 1, -1):
            if not(x <= num) and not(x > num2):
                break
        string = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                 f'x <= {num} и не(x > {num2})'
        return string

    def simple2(num):
        num2 = random.randint(num, num + 7)
        for x in range(100, 1, -1):
            if x >= num and not(x > num2):
                break
        string = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                 f' x >= {num} и не(x > {num2})'
        return string

    def simple3(num):
        num2 = random.randint(num, num + 7)
        for x in range(100, 1, -1):
            if not(x <= num) and x < num2:
                break
        string = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                 f'не(x <= {number}) и x < {num2}'
        return string

    def simple4(num):
        num2 = random.randint(num, num + 7)
        for x in range(1, 100):
            if not (x < num) and not (x > num2):
                break
        string = f'Напишите наименьшее целое число x, для которого истинно высказывание:\n' \
                 f'не(x < {num}) и не(x > {num2})'
        return string

    def simple5(num):
        num2 = random.randint(num, num + 7)
        for x in range(1, 100):
            if not (x <= num) and x < num2:
                break
        string = f'Напишите наименьшее целое число x, для которого истинно высказывание:\n' \
                 f'не(x < {num}) и x < {num2}'
        return string

    def simple6(num):
        num2 = num + 1
        for x in range(num):
            if x > num and not(x > num2):
                break
        string = f'Для какого целого числа x ложно высказывание:\n' \
                 f'x > {num} и не(x > {num2})'
        return string

    simples = [simple1, simple2, simple3, simple4, simple5, simple6]
    one_from = random.choice(simples)(number)
    return one_from


variants_right = [sum_parts, chetnost, simple, simple]
variants_bool = [True, False]
left = random.randint(10, 55)
variant_bool = random.choice(variants_bool)
example = random.choice(variants_right)
if example == variants_right[2] or example == variants_right[3]:
    print(example(left))
else:
    print(example(left, variant_bool))
