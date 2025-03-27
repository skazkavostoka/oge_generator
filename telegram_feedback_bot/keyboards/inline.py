from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_students_inline_kb(students, page=1, page_size=5, prefix='student_lesson'):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    chunk = students[start_index:end_index]

    keyboard_rows = []

    # Кнопки
    for student in chunk:
        text = student.full_name or f'Ученик {student.telegram_id}'
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"{prefix}:{student.telegram_id}"
        )
        # Добавляем отдельную строку с одной кнопкой
        keyboard_rows.append([button])

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

    if nav_buttons:
        keyboard_rows.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)



def create_lessons_inline_kb(lessons, page=1, page_size=5, prefix='choose_lesson_to_change'):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    chunk = lessons[start_index:end_index]

    keyboard_rows = []

    # Кнопки
    for lesson in chunk:
        lesson_date = str(lesson.date)
        text = f'{lesson_date}:{lesson.id}'
        button = InlineKeyboardButton(
            text=text,
            callback_data=f"{prefix}:{lesson.id}"
        )
        keyboard_rows.append([button])

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

    if nav_buttons:
        keyboard_rows.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)