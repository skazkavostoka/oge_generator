import os

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, or_f, StateFilter

from keyboards.reply import parent_kbrd, cmd_start
from models import User, ParentChild, Lesson
from database import *

from keyboards.inline import create_students_inline_kb

parent_router = Router()


def check_user(user_id=0, role='учитель'):
    user = get_user(user_id)
    if not user or user.role.lower() != role:
        return False
    return True


@parent_router.message(or_f(Command('show_children'), F.text =='Кто закреплен за мной?'))
async def show_children_handler(message: types.Message):
    user = await get_user(message.from_user.id)
    if not check_user(message.from_user.id, role='родитель'):
        await message.answer('Вы не имеете прав для выполнения этой команды', reply_markup=cmd_start)
        return

    children = await get_children_to_parent(user.id)
    if not children:
        await message.answer('Вы не закреплены ни за одним учеником', reply_markup=parent_kbrd)
        return

    children_list = '\n'.join([f'{child.id}: {child.full_name}'for child in children])
    await message.answer(children_list, reply_markup=parent_kbrd)



@parent_router.message(or_f(Command('export_lessons'), F.text == 'Выгрузка статистики'))
async def export_lessons_handler(message: types.Message):

    user = await get_user(message.from_user.id)

    if not check_user(message.from_user.id, role='учитель'):
        await message.answer('Эта команда вам недоступна', reply_markup=cmd_start)
        return

    filepath = await export_lessons_handler(user.id)

    if filepath:
        await message.answer_document(types.FSInputFile(filepath), caption='Вот информация о занятиях ваших детей',
                                      reply_markup=parent_kbrd)
        os.remove(filepath)
    else:
        await message.answer('Данных о занятиях пока нет', reply_markup=parent_kbrd)


@parent_router.message(or_f(Command('last_lessons'), F.text == 'Последние результаты'))
async def get_last_lessons(message: types.Message, state: FSMContext):
    parent_id = message.from_user.id

    students_ids = await get_children_to_parent(parent_id)

    if not students_ids:
        await message.answer('Вы не закреплены ни за одним учеником')
        return

    await state.update_data({'students': students_ids})
    kb = create_students_inline_kb(students_ids, prefix='parent_lessons')

    await message.answer('Выберите учеников', reply_markup=kb)


@parent_router.callback_query(F.data.startswith('parent_lessons_page:'))
async def parent_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'родитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()

    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='parent_lessons')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@parent_router.callback_query(F.data.startswith('parent_lessons:'))
async def parent_lessons(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'родитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    lessons = await get_lessons(student_id)
    if not lessons:
        await callback.answer(f'У ученика {student_id} нет занятий')
    else:
        text = ''
        for lesson in lessons:
            text += (f"\n📅 {lesson.date}: "
                     f"ДЗ - {lesson.hw_res}, "
                     f"Урок - {lesson.cw_res}, "
                     f"Тест - {lesson.test_res}")
        await callback.message.answer(f"Последние занятия ученика {student_id}:{text}", reply_markup=cmd_start)

        await callback.answer()