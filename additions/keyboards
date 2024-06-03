from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
        page: int = 1,
        total_pages: int = 1
):
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    if page > 1:
        keyboard.row(KeyboardButton(text='<<'), KeyboardButton(text='>>'))
    elif page < total_pages:
        keyboard.row(KeyboardButton(text='Меню'),  KeyboardButton(text='>>'))
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)

ex_kb = get_keyboard(
    'Отправить ответ',
    'Меню'
)
