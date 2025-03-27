from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_students_inline_kb(students, page=1, page_size=5, prefix='student_lesson'):
    """
    Создаём построчную клавиатуру для списка учеников,
    с навигацией по страницам и кастомным префиксом.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    chunk = students[start_index:end_index]

    # Каждая строка — это список InlineKeyboardButton
    keyboard_rows = []

    # Кнопки для каждого ученика
    for student in chunk:
        text = student.full_name or f'Ученик {student.telegram_id}'
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"{prefix}:{student.telegram_id}"
        )
        # Добавляем отдельную строку с одной кнопкой
        keyboard_rows.append([button])

    # Кнопки «Назад/Вперёд»
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=f"{prefix}_page:{page-1}"
        )
            )
    if end_index < len(students):
        nav_buttons.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=f"{prefix}_page:{page+1}"
            )
        )

    # Если есть кнопки навигации, добавляем их в конец (одна строка)
    if nav_buttons:
        keyboard_rows.append(nav_buttons)

    # Возвращаем InlineKeyboardMarkup, передавая кнопки через inline_keyboard
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)



def create_students_inline_kb(lessons, page=1, page_size=5, prefix='student_lesson'):
    """
    Создаём построчную клавиатуру для списка учеников,
    с навигацией по страницам и кастомным префиксом.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    chunk = students[start_index:end_index]

    # Каждая строка — это список InlineKeyboardButton
    keyboard_rows = []

    # Кнопки для каждого ученика
    for lesson in lessons:
        lesson_date = str(lesson.date)
        text = f'{lesson_date}:{lesson.id}'
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"{prefix}:{lesson.id}"
        )
        # Добавляем отдельную строку с одной кнопкой
        keyboard_rows.append([button])

    # Кнопки «Назад/Вперёд»
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="<<",
                callback_data=f"{prefix}_page:{page-1}"
        )
            )
    if end_index < len(lessons):
        nav_buttons.append(
            InlineKeyboardButton(
                text=">>",
                callback_data=f"{prefix}_page:{page+1}"
            )
        )

    # Если есть кнопки навигации, добавляем их в конец (одна строка)
    if nav_buttons:
        keyboard_rows.append(nav_buttons)

    # Возвращаем InlineKeyboardMarkup, передавая кнопки через inline_keyboard
    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)