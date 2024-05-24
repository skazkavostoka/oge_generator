import random


def ex_3():
    def sum_parts(num, var):
        right_side = sum([int(i) for i in str(num)])
        if var:
            right_side += random.randint(1, 2)
            left_side = f'x > {num}'
            hello_3 = f'Найдите наименьшее значение числа X,' \
                      f' для которого высказывание ниже будет истинным:\n' \
                      f'{left_side} и сумма цифр числа X больше {right_side}'
            for x in range(num, 1000):
                if sum([int(j) for j in str(x)]) > right_side:
                    res = x
                    break
        else:
            right_side -= random.randint(1, 2)
            left_side = f'x < {num}'
            hello_3 = f'Найдите наименьшее положительное значение числа X,' \
                      f' для которого высказывание ниже будет ложным:\n' \
                      f'{left_side} и сумма цифр числа X меньше {right_side}'
            for x in range(num, 0, -1):
                if sum([int(j) for j in str(x)]) < right_side:
                    res = x
                    break
        return hello_3, res


    def chetnost(num, var):
        right_side = sum([int(i) for i in str(num)])
        if var:
            left_side = f'x > {num}'
            hello_3 = f'Найдите наименьшее положительное значение числа X,' \
                      f' для которого высказывание ниже будет истинным: \n' \
                      f'{left_side} и сумма цифр числа X четная'
            for x in range(num + 1, num + 5):
                right_side = sum([int(i) for i in str(x)])
                if x % 2 == 0:
                    res = x
                    break
        else:
            left_side = f'x < {num}'
            hello_3 = f'Найдите наибольшее положительное значение числа X,' \
                      f' для которого высказывание ниже будет истинным:\n' \
                      f'{left_side} и сумма цифр числа X нечетная'
            for x in range(num-1, num-10, -1):
                right_side = sum([int(i) for i in str(x)])
                if right_side % 2 != 0:
                    res = x
                    break
        return hello_3, res


    def simple(number):
        def simple1(num):
            num2 = random.randint(num, num + 7)
            hello_3 = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                     f'x >= {num} и не(x >= {num2})'
            res = num2 - 1
            return hello_3, res

        def simple2(num):
            num2 = random.randint(num, num + 7)
            hello_3 = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                     f' x >= {num} и не(x > {num2})'
            return hello_3, num2

        def simple3(num):
            num2 = random.randint(num, num + 7)
            hello_3 = f'Напишите наибольшее целое число x, для которого истинно высказывание:\n' \
                     f'не(x <= {number}) и x < {num2}'
            res = num2 - 1
            return hello_3, res

        def simple4(num):
            num2 = random.randint(num, num + 7)
            hello_3 = f'Напишите наименьшее целое число x, для которого истинно высказывание:\n' \
                     f'не(x < {num}) и не(x > {num2})'
            res = num
            return hello_3, res

        def simple5(num):
            num2 = random.randint(num, num + 7)
            hello_3 = f'Напишите наименьшее целое число x, для которого истинно высказывание:\n' \
                     f'не(x < {num}) и x < {num2}'
            res = num
            return hello_3, res

        def simple6(num):
            num2 = num + 1
            for x in range(num):
                if x > num and not(x > num2):
                    break
            hello_3 = f'Для какого целого числа x истинно высказывание:\n' \
                     f'x > {num} и не(x > {num2})'
            return hello_3, num2

        simples = [simple1, simple2, simple3, simple4, simple5, simple6]
        one_from = random.choice(simples)(number)
        hello_3, simple_num = one_from
        return hello_3, simple_num


    variants_right = [sum_parts, chetnost, simple, simple]
    variants_bool = [True, False]
    left = random.randint(10, 55)
    variant_bool = random.choice(variants_bool)
    example = random.choice(variants_right)
    if example == variants_right[2] or example == variants_right[3]:
        # print(example(left))
        hello_3, res = example(left)
        return hello_3, res
    else:
        # print(example(left, variant_bool))
        hello_3, res = example(left, variant_bool)
        return hello_3, res
