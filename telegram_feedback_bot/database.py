import logging
import os


from sqlalchemy import delete, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from config import DATABASE_URL

from models import Base, User, ParentChild, Lesson

from datetime import date, datetime
import pandas as pd
import openpyxl


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(telegram_id: int, full_name: str, role: str):
    async with AsyncSessionLocal() as session:
        new_user = User(telegram_id=telegram_id, full_name=full_name, role=role)
        session.add(new_user)
        await session.commit()


async def get_user(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first()


async def del_user(telegram_id: int) -> bool:
    async def del_user(telegram_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                q = select(User).where(User.telegram_id == telegram_id)
                res = await session.execute(q)
                user = res.scalar_one_or_none()
                if not user:
                    logging.warning(f"del_user: user not found tg={telegram_id}")
                    return False

                user_pk = user.id
                user_tg = user.telegram_id

                # удаляем уроки
                await session.execute(
                    delete(Lesson).where(
                        or_(Lesson.student_id == user_pk, Lesson.student_id == user_tg)
                    )
                )
                # удаляем связи
                await session.execute(
                    delete(ParentChild).where(
                        or_(
                            ParentChild.parent_id == user_pk,
                            ParentChild.parent_id == user_tg,
                            ParentChild.child_id == user_pk,
                            ParentChild.child_id == user_tg,
                        )
                    )
                )
                # удаляем сам объект
                await session.delete(user)

        logging.info(f"Deleted user tg={telegram_id}")
        return True

async def set_user_role(telegram_id: int, new_role: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if user:
            user.role = new_role
            await session.commit()
            return True
        return False


async def add_parent_child(parent_id: int, child_id: int):
    async with AsyncSessionLocal() as session:
        parent = await session.execute(select(User).where(User.telegram_id == parent_id))
        child = await session.execute(select(User).where(User.telegram_id == child_id))

        if not parent.scalar() or not child.scalar():
            return False

        existing = await session.execute(select(ParentChild).where(ParentChild.parent_id == parent_id,
                                                                   ParentChild.child_id == child_id))
        if existing.scalar():
            return False

        new_relation = ParentChild(parent_id = parent_id, child_id = child_id)
        session.add(new_relation)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False

async def get_children_to_parent(parent_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User)  # Выбираем учеников
            .join(ParentChild, User.telegram_id == ParentChild.child_id)  # Соединяем таблицы по ID ученика
            .where(ParentChild.parent_id == parent_id)  # Фильтруем по родителю
        )
        return result.scalars().all()


async def remove_parent_child(parent_id: int, child_id: int):
    async with AsyncSessionLocal() as session:
        relation = await session.execute(select(ParentChild).where(ParentChild.parent_id == parent_id,
                                ParentChild.child_id == child_id))
        relation = relation.scalar()
        if not relation:
            return False
        await session.delete(relation)
        await session.commit()
        return True

async def add_lesson(student_id: int,
        hw_res: str = '-', cw_res: str='-', test_res: str='-', lesson_date: date=None):
    if lesson_date is None:
        lesson_date = date.today()

    async with AsyncSessionLocal() as session:
        new_lesson = Lesson(
            student_id = student_id,
            date = lesson_date,
            hw_res = hw_res,
            cw_res = cw_res,
            test_res = test_res
        )
        session.add(new_lesson)

        student_name = select(User.full_name).where(User.telegram_id == student_id)

        try:
            await session.commit()
            logging.info(f'Добавлено занятие {new_lesson} для ученика {student_name}, id: {student_id}')
            return True
        except IntegrityError:
            await session.rollback()
            logging.warning(f'Ошибка при добавлении занятия для ученика {student_name}, id: {student_id}')
            return False

async def get_lessons(student_id: int = None):
    async with AsyncSessionLocal() as session:
        query = select(Lesson).order_by(Lesson.date.desc()).limit(5)
        if student_id:
            query = query.where(Lesson.student_id == student_id)

        result = await session.execute(query)
        return result.scalars().all()

async def get_all_lessons(student_id: int = None):
    async with AsyncSessionLocal() as session:
        query = select(Lesson).order_by(Lesson.date.desc())
        if student_id:
            query = query.where(Lesson.student_id == student_id)

        result = await session.execute(query)
        return result.scalars().all()


async def delete_lesson(lesson_id: int):
    async with AsyncSessionLocal() as session:
        query = select(Lesson).where(
            Lesson.id == lesson_id)
        result = await session.execute(query)
        lesson = result.scalar_one_or_none()

        if lesson:
            await session.delete(lesson)
            await session.commit()
            logging.info(f'Удалено занятие ученика {lesson_id}')
            return True

        logging.warning(f'Не получилось удалить занятие ученика {lesson_id}')


async def change_lesson(lesson_id: int,  new_date_str: str):
    try:
        new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
    except ValueError:
        logging.info(f'Некорректный формат даты: {new_date_str}')
        return False

    async with AsyncSessionLocal() as session:
        query = select(Lesson).where(Lesson.id == lesson_id,)
        result = await session.execute(query)
        lesson = result.scalar_one_or_none()

        if not lesson:
            logging.warning(f"Урок  не найден")
            return False
        lesson.date = new_date
        await session.commit()
        logging.info(f'Дата занятия обновлена на {new_date_str}.')
        return True



async def export_lessons_to_excel(student_id: int):
    async with AsyncSessionLocal() as session:
        stmt = (
            select(
                Lesson.student_id,
                User.full_name,
                Lesson.date,
                Lesson.hw_res,
                Lesson.cw_res,
                Lesson.test_res
            )
            .join(User, Lesson.student_id == User.telegram_id)
            .where(Lesson.student_id == student_id)
            .order_by(Lesson.date)
        )

        # Выполняем запрос
        result = await session.execute(stmt)
        lessons = result.all()  # список кортежей

        if not lessons:
            return None

        # Далее формируем DataFrame и сохраняем Excel
        df = pd.DataFrame(
            lessons,
            columns=[
                "ID ученика",
                "ФИО ученика",
                "Дата",
                "Результат ДЗ",
                "Работа на занятии",
                "Результат теста",
            ],
        )

        filename = f"lessons_student_{student_id}_{date.today()}.xlsx"
        filepath = f"/home/artem/bot/oge_generator/telegram_feedback_bot/excel_files/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        df.to_excel(filepath, index=False, engine='openpyxl')

        return filepath


async def get_all_students():
    async with AsyncSessionLocal() as session:
        students = select(User).where(User.role == 'ученик')
        result = await session.execute(students)
        return result.scalars().all()



async def get_all_users():
    async with AsyncSessionLocal() as session:
        users = select(User)
        result = await session.execute(users)
        return result.scalars().all()


async def get_all_parents():
    async with AsyncSessionLocal() as session:
        parents = select(User).where(User.role == 'родитель')
        result = await session.execute(parents)
        return result.scalars().all()


async def show_child_parents(child_tg_id: int):
    async with AsyncSessionLocal() as session:
        query = select(User).join(ParentChild,
                User.telegram_id == ParentChild.parent_id).where(ParentChild.child_id == child_tg_id)

        result = await session.execute(query)
        return result.scalars().all()