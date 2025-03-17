from sys import prefix
from tracemalloc import Statistic

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.filters import Command, or_f, StateFilter

from database import *
from keyboards.reply import *
from keyboards.inline import create_students_inline_kb
from database import add_parent_child, remove_parent_child, get_user, get_all_users, get_all_students, get_all_parents


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

    students = get_all_students()
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
    parents = get_all_parents()

    if not parents:
        await callback.answer('Для начала добавьте родителей!', reply_markup = cmd_start)
        await state.clear()
        return

    await state.update_data({'parents': parents})
    kb = create_students_inline_kb(parents, prefix='parent_student')

    await callback.answer('Выберите родителя с которым необходимо установить связь для выбранного ученика',
                          reply_markup=kb)



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
        await callback.answer(f'Родитель {parent_id} привязан к ребенку {student_id}',
                             reply_markup=cmd_start)

    else:
        await callback.answer('Возникла ошибка, проверьте корректность введенных данных',
                              reply_markup=cmd_start)
    await state.clear()



@teacher_router.message(or_f(Command('remove_parent'), F.text == 'Удалить связь'))
async def remove_parent_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer('У вас недостаточно прав!',
                             reply_markup=cmd_start)
        return

    await message.answer('Введите через пробел ID родителя и ID ребенка', reply_markup=cmd_start)

    await state.set_state('waiting_for_ids_remove')


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


@teacher_router.callback_query(F.data.startswith('students_lessons_page:'))
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
    await callback.message.edit_reply_markup(kb)
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
    await callback.message.edit_reply_markup(kb)
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

    parts = message.text.split(',')
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