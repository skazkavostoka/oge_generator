from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.filters import Command, or_f, StateFilter

from database import *
from keyboards.reply import *
from keyboards.inline import create_students_inline_kb, create_lessons_inline_kb
from database import *

import os

from oge_generator.telegram_feedback_bot.database import get_user, get_all_students

teacher_router = Router()


@teacher_router.message(F.text == 'Связи')
async def connects(message: Message):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return
    await message.answer('Выберите действие: ', reply_markup=teacher_2_kbrd)


@teacher_router.message(F.text == 'Уроки')
async def lessons(message: Message):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return
    await message.answer('Выберите действие: ', reply_markup=teacher_3_kbrd)


@teacher_router.message(or_f(Command("set_role"), F.text == 'Назначить роли'))
async def set_role_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return

    users_ids = await get_all_users()
    if not users_ids:
        await message.answer('Что-то не так с работой программы', reply_markup=cmd_start)
        return

    await state.update_data({'users': users_ids})
    kb = create_students_inline_kb(users_ids, prefix='users_choose')

    await message.answer('Выберите пользователя которому хотите присвоить новую роль', reply_markup=kb)

@teacher_router.callback_query(F.data.startswith('users_choose_page:'))
async def users_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != "учитель":
        await callback.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()

    users = data.get('users', [])

    kb = create_students_inline_kb(users, page=page, prefix='users_choose')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('users_choose:'))
async def users_choose(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != "учитель":
        await callback.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return

    _, user_id_str = callback.data.split(':')
    user_id = int(user_id_str)

    await state.update_data({'user_id': user_id})
    await state.set_state('waiting_for_role_change')
    await callback.message.answer('Введите новую роль для пользователя(ученик, родитель): ')

@teacher_router.message(F.text, StateFilter('waiting_for_role_change'))
async def change_user_role(message: Message, state: FSMContext):
    new_role = message.text.strip().lower()
    data = await state.get_data()
    user_id = data.get('user_id')
    valid_roles = ['ученик', 'родитель']

    if not user_id:
        await message.answer('Ошибка: не удалось идентифицировать пользователя!', reply_markup=cmd_start)
        return

    sucess = await set_user_role(user_id, new_role)
    if sucess:
        await message.answer(f'Роль пользователя изменена на {new_role}', reply_markup=cmd_start)
    else:
        await message.answer('Возникли проблемы', reply_markup=cmd_start)

    await state.clear()


@teacher_router.message(or_f(Command('set_parent'), F.text == 'Установить связь'))
async def set_parent_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Нет ни одного ученика или с программой что-то не так.', reply_markup=cmd_start())
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='student_parent')
    await message.answer('Выберите ученика, для которого хотите создать связь', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('student_parent_page:'))
async def student_parent_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='student_parent')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('student_parent:'))
async def student_parent(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    await state.update_data({'student_id': student_id})
    parents = await get_all_parents()

    if not parents:
        await callback.answer('Для начала добавьте родителей!', reply_markup = cmd_start)
        await state.clear()
        return

    await state.update_data({'parents': parents})
    kb = create_students_inline_kb(parents, prefix='parent_student')

    await callback.message.edit_text('Выберите родителя с которым необходимо установить связь для выбранного ученика',
                          reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('parent_student_page:'))
async def student_parent_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('parents', [])

    kb = create_students_inline_kb(students, page=page, prefix='parent_student')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('parent_student:'))
async def student_parent(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, parent_id_str = callback.data.split(':')
    parent_id = int(parent_id_str)

    data = await state.get_data()
    student_id = data.get('student_id', [])


    success = await add_parent_child(parent_id, student_id)
    if success:
        await callback.message.answer(f'Родитель {parent_id} привязан к ребенку {student_id}',
                             reply_markup=cmd_start)

    else:
        await callback.message.answer('Возникла ошибка, проверьте корректность введенных данных',
                              reply_markup=cmd_start)
    await state.clear()


@teacher_router.message(or_f(Command('remove_parent'), F.text == 'Удалить связь'))
async def remove_parent_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer('У вас недостаточно прав!',
                             reply_markup=cmd_start)
        return

    parents = await get_all_parents()
    if not parents:
        await message.answer('Нет пользователей-родителей', reply_markup=cmd_start)
        return

    await state.update_data({'parents': parents})
    kb = create_students_inline_kb(parents, prefix='parent_child_remove')
    await message.answer('Выберите родителя, у которого хотите удалить связь', reply_markup=kb)

@teacher_router.callback_query(F.data.startswith('parent_child_remove_page:'))
async def remove_parent_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    parents = data.get('parents', [])

    kb = create_students_inline_kb(parents, page=page, prefix='parent_child_remove')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('parent_child_remove:'))
