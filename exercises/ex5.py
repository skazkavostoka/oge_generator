import random


def ex_5():
    def multiplyer(a):
        user = random.choice(['Альфа', 'Бета'])
        start, muls = random.randint(2, 8), random.randint(2, 6)
        itog = 0 + start
        if a % 3 == 0:
            res = ['1', '1', '2', '2', '1']
        else:
            res = ['1', '1', '1', '1', '2']
        random.shuffle(res)
        res = ''.join(res)
        for i in res:
            if i == '1' and user == 'Альфа':
                itog += a
            elif i == '1':
                itog -= a
            elif i == '2':
                itog *= muls
        if user == 'Альфа':
            hello_5 = f'У исполнителя {user} две команды:\n1.Прибавь {a};\n2.Умножь на b;\n' \
                      f'Программа для исполнителя {user} это последовательность номеров команд.\n' \
                      f'Известно, что программа {res} переводит число {start} в число {itog}.\n' \
                      f'Определите значение b'
        else:
            hello_5 = f'У исполнителя {user} две команды:\n1.Вычти {a};\n2.Умножь на b;\n' \
                      f'Программа для исполнителя {user} это последовательность номеров команд.\n' \
                      f'Известно, что программа {res} переводит число {start} в число {itog}.\n' \
                      f'Определите значение b'
        if itog > 10:
            print(start, muls, itog)
            return hello_5, res

        else:
            print('рекурсия')
            return multiplyer(a)


    def divider(a):
        user = random.choice(['Сигма', 'Гамма'])
        start, b = random.randint(50, 170), random.randint(2, 4)
        k = str(start)
        res = ['1', '1', '1', '2', '1']
        random.shuffle(res)
        for i in res:
            if i == '1' and user == 'Сигма':
                start += a
            elif i == '1':
                start -= a
            elif i == '2' and start % b == 0:
                start //= b
            else:
                return divider(a)
        res = ''.join(res)
        if user == 'Сигма':
            hello_5 = f'У исполнителя {user} две команды:\n1.Прибавь {a};\n2.Раздели на b;\n' \
                      f'Программа для исполнителя {user} это последовательность номеров команд.\n' \
                      f'Известно, что программа {res} переводит число {k} в число {start}.\n' \
                      f'Определите значение b'
        else:
            hello_5 = f'У исполнителя {user} две команды:\n1.Вычти {a};\n2.Раздели на b;\n' \
                      f'Программа для исполнителя {user} это последовательность номеров команд.\n' \
                      f'Известно, что программа {res} переводит число {k} в число {start}.\n' \
                      f'Определите значение b'
        return hello_5, res


    def square(a):
        user = random.choice(['Омега', 'Дельта'])
        start, b = random.randint(2, 5), random.randint(1, 3)
        itog = 0 + start
        if a % 3 == 0:
            res = ['1', '1', '2', '2', '1']
        else:
            res = ['1', '1', '1', '1', '2']
        random.shuffle(res)
        for i in res:
            if i == '1':
                itog += b
            elif i == '2':
                itog **= 2
        res = ''.join(res)
        hello_5 = f'У исполнителя {user} две команды:\n1.Прибавь b;\n2.Возведи в квадрат;\n' \
                      f'Программа для исполнителя {user} это последовательность номеров команд.\n' \
                      f'Известно, что программа {res} переводит число {start} в число {itog}.\n' \
                      f'Определите значение числа b.'
        return hello_5, res


    variants = {'mul': multiplyer, 'div': divider, 'squ': square}
    variantss = ['mul', 'div', 'squ']
    a = random.randint(1, 4)
    hello_5, res = variants[random.choice(variantss)](a)
    return hello_5, res
