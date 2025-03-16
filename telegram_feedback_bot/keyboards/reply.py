from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_kbrd(buttons, resize=True, one_time=False):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn)] for btn in buttons],
        resize_keyboard=resize,
        one_time_keyboard=one_time
    )


parent_kbrd = get_kbrd(
            ['Кто закреплен за мной?',
            'Выгрузка статистики',
            'Последние результаты',
            'Узнать ID']
            )

student_kbrd = get_kbrd(
            ['Мои результаты',
            'Узнать ID']
            )


teacher_1_kbrd = get_kbrd(['Уроки',
                           'Связи',
                           'Узнать ID'])

teacher_2_kbrd = get_kbrd(
            ['Назначить роли',
            'Установить связь',
            'Удалить связь',
            'Меню']
            )

teacher_3_kbrd = get_kbrd(['Оценить урок',
                           'Изменить урок',
                           'Получить выгрузку',
                           'Результаты ученика',
                           'Меню'])


cmd_start = get_kbrd(['Меню'])

rmv = ReplyKeyboardRemove()