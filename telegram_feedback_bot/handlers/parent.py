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



@parent_router.message(or_f(Command('show_children'), F.text =='Кто закреплен за мной?'))
async def show_children_handler(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'родитель':
        await message.answer('Вы не имеете прав для выполнения этой команды', reply_markup=cmd_start)
        return

    children = await get_children_to_parent(user.telegram_id)
    if not children:
        await message.answer('Вы не закреплены ни за одним учеником', reply_markup=parent_kbrd)
        return

    children_list = '\n'.join([f'{child.telegram_id}: {child.full_name}'for child in children])
    await message.answer(children_list, reply_markup=parent_kbrd)



@parent_router.message(or_f(Command('export_lessons'), F.text == 'Выгрузка статистики'))
async def export_lessons_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'родитель':
        await message.answer('Вы не имеете прав для выполнения этой команды', reply_markup=cmd_start)
        return

    students = await get_children_to_parent(user.telegram_id)
    if not students:
        await message.answer('За вами не закреплены ученики!', reply_markup=cmd_start)
        return
    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='export_lesson')
    await message.answer('Выберите ученика, результаты за которого хотите выгрузить')

@parent_router.callback_query(F.data.startswith('export_lesson_page:'))
async def export_lessons_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'родитель':
        await callback.answer('Вы не имеете прав для выполнения этой команды', reply_markup=cmd_start)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    users = data.get('students', [])

    kb = create_students_inline_kb(users, page=page, prefix='export_lesson')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@parent_router.callback_query(F.data.startswith('export_lesson:'))
async def export_lesson(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'родитель':
        await callback.answer('Вы не имеете прав для выполнения этой команды', reply_markup=cmd_start)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    success = await export_lessons_to_excel(student_id)

    if success:
        await callback.message.answer_document(types.FSInputFile(success), caption='Вот информация о занятиях ваших детей',
                                      reply_markup=cmd_start)
        os.remove(success)
    else:
        await callback.message.answer('Данных о занятиях пока нет', reply_markup=cmd_start)
    await state.clear()


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