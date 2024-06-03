from aiogram import Router, types, F
from aiogram.filters import or_f, StateFilter
from aiogram.filters.command import Command, CommandStart
from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from math import ceil


from handlers.filters import StudentFilter
from addition import keyboards
from exercises import ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10


tasks = 15
tasks_in_page = 5

student_router = Router()
student_router.message.filter(StudentFilter(['private']))

back_kb = keyboards.get_keyboard(
    'Назад',
    'Отмена'
)


# хенлдер на команду /start
@student_router.message(or_f(CommandStart(), (F.text == 'Запустить бота'), (F.text == 'Главное меню')))
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {html.bold(html.quote(message.from_user.full_name))}, исследуй мои возможности!',
                         reply_markup=keyboards.get_keyboard(
                             'Практика',
                             'Личный кабинет',
                             'Как пользоваться ботом',
                             'О проекте',
                             'Оставьте отзыв',
                         ))


@student_router.message(F.text.lower().contains('личный кабинет'))
async def student_account(message: types.Message):
    await message.answer(f'Вот ваш кабинет, {html.bold(html.quote(message.from_user.full_name))}',
                         reply_markup=keyboards.get_keyboard(
                             'Главное меню',
                             'Расскажите о себе',
                             'Статистика',
                         ))


class StudentInfo(StatesGroup):
    full_name = State()
    birth_date = State()
    origin = State()
    school = State()
    level = State()
    about = State()

    texts = {
        'StudentInfo:full_name': 'Введите пожалуйста ваше ФИО, пример - "Иванов Иван Иванович',
        'StudentInfo:birth_date': 'Введите Вашу дату рождения',
        'StudentInfo:origin': 'Введите название города, в котором Вы учитесь',
        'StudentInfo:school': 'Введите название школы в которой Вы учитесь',
        'StudentInfo:level': 'В каком классе вы учитесь?',
    }




@student_router.message(StateFilter(None), F.text.casefold()  == 'расскажите о себе')
async def about_student(message:types.Message, state: FSMContext):
    await message.answer('Если есть желание помочь проекту со статистикой - расскажи немного о себе! Заранее спасибо.')
    await message.answer('Напишите пожалуйста ваше ФИО, пример - "Иванов Иван Иванович',
                         reply_markup=keyboards.get_keyboard(
                             'Меню',
                         ))
    await state.set_state(StudentInfo.full_name)


@student_router.message(F.text.casefold() == 'меню')
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {html.bold(html.quote(message.from_user.full_name))}, исследуй мои возможности!',
                         reply_markup=keyboards.get_keyboard(
                             'Практика',
                             'Личный кабинет',
                             'Как пользоваться ботом',
                             'О проекте',
                             'Оставьте отзыв',
                         ))


@student_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.set_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Действия отменены', reply_markup=keyboards.get_keyboard(
                             'Главное меню',
                             'Расскажите о себе'
                             'Статистика',))

