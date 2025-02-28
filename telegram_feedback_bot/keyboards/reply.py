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

teacher_kbrd = get_kbrd(
            ['Назначить роли',
            'Оценить урок',
            'Установить связь',
            'Удалить связь',
            'Получить выгрузку',
            'Результаты ученика',
            'Узнать ID']
            )


student_kbrd = get_kbrd(
            ['Мои результаты',
            'Узнать ID']
            )


cmd_start = get_kbrd(['Меню'])

rmv = ReplyKeyboardRemove()