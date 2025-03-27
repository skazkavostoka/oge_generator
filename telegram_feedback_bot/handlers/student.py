from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, or_f, StateFilter

from database import *
from keyboards.reply import student_kbrd, cmd_start
from models import Lesson, User


student_router = Router()

@student_router.message(F.text == 'Мои результаты')
async def show_my_results(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'ученик':
        await message.answer('Возникла какая-то ошибка!', reply_markup=cmd_start)
        return

    lessons = await get_all_lessons(user.telegram_id)
    if not lessons:
        await message.answer('Пока что тут пусто !=(')
    else:
        text = ''
        for lesson in lessons:
            text += (f"\n📅 {lesson.date}: "
                     f"ДЗ - {lesson.hw_res}, "
                     f"Урок - {lesson.cw_res}, "
                     f"Тест - {lesson.test_res}")
        await message.answer(f'Ваши последние результаты:\n{text}', reply_markup=cmd_start)


