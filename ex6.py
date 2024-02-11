# OGE exercise 6 generator. I have made a decision to prepare the correct answer to exercise. The answer is in a variable with name "res"
# Решил сразу подготовить почву для проверки правильности решений.
# Для этого я добавил переменную res которая содержит в себе правильный ответ на любую сгенерированную задачу.


import random
import operator
from functools import reduce
import prettytable

# зададим проверяемые для s и t значения, и сгенерируем последовательности этих чисел
# k - длина каждой последовательности
s, t, k = random.randint(8, 15), random.randint(8, 15), random.randint(8, 10)
s_seq = [random.randint(-s-s, s+s) for _ in range(k)]
t_seq = [random.randint(-t-t, t+t) for _ in range(k)]


# создадим пары чисел для каждой s и t
st_tup = [(s_seq[i], t_seq[i]) for i in range(k)]

# далее создадим список операторов и рандомно вытянем свой знак для s и t чисел
operators = [operator.lt, operator.le, operator.ge, operator.gt]
operators_names = {'gt': '>', 'ge': '>=', 'le': '<=', 'lt': '<'}
mark_s, mark_t = random.choice(operators), random.choice(operators)

# зададим выбор логической функции
and_or = random.randint(0, 1)
and_or_names = {1: 'and', 0: 'or'}

# создадим таблицу для вывода задания
table = prettytable.PrettyTable(['Python', 'Паскаль', 'C++'])
open_fig, close_fig = '{', '}'
table.align = 'l'

row1 = f's = int(input())\n' \
       f't = int(input())\n' \
       f'if s {operators_names[mark_s.__name__]} {s} {and_or_names[and_or]} t {operators_names[mark_t.__name__]} {t}:\n' \
       f'   print("ДА")\n' \
       f'else:\n' \
       f'   print("НЕТ")'

row2 = f'var s,t: integer;\n' \
       f'begin\n' \
       f'   readln(s);\n' \
       f'   readln(t);\n' \
       f'   if (s {operators_names[mark_s.__name__]} {s}) {and_or_names[and_or]} (t {operators_names[mark_t.__name__]} {t})\n' \
       f'       then writeln("ДА")\n' \
       f'       else writeln("НЕТ")'

row3 = f'#include <iostream>\n' \
       f'using namespace std;\n' \
       f'int main() {open_fig}\n' \
       f'   int s,t;\n' \
       f'   cin>>s;\n' \
       f'   cin>>t;\n' \
       f'   if(s {operators_names[mark_s.__name__]} {s} {and_or_names[and_or]} t {operators_names[mark_t.__name__]} {t})\n' \
       f'       cout<<"ДА";\n' \
       f'   else\n' \
       f'       cout<<"НЕТ";\n' \
       f'   {close_fig}'
table.add_row([row1, row2, row3])

# переберем эти числа, заранее обеспечив правильный ответ для проверки. Создадим переменную counter,
# которая будет считать подходящие под условие пары чисел
counter = 0
if and_or:
    res = sum(map(lambda x, y: x and y, list(map(mark_s, s_seq, [s for _ in range(k)])), list(map(mark_t, t_seq, [t for _ in range(k)]))))
else:
    res = sum(map(lambda x, y: x or y, list(map(mark_s, s_seq, [s for _ in range(k)])), list(map(mark_t, t_seq, [t for _ in range(k)]))))

#выводящая строка
hello_6 = f'Дана программа:\n' \
          f'{table}\n' \
          f'Было проведено {k} запусков этой программы, при которых\n' \
          f'в качестве значений s и t вводились следующие пары чисел:\n' \
          f'{st_tup}\n' \
          f'Сколько было запусков, при которых программа напечатала "ДА"'
print(hello_6)
