import random
import prettytable

def ex_7():
    def gen_ip():
        total = -1
        while total % 2 != 0:
            ip = '.'.join([str(random.randint(0, 255)) for _ in range(4)])
            total = len(ip)
        cut1, cut3, cut2, ip_row = random.randint(2, 4), random.randint(2, 4), total // 2, []
        for i in range(len(ip.split('.'))):
            if i % 2 == 0 and i != 2:
                ip_row.append(ip.split('.')[i] + '.')
            elif i == 2:
                ip_row.append('.' + ip.split('.')[i] + '.')
            else:
                ip_row.append(ip.split('.')[i])
        newtable = prettytable.PrettyTable(list(range(1,5)))
        random.shuffle(ip_row)
        newtable.add_row(ip_row)
        hello_7 = f'Вова записал IP адрес сервера на листок, оставил его на столе и ушел гулять.\n' \
                  f'Вернувшись домой, он заметил, что его погрызла собака.\n' \
                  f'Ниже показаны четыре фрагмента, \n{newtable}\n' \
                  f'соберите из них корректный IP-адрес. В ответе укажите цифры.'
        return hello_7, ip


    def gen_mask():
        protocols = ['ftp', 'https']
        domains_1 = ['ru', 'com', 'io', 'ua', 'ca', 'org', 'site', 'space']
        domains_2 = ['ru.', 'chopik.', 'doge.', 'bitcoin.', 'ethereum.', 'pepe.', 'clone.', 'president.', 'times.', 'doc.']
        catalogs = ['credits', 'files', 'opens', 'mydocs', 'orders', 'transactions', 'libraries']
        file_name = ['bit', 'chop', 'top', 'frog', 'floki', 'ltc', 'btc', 'scan', 'wide', 'lion', 'bird']
        formats = ['.svg', '.png', '.img', '.txt', '.doc', '.docx', 'xml']
        newtable = prettytable.PrettyTable(list(range(1, 9)))
        protocol, catalog = random.choice(protocols), random.choice(catalogs)
        domain_1, domain_2 = random.choice(domains_1), random.choice(domains_2)
        file_1, file_2 = random.choice(file_name), random.choice(formats)
        link_row = [protocol, domain_2, domain_1, file_2, file_1, catalog, '/', ':']
        random.shuffle(link_row)
        newtable.add_row(link_row)
        hello_7 = f'Пользователь осуществляет подключейние к сайту {domain_2 + domain_1} про протоколу {protocol}.\n' \
                  f'На сервере, в каталоге {catalog} лежит файл {file_1 + file_2}. Ниже показаны фрагменты' \
                  f'ссылки на сайт \n{newtable}\n' \
                  f'Cоставьте из них корректную ссылку для данного файла, в ответе запиши цифры фрагментов.'
        res = protocol + '://' + domain_2 + domain_1 + '/' + catalog + '/' + file_1 + file_2
        return hello_7, res


    def could_ip_be():
        numbers_2 = [random.randint(0, 255) for _ in range(4)]
        if random.randint(0, 100) % 2 == 0:
            numbers_2[numbers_2.index((random.choice(numbers_2)))] = 256
        res = '.'.join([str(i) for i in numbers_2])
        flag = True
        for i in res.split('.'):
            if int(i) > 255:
                flag = False
        hello_7 = f'Возможен ли такой ip-адрес {res} ? В ответе укажите "ДА" если возможен,\n' \
                  f'и "НЕТ" если невозможен'
        return hello_7, flag


    variants = {'mask': gen_mask, 'ip': gen_ip, 'maybe': could_ip_be}
    variantss = ['mask', 'ip', 'maybe']
    exercise, res, = variants[random.choice(variantss)]()
    return exercise, res