@student_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def back_about(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is StudentInfo.full_name:
        await message.answer('Здесь нет шага назад')
    previous_state = None
    for step in StudentInfo.__all_states__:
        if step == current_state:
            await state.set_state(previous_state)
            await message.answer(f'Вы вернулись назад')
            await message.answer(f'{StudentInfo.texts[previous_state]}')
            return
        previous_state = step


@student_router.message(StudentInfo.full_name, F.text)
async def student_birth(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer('Введите свою дату рождения', reply_markup=back_kb)
    await state.set_state(StudentInfo.birth_date)


@student_router.message(StudentInfo.birth_date, F.text)
async def student_origin(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer('Введите название города в котором вы учитесь', reply_markup=back_kb)
    await state.set_state(StudentInfo.origin)

@student_router.message(StudentInfo.origin, F.text)
async def student_school(message: types.Message, state: FSMContext):
    await state.update_data(school=message.text)
    await message.answer('В каком классе вы учитесь?', reply_markup=back_kb)
    await state.set_state(StudentInfo.level)


@student_router.message(StudentInfo.school, F.text)
async def student_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text)
    await message.answer('Расскажите, почему вы выбрали информатику в качестве предмета для сдачи ОГЭ? Просто так,'
                         'или в дальнейшем хотите связать свою жизнь с информационными науками?')
    await state.set_state(StudentInfo.about)


@student_router.message(StudentInfo.level, F.text)
async def student_about(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    #все данные сохранены, очистим машину состояний, и выйдем из этого меню
    data = await state.get_data()
    await message.answer(f'Спасибо большое, что уделил время опросу. Это важно для развития проекта'
                         f'Надеюсь, что наш бот поможет тебе подготовиться к экзамену')
    await state.clear()
    await message.answer(f'{data}')


@student_router.message(F.text.casefold() == 'как пользоваться ботом')
async def how_use_bot(message: types.message):
    await message.answer('Этот бот является одним из множества проектов системы помощи в подготовке к экзамен'
                         '"лялялякозел". Здесь вы можете ознакомиться получить необходимый теоретический материал для'
                         'решения практических задач из ОГЭ по информатике. Кстати, сами задания здесь'
                         ' тоже генерируются. Тестовые задания проверяются ботом автоматически. Ниже представлены'
                         ' кнопки, нажмите на них, и бот пришлет вам видео гайды по его использованию. Желаем удачи'
                         '')


@student_router.message(F.text.casefold() == 'о проекте')
async def about_project(message: types.Message):
    await message.answer('Автор проекта поставил перед собой задачу помочь обучающимся подготовиться к экзаменам и '
                         'повысить свой уровень знаний в удобной и понятной форме. Проще говоря, обстоятельства бывают'
                         'разные, наша цель - получить достойное образование')


@student_router.message(F.text.casefold() == 'оставьте отзыв')
async def set_feedback(message: types.Message):
    await message.answer('Нам очень важно Ваше мнение о данном продукте. С радостью примем положительные впечатления и '
                         'конструктивную критику.')


# ______________________ теперь начнем прописывать раздел с выводом заданий
def get_tasks(page: int) -> list[str]:
    start = (page - 1) * tasks_in_page
    end = start + 5
    return [f'Задание {i}' for i in range(start+1, end+1)]


@student_router.message(F.text.casefold() == 'практика')
async def theory(message: types.message, state: FSMContext):
    total_pages = ceil(tasks/tasks_in_page)
    page = 1
    btns = get_tasks(page)
    await message.answer('Задания 1-5',
                         reply_markup=keyboards.get_keyboard(*btns, page=page,
                                                             total_pages=tasks, sizes=(1, 2, 2, 2)))
    await state.update_data(page=page, total_pages=total_pages)


@student_router.message(F.text.casefold() == '>>')
async def next_page(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_page, total_pages = data.get('page', 1), data.get('total_pages', 1)
    if current_page < total_pages:
        page = current_page + 1
        btns = get_tasks(page)
        await message.answer(f'Задания {(page-1)*5+1}-{(page-1)*5+5}',
                             reply_markup=keyboards.get_keyboard(*btns, page=page,
                                                                 total_pages=total_pages, sizes=(1, 2, 2, 2)))
        await state.update_data(page=page)


@student_router.message(F.text.casefold() == '<<')
async def next_page(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_page, total_pages = data.get('page', 1), data.get('total_pages', 1)
    if current_page > 1:
        page = current_page - 1
        btns = get_tasks(page)
        await message.answer(f'Задания с {page*5-4}-{page*5}',
                             reply_markup=keyboards.get_keyboard(*btns, page=page,
                                                                 total_pages=total_pages, sizes=(1, 2, 2, 2)))
        await state.update_data(page=page)


class ExerciseInfo(StatesGroup):
    ex_number = State()
    completely = State()
    tries = State()


@student_router.message(F.text.casefold() == 'задание 1')
async def exercise_1(message: types.message):
    await message.answer('Сгенерировано задание 1', reply_markup=keyboards.ex_kb)
    hello_1, res_1 = ex1.ex_1()
    await message.answer(hello_1)


@student_router.message(F.text.casefold() == 'задание 2')
async def exercise_2(message: types.message):
    await message.answer('Сгенерировано задание 2', reply_markup=keyboards.ex_kb)
    hello_2, res_2 = ex2.ex_2()
    await message.answer(hello_2)


@student_router.message(F.text.casefold() == 'задание 3')
async def exercise_3(message: types.message):
    await message.answer('Сгенерировано задание 3', reply_markup=keyboards.ex_kb)
    hello_3, res_3 = ex3.ex_3()
    await message.answer(hello_3)


@student_router.message(F.text.casefold() == 'задание 4')
async def exercise_4(message: types.message):
    await message.answer('Сгенерировано задание 4', reply_markup=keyboards.ex_kb)
    hello_4, res_4 = ex4.ex_4()
    await message.answer(hello_4)


@student_router.message(F.text.casefold() == 'задание 5')
async def exercise_5(message: types.message):
    await message.answer('Сгенерировано задание 5', reply_markup=keyboards.ex_kb)
    hello_5, res_5 = ex5.ex_5()
    await message.answer(hello_5)


@student_router.message(F.text.casefold() == 'задание 6')
async def exercise_6(message: types.message):
    await message.answer('Сгенерировано задание 6', reply_markup=keyboards.ex_kb)
    hello_6, res_6 = ex6.ex_6()
    await message.answer(hello_6)


@student_router.message(F.text.casefold() == 'задание 7')
async def exercise_7(message: types.message):
    await message.answer('Сгенерировано задание 7', reply_markup=keyboards.ex_kb)
    hello_7, res_7 = ex7.ex_7()
    await message.answer(hello_7)


@student_router.message(F.text.casefold() == 'задание 8')
async def exercise_8(message: types.message):
    await message.answer('Сгенерировано задание 8', reply_markup=keyboards.ex_kb)
    hello_8, res_8 = ex8.ex_8()
    await message.answer(hello_8)


@student_router.message(F.text.casefold() == 'задание 9')
async def exercise_9(message: types.message):
    await message.answer('Сгенерировано задание 9', reply_markup=keyboards.ex_kb)
    hello_9, res_9 = ex9.ex_9()
    await message.answer(hello_9)


@student_router.message(F.text.casefold() == 'задание 10')
async def exercise_10(message: types.message):
    await message.answer('Сгенерировано задание 10', reply_markup=keyboards.ex_kb)
    hello_10, res_10 = ex10.ex_10()
    await message.answer(hello_10)



@student_router.message(F.text.casefold() == 'меню')
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {html.bold(html.quote(message.from_user.full_name))}, исследуй мои возможности!',
                         reply_markup=keyboards.get_keyboard(
                             'Практика',
                             'Личный кабинет',
                             'Как пользоваться ботом',
                             'О проекте',
                             'Оставьте отзыв',
                         ))
