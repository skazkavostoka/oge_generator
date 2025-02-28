import os

from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command, or_f, StateFilter

from keyboards.reply import parent_kbrd, cmd_start
from models import User, ParentChild, Lesson
from database import *

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
async def get_last_lessons(message: types.Message):
    parent_id = message.from_user.id

    students_ids = await get_children_to_parent(parent_id)

    if not students_ids:
        await message.answer('Вы не закреплены ни за одним учеником')
        return

    lessons_by_students = {student_id: await get_lessons(student_id) for student_id in students_ids}

    if not any(lessons_by_students.values()):
        await message.answer('Нет данных о последних занятиях ваших учеников')
        return

    response = ''
    for student_id, lessons in lessons_by_students.items():
        if lessons:
            response += f"\n👦 Ученик {student_id}:\n"
            for lesson in lessons:
                response += (f"📅 {lesson.date}: "
                             f"ДЗ - {lesson.homework_result}, "
                             f"Урок - {lesson.classwork_result}, "
                             f"Тест - {lesson.test_result}\n")

