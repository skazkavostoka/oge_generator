#Exercise 7, all variants(without mailbox constructor). Without checket correct answers and BD for statistics(its in future
#7 урпажнение, реализованы все варианты кроме конструктора корректного адреса электронной почты. Задание по разбиению IP генерируется абсолютно случайно,
#что касается сборки корректной ссылки файла, то решил не заморачиваться с созданием словаря, вообще можно расширить
#Пока что без проверки правильности решения и БД. Это все будет в будущем, когда допилю генератор первых 10 заданий и соберу все это в единое целое)

import random
import prettytable


def gen_ip():
    total = -1
    while total % 2 != 0:
        ip = '.'.join([str(random.randint(0, 255)) for _ in range(4)])
        total = len(ip)
    cut1, cut3, cut2 = random.randint(2, 4), random.randint(2, 4), total // 2
    part1, part2, part3, part4 = ip[0:cut1], ip[cut1: cut2], ip[cut2:cut2+cut3], ip[cut2+cut3:]
    newtable = prettytable.PrettyTable(list(range(1,5)))
    newtable.add_row([part1, part2, part3, part4])
    hello_7 = f'Вова записал IP адрес сервера на листок, оставил его на столе и ушел гулять.' \
              f' Вернувшись домой, он заметил, что его погрызла собака.' \
              f'Ниже показаны четыре фрагмента, \n{newtable}\n' \
              f'соберите из них корректный IP-адрес. В ответе укажите цифры.'
    return hello_7


def gen_mask():
    protocols = ['ftp', 'https']
    files = ['ru.doc', 'doc.ru', 'classes.xml', 'com.pdf', 'pirog.svg']
    catalogs = ['credits', 'files', 'opens', 'mydocs', 'orders']
    servers = ['capcom.com', 'python.org', 'semel.ru', 'slava.com', 'draw.io']
    protocol = random.choice(protocols)
    server = random.choice(servers)
    catalog = random.choice(catalogs)
    file = random.choice(files)
    hello_7 = f'Пользователь осуществляет подключейние к сайту {server} про протоколу {protocol}. ' \
              f'На сервере, в каталоге {catalog} лежит файл {file}. Используя эти данные,' \
              f'составьте корректную ссылку для данного файла.'
    return hello_7


def could_ip_be():
    numbers_2 = [random.randint(0, 255) for _ in range(4)]
    if random.randint(0, 100) % 2 == 0:
        numbers_2[numbers_2.index((random.choice(numbers_2)))] = 256
    res = '.'.join([str(i) for i in numbers_2])
    hello_7 = f'Возможен ли такой ip-адрес {res} ? В ответе укажите "ДА" если возможен,' \
              f'и "НЕТ" если невозможен'
    return hello_7


variants = {'mask': gen_mask, 'ip': gen_ip, 'maybe': could_ip_be}
variantss = ['mask', 'ip', 'maybe']
k = random.choice(variantss)
print(variants[k]())


