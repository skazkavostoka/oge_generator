import random
import prettytable

def ex_2():
    def generate_word():
        letters = [i for i in 'АБВГДЕЖЗИКЛМНО']
        random.shuffle(letters)
        letters = letters[:6]
        pairs, word, digits = {i: 0 for i in letters}, '', ''
        for i in letters:
            if letters.index(i) < 3:
                length = random.randint(2, 3)
            else:
                length = 3
            s = generate_k(length, pairs)
            # while s == 0:
            #     s = generate_k(length, pairs)
            pairs[i] = s
        for i in range(random.randint(5, 9)):
            t = random.choice(letters)
            word += pairs[t]
            digits += t
        return word, pairs, letters, digits


    def generate_k(length, pairs):
        k = ''.join([str(random.randint(0, 1)) for i in range(length)])
        if k not in pairs.values():
            return k
        else:
            return generate_k(length, pairs)


    word, pairs, letters, digits = generate_word()
    table = prettytable.PrettyTable(letters)
    transcript = [pairs[i] for i in letters]
    table.add_row(transcript)
    hello_2 = f'От разведчика было получено сообщение:\n' \
              f'{word}\n' \
              f'В этом сообщении зашифрован пароль – последовательность русских букв.' \
              f'В пароле использовались буквы {*letters,}.\n' \
              f'Расшифруйте сообщение, в ответе запишите пароль.\n' \
              f'Если таких вариантов несколько, запишите любой из них.\n' \
              f'{table}'
    return hello_2, digits
)
