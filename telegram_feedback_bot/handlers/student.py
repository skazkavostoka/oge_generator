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
    user_id = message.from_user.id
    await message.answer(f'Ваши результаты пока недоступны для Вас')