async def student_parent(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, parent_id_str = callback.data.split(':')
    parent_id = int(parent_id_str)

    await state.update_data({'parent_id': parent_id})
    students = await get_children_to_parent(parent_id)

    if not students:
        await callback.answer('Для начала добавьте учеников этому родителю!', reply_markup = cmd_start)
        await state.clear()
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='child_parent_remove')

    await callback.message.edit_text('Выберите ученика с которым необходимо удалить связь',
                          reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('child_parent_remove_page:'))
async def student_parent_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='child_parent_remove')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('child_parent_remove:'))
async def student_parent(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    data = await state.get_data()
    parent_id = data.get('parent_id', [])


    success = await remove_parent_child(parent_id, student_id)
    if success:
        await callback.message.answer(f'Родитель {parent_id} отвязан от ребенка {student_id}',
                             reply_markup=cmd_start)

    else:
        await callback.message.answer('Возникла ошибка, проверьте корректность введенных данных',
                              reply_markup=cmd_start)
    await state.clear()



@teacher_router.message(F.text, StateFilter('waiting_for_ids_remove'))
async def process_remove_parent(message: types.Message, state: FSMContext):
    try:
        parent_id, student_id = message.text.split(maxsplit=1)
        parent_id, student_id = int(parent_id), int(student_id)
    except ValueError:
        await message.answer('Ошибка ввода!'
                             'Введите Введите через пробел ID родителя и ID ребенка без ошибок',
                             reply_markup=cmd_start)
        await state.clear()
        return

    success = await remove_parent_child(parent_id, student_id)
    if success:
        await message.answer(f'Родитель {parent_id} больше не привязан к ребенку {student_id}',
                             reply_markup=teacher_kbrd)
    else:
        await message.answer('Возникла ошибка, проверьте корректность введенных данных',
                             reply_markup=teacher_kbrd)
    await state.clear()



@teacher_router.message(F.text == 'Результаты ученика')
async def show_results_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('У Вас недостаточно прав доступа.', reply_markup=cmd_start)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Пока нет зарегистрированных учеников')
        return

    await state.update_data({'students': students})

    kb = create_students_inline_kb(students, prefix='student_lessons')

    await message.answer('Выберите учеников', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('student_lessons_page:'))
async def process_student_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='student_lessons')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('student_lessons:'))
async def process_student_lesson(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    lessons = await get_lessons(student_id)
    if not lessons:
        await callback.message.answer(f'У ученика {student.id} нет занятий')
    else:
        text = ''
        for lesson in lessons:
            text += (f"\n📅 {lesson.date}: "
                     f"ДЗ - {lesson.hw_res}, "
                     f"Урок - {lesson.cw_res}, "
                     f"Тест - {lesson.test_res}")
        await callback.message.answer(f"Последние занятия ученика {student_id}:{text}", reply_markup=cmd_start)

    await callback.answer()

@teacher_router.message(F.text == 'Оценить урок')
async def create_lesson_start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer(f'У Вас недостаточно прав!', reply_markup=cmd_start)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Пока нет зарегистрированных учеников')
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='newlesson_student')

    await message.answer('Выберите учеников', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('newlesson_student_page:'))
