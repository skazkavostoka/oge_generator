from sys import prefix

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram.filters import Command, or_f, StateFilter

from database import *
from keyboards.reply import teacher_kbrd, cmd_start, rmv
from keyboards.inline import create_students_inline_kb
from database import add_parent_child, remove_parent_child, get_user

from database import get_all_students

teacher_router = Router()


@teacher_router.message(or_f(Command("set_role"), F.text == 'Назначить роли'))
async def set_role_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer("❌ У вас нет прав для выполнения этой команды.", reply_markup=cmd_start)
        return

    await message.answer("Введите ID пользователя и новую роль через пробел (пример: `123456789 родитель`)", reply_markup=rmv)

    # Устанавливаем состояние ожидания ввода ID и новой роли
    await state.set_state("waiting_for_role_change")


@teacher_router.message(F.text, StateFilter("waiting_for_role_change"))
async def process_role_change(message: types.Message, state: FSMContext):
    """Обрабатывает изменение роли"""

    try:
        user_id, new_role = message.text.split(maxsplit=1)
        user_id = int(user_id)
    except ValueError:
        await message.answer("❌ Ошибка ввода. Введите ID пользователя и новую роль через пробел.",
                             reply_markup=cmd_start)
        await state.clear()
        return

    success = await set_user_role(user_id, new_role)
    if success:
        await message.answer(f"✅ Роль пользователя {user_id} изменена на {new_role}.",
                             reply_markup=teacher_kbrd)
    else:
        await message.answer("❌ Пользователь не найден.",
                             reply_markup=teacher_kbrd)

    await state.clear()


@teacher_router.message(or_f(Command('set_parent'), F.text == 'Установить связь'))
async def set_parent_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user or user.role != "учитель":
        await message.answer('У вас недостаточно прав!',
                             reply_markup=cmd_start)
        return

    await message.answer('Введите через пробел ID родителя и ID ребенка', reply_markup=cmd_start)

    await state.set_state('waiting_for_ids')


@teacher_router.message(F.text, StateFilter('waiting_for_ids'))
async def process_set_parent(message: types.Message, state: FSMContext):
    try:
        parent_id, student_id = message.text.split(maxsplit=1)
        parent_id, student_id = int(parent_id), int(student_id)
    except ValueError:
        await message.answer('Ошибка ввода!'
                             'Введите Введите через пробел ID родителя и ID ребенка без ошибок',
                             reply_markup=cmd_start)
        await state.clear()
        return

    success = await add_parent_child(parent_id, student_id)
    if success:
        await message.answer(f'Родитель {parent_id} привязан к ребенку {student_id}',
                             reply_markup=teacher_kbrd)
    else:
        await message.answer('Возникла ошибка, проверьте корректность введенных данных',
                             reply_markup=teacher_kbrd)
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


@teacher_router.callback_query(F.data.startswith('students_page:'))
async def process_student_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page)
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


@teacher_router.callback_query(F.data.startswith('newlesson_page'))
async def newlesson_page(callback: CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    if not user or user.role != 'учитель':
        await callback.answer('Недостаточно прав', show_alert=True)
        return

    _, page_str = callback.data.split(':')
    page = int(page_str)

    data = await state.get_data()
    students = data.get('students', [])

    kb = create_students_inline_kb(students, page=page)
    await callback.message.edit_reply_markup(kb)
    await callback.answer()


@teacher_router.callback_query(F.data.startswith('newlesson_student'))
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