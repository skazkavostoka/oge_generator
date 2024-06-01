import random
import prettytable

#функция генерирующая задание для двух множеств
def ex_8():
    def v2():
        #здесь создаются переменные выбора типа задачи, алфавит, случайная выборка слов из алфавита для задания
        k, hello_8, res = random.randint(1, 4), '', 0
        alphabet = {0: ['Сорока', 'Ворона'], 1: ['Футбол', 'Баскетбол'], 2: ['Цапля', 'Аист'],
                    3: ['Пластик', 'Металл'], 4: ['Россия', 'Америка'], 5: ['Пистолет', 'Автомат'],
                    6: ['Нефть', 'Газ'], 7: ['Медведь', 'Кабан'], 8: ['Орел', 'Ястреб']}
        words = alphabet[random.randint(0, 8)]
        #ниже, исходя из k генерируется задание. Случайно задается каждое множество и вычисляются результаты
        #переменная res возвращает правильный ответ, текст задачи печатается из функции.
        #в принципе, все аналогично для функции v3, только переменных больше
        if k == 1:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_and_p2 = point1 + point2 - p1_or_p2
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([words[0], point1])
            table.add_row([words[1], point2])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]} | {words[1]}'
            res = p1_or_p2
        elif k == 2:
            point1 = random.randint(2500, 10000)
            point2 = random.randint(2500, 10000)
            p1_or_p2 = random.randint(max(point1, point2), point1+point2)
            p1_and_p2 = point1 + point2 - p1_or_p2
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([words[0], point1])
            table.add_row([words[1], point2])
            table.add_row([f'{words[0]} | {words[1]}', p1_or_p2])
            res = p1_and_p2
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]} & {words[1]}'
        elif k == 3:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_and_p2 = point1 + point2 - p1_or_p2
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([words[0], point1])
            table.add_row([f'{words[0]} | {words[1]}', p1_or_p2])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет.\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу' \
                      f'{words[1]}'
            res = point2
        elif k == 4:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_and_p2 = point1 + point2 - p1_or_p2
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([words[1], point2])
            table.add_row([f'{words[0]} | {words[1]}', p1_or_p2])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]}'
            res = point1
        return hello_8, res


    def v3():
        k, hello_8, res = random.randint(1, 3), '', 0
        alphabet = {0: ['Сорока', 'Ворона', 'Синица'], 1: ['Футбол', 'Баскетбол', 'Волейбол'],
                    2: ['Цапля', 'Аист', 'Страус'], 3: ['Пластик', 'Металл', 'Дерево'],
                    4: ['Россия', 'Америка', 'Канада'], 5: ['Пистолет', 'Автомат', 'Пулемет'],
                    6: ['Нефть', 'Газ', 'Уголь'], 7: ['Медведь', 'Кабан', 'Волк'],
                    8: ['Орел', 'Ястреб', 'Сокол']}
        words = alphabet[random.randint(0, 8)]
        if k == 1:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            point3 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_or_p3 = random.randint(max(point1, point3), point1 + point3)
            p2_or_p3 = random.randint(max(point2, point3), point2 + point3)
            p1_and_p2 = point1 + point2 - p1_or_p2
            p1_and_p3 = point1 + point3 - p1_or_p3
            p2_and_p3 = point2 + point3 - p2_or_p3
            p1_p2_p3 = random.randint(min(p1_and_p2, p2_and_p3, p1_and_p3) // 2, min(p1_and_p2, p2_and_p3, p1_and_p3))
            p1_and_p2p3 = p1_and_p2 + p1_and_p3 - p1_p2_p3
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            table.add_row([f'{words[0]} & ({words[1]} | {words[2]})', p1_and_p2p3])
            table.add_row([f'{words[0]} & {words[1]} & {words[2]}', p1_p2_p3])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]} & {words[2]}?'
            res = p1_and_p3
        if k == 2:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            point3 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_or_p3 = random.randint(max(point1, point3), point1 + point3)
            p2_or_p3 = random.randint(max(point2, point3), point2 + point3)
            p1_and_p2 = point1 + point2 - p1_or_p2
            p1_and_p3 = point1 + point3 - p1_or_p3
            p2_and_p3 = point2 + point3 - p2_or_p3
            p1_p2_p3 = random.randint(min(p1_and_p2, p2_and_p3, p1_and_p3) // 2, min(p1_and_p2, p2_and_p3, p1_and_p3))
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            table.add_row([f'{words[0]} & {words[2]}', p1_and_p3])
            table.add_row([f'{words[0]} & {words[1]} & {words[2]}', p1_p2_p3])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]} & ({words[2]} | {words[1]})?'
            res = p1_and_p2 + p1_and_p3 - p1_p2_p3
        if k == 3:
            point1 = random.randint(250, 1000)
            point2 = random.randint(250, 1000)
            point3 = random.randint(250, 1000)
            p1_or_p2 = random.randint(max(point1, point2), point1 + point2)
            p1_or_p3 = random.randint(max(point1, point3), point1 + point3)
            p2_or_p3 = random.randint(max(point2, point3), point2 + point3)
            p1_and_p2 = point1 + point2 - p1_or_p2
            p1_and_p3 = point1 + point3 - p1_or_p3
            p2_and_p3 = point2 + point3 - p2_or_p3
            p1_p2_p3 = random.randint(min(p1_and_p2, p2_and_p3, p1_and_p3) // 2, min(p1_and_p2, p2_and_p3, p1_and_p3))
            p1_and_p2p3 = p1_and_p2 + p1_and_p3 - p1_p2_p3
            table = prettytable.PrettyTable(['Запрос', 'Найдено страниц'])
            table.add_row([f'{words[0]} & {words[1]}', p1_and_p2])
            table.add_row([f'{words[0]} & ({words[2]} | {words[1]})', p1_and_p2p3])
            table.add_row([f'{words[0]} & {words[1]} & {words[2]}', p1_p2_p3])
            hello_8 = f'В таблице приведены запросы и количество найденных' \
                      f' по ним страниц некоторого сегмента сети Интернет:\n' \
                      f'{table}\n' \
                      f'Какое количество страниц будет найдено по запросу ' \
                      f'{words[0]} & {words[2]}?'
            res = p1_and_p3
        return hello_8, res


    variants = {2: v2, 3: v3}
    return variants[random.randint(2, 3)]()