async def newlesson_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='newlesson_student')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('newlesson_student:'))
async def choose_student_newlesson(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    await state.update_data({'student_id': student_id})
    await callback.message.answer("Введите результаты урока одной строкой, через запятую.\n"
        "Например: \"ДЗ на 80%, Активно работал, Тест на 90%\"")

    await state.set_state('waiting_for_new_lesson_data')
    await callback.answer()


@teacher_router.message(F.text, StateFilter('waiting_for_new_lesson_data'))
async def process_new_lesson_data(message: Message, state: FSMContext):
    data = await state.get_data()
    student_id = data['student_id']

    parts = message.text.split(';')
    hw_res = parts[0].strip() if len(parts) > 0 else '-'
    cw_res = parts[1].strip() if len(parts) > 1 else '-'
    test_res = parts[2].strip() if len(parts) > 2 else '-'

    success = await add_lesson(student_id, hw_res, cw_res, test_res)
    if success:
        await message.answer(            f"Добавлен урок для ученика {student_id}:\n"
            f"ДЗ: {hw_res}\n"
            f"Классная работа: {cw_res}\n"
            f"Тест: {test_res}", reply_markup=cmd_start)

    else:
        await message.answer('Ошибка при создании урока')

    await state.clear()


@teacher_router.message(F.text == 'Посмотреть связи')
async def show_childs_parent(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('Недостаточно прав', reply_markup=cmd_start)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Что-то не так с вашей функцией или программой', reply_markup=cmd_start)
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='show_parent_child')
    await message.answer('Выберите ученика, связи которого хотите посмотреть: ', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('show_parent_child_page:'))
async def show_parent_child_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page, prefix='show_parent_child')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('show_parent_child:'))
async def show_parent_child(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    success = await show_child_parents(student_id)
    if not success:
        await callback.answer('У ученика нет родителей', reply_markup=cmd_start)
        await state.clear()
        return

    parent_list = '\n'.join([f'{parent.telegram_id}: {parent.full_name}' for parent in success])
    await callback.message.answer(parent_list, reply_markup=cmd_start)
    await state.clear()


@teacher_router.message(F.text == 'Получить выгрузку')
async def export_lessons(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('Недостаточно прав', show_alert=True)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Нет учеников или что-то не так с программой', reply_markup=cmd_start)
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='export_lessons')
    await message.answer('Выберите студента, для которого необходимо сформировать выгрузку', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('export_lessons_page:'))
async def export_lessons_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])
    kb = create_students_inline_kb(students, page=page, prefix='export_lessons')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('export_lessons:'))
async def export_lessons(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
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

@teacher_router.message(F.text == 'Изменить урок')
async def change_lesson_date(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('Недостаточно прав', show_alert=True)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Нет учеников или что-то не так с программой', reply_markup=cmd_start)
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='change_lesson')
    await message.answer('Выберите студента, у которого необходимо изменить урок', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('change_lesson_page:'))
async def change_lesson_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])
    kb = create_students_inline_kb(students, page=page, prefix='change_lesson')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('change_lesson:'))
async def change_lesson_date(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    await state.update_data({'student_id': student_id})
    lessons = await get_all_lessons(student_id=student_id)
    if not lessons:
        await callback.message.answer('У ученика нет уроков')
        await callback.answer()
        return
    await state.update_data({'lessons': lessons})

    kb = create_lessons_inline_kb(lessons, page=1, page_size=5, prefix='choose_lesson_to_change')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer("Выберите урок, дату которого хотите изменить:")


@teacher_router.callback_query(F.data.startswith('choose_lesson_to_change_page:'))
async def choose_lesson_to_change_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer("Недостаточно прав!", show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    lessons = data.get('lessons', [])

    kb = create_lessons_inline_kb(lessons, page=page, page_size=5, prefix='choose_lesson_to_change')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('choose_lesson_to_change:'))
async def choose_lesson_to_change(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer("Недостаточно прав!", show_alert=True)
        return

    _, lesson_str = callback.data.split(':')
    lesson_id = int(lesson_str)

    await state.update_data({'lesson_id': lesson_id})
    await callback.message.answer("Введите новую дату для урока (формат: YYYY-MM-DD):")
    await state.set_state('waiting_for_change_lesson')
    await callback.answer()

@teacher_router.message(F.text, StateFilter('waiting_for_change_lesson'))
async def process_change_lesson(message: Message, state: FSMContext):
    data = await state.get_data()
    lesson_id = data.get('lesson_id')
    new_date_str = message.text.strip()

    success = await change_lesson(lesson_id, new_date_str)
    if success:
        await message.answer(f"Дата изменена с {new_date_str}", reply_markup=cmd_start)
    else:
        await message.answer('Ошибка при изменении урока')

    await state.clear()



@teacher_router.message(F.text == 'Удалить урок')
async def delete_lesson_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('Недостаточно прав', show_alert=True)
        return

    students = await get_all_students()
    if not students:
        await message.answer('Нет учеников или что-то не так с программой', reply_markup=cmd_start)
        return

    await state.update_data({'students': students})
    kb = create_students_inline_kb(students, prefix='delete_lesson')
    await message.answer('Выберите студента, у которого необходимо удалить урок', reply_markup=kb)


@teacher_router.callback_query(F.data.startswith('delete_lesson_page:'))
async def delete_lesson_handler_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])
    kb = create_students_inline_kb(students, page=page, prefix='delete_lesson')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('delete_lesson:'))
