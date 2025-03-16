from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from database import get_user, add_user
from aiogram.types import Message

from keyboards.reply import *

router = Router()



@router.message(or_f(Command('start'), F.text == 'Меню'))
async def start_handler(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        if user.role == 'учитель':
            await message.answer(f'Привет, {user.full_name}\nЧто нужно сделать?', reply_markup=teacher_1_kbrd)
        elif user.role == 'родитель':
            await message.answer(f'Привет, {user.full_name}\nЧто нужно сделать?', reply_markup=parent_kbrd)
        else:
            await message.answer(f'Привет, {user.full_name}\nЧто нужно сделать?', reply_markup=student_kbrd)
    else:
        await add_user(message.from_user.id, message.from_user.full_name, 'ученик')
        await message.answer(f'Вы зарегистрированы как ученик. Свяжитесь с администратором при возникновении вопросов')


@router.message(or_f(Command('my_id'), F.text == 'Узнать ID'))
async def get_my_id(message: types.Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