async def delete_lesson_handler(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, student_id_str = callback.data.split(':')
    student_id = int(student_id_str)

    await state.update_data({'student_id': student_id})
    lessons = await get_all_lessons(student_id=student_id)
    if not lessons:
        await callback.message.answer('У ученика нет уроков')
        await callback.answer()
        return
    await state.update_data({'lessons': lessons})

    kb = create_lessons_inline_kb(lessons, page=1, page_size=5, prefix='choose_lesson_to_delete')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer("Выберите урок который хотите удалить")


@teacher_router.callback_query(F.data.startswith('choose_lesson_to_delete_page:'))
async def choose_lesson_to_delete_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer("Недостаточно прав!", show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    lessons = data.get('lessons', [])

    kb = create_lessons_inline_kb(lessons, page=page, page_size=5, prefix='choose_lesson_to_delete')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()

@teacher_router.callback_query(F.data.startswith('choose_lesson_to_delete:'))
async def choose_lesson_to_delete(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer("Недостаточно прав!", show_alert=True)
        return

    _, lesson_str = callback.data.split(':')
    lesson_id = int(lesson_str)

    success = await delete_lesson(lesson_id)
    if success:
        await callback.message.answer(f'Удален урок {lesson_id}', reply_markup=cmd_start)
    else:
        await callback.message.answer('Ошибка при удалении урока', reply_markup=cmd_start)

    await state.clear()



@teacher_router.message(F.text == 'Удалить пользователя')
async def delete_user(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != 'учитель':
        await message.answer('Недостаточно прав', show_alert=True)
        return

    users = await get_all_users()
    if not users:
        await message.answer('Нет пользователей или что-то не так с программой', reply_markup=cmd_start)
        return

    await state.update_data({'users': users})
    kb = create_students_inline_kb(users, prefix='delete_user')
    await message.answer('Выберите пользователя, которого необходимо удалить', reply_markup=kb)

@teacher_router.callback_query(F.data.startswith('delete_user_page:'))
async def delete_user_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    users = data.get('users', [])
    kb = create_students_inline_kb(users, page=page, prefix='delete_user')
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('delete_user:'))
async def delete_user_choose(callback: CallbackQuery, state: FSMContext):
    # Пользователь выбрал конкретного пользователя для удаления — просим подтверждение
    teacher = await get_user(callback.from_user.id)
    if not teacher or teacher.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, target_id_str = callback.data.split(':', 1)
    target_id = int(target_id_str)

    # Сохраним выбор в state
    await state.update_data({'target_user_id': target_id})

    # Найдём объект пользователя для отображения в тексте (по необходимости)
    # Можно получить его из state 'users' списка:
    data = await state.get_data()
    users = data.get('users', [])
    # попытка найти объект User в списке (если get_all_users возвращал ORM объекты)
    target_user = None
    for u in users:
        # поле может быть telegram_id или id — у тебя используется telegram_id в других местах
        if getattr(u, 'telegram_id', None) == target_id or getattr(u, 'id', None) == target_id:
            target_user = u
            break

    name = target_user.full_name if target_user and getattr(target_user, 'full_name', None) else str(target_id)

    # Подтверждающая клавиатура
    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Да, удалить', callback_data=f'confirm_delete:{target_id}')],
        [InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_delete')]
    ])

    await callback.message.answer(f'Вы уверены, что хотите удалить пользователя {name} (id: {target_id})?', reply_markup=confirm_kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('confirm_delete:'))
async def delete_user_confirm(callback: CallbackQuery, state: FSMContext):
    teacher = await get_user(callback.from_user.id)
    if not teacher or teacher.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, target_id_str = callback.data.split(':', 1)
    target_id = int(target_id_str)

    # Защита от удаления учителей (чтобы не удалить коллегу/себя случайно)
    target_user = await get_user(target_id)
    if target_user and getattr(target_user, 'role', None) == 'учитель':
        await callback.message.answer('Нельзя удалять пользователей с ролью "учитель".', reply_markup=cmd_start)
        await callback.answer()
        await state.clear()
        return

    # Удаляем
    success = await del_user(target_id)
    if success:
        await callback.message.answer(f'Пользователь {target_id} успешно удалён.', reply_markup=cmd_start)
    else:
        await callback.message.answer('Не удалось удалить пользователя. Возможно он уже отсутствует.', reply_markup=cmd_start)

    await callback.answer()
    await state.clear()


@teacher_router.callback_query(F.data == 'cancel_delete')
async def delete_user_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Удаление отменено.', reply_markup=cmd_start)
    await callback.answer()
    await state.clear()
