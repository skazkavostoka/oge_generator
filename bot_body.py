import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from tortoise import Tortoise

from handlers.student import student_router

load_dotenv(find_dotenv())


#включим логирование
logging.basicConfig(level=logging.INFO)

#создадим объект бота с разметкой текста html
bot = Bot(token=os.getenv('token'), parse_mode='HTML')
bot.my_admins_list = []

storage = MemoryStorage()

#диспетчер и роутеры
dp = Dispatcher(storage=storage)
dp.include_router(student_router)


async def start_db():
    await Tortoise.init(
        db_url=f'postgres://{os.getenv("db_admin")}:{os.getenv("db_password")}@{os.getenv("db_host")}'
               f':{os.getenv("db_port")}/{os.getenv("db_name")}',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


#запуск бота
async def main():
    await start_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
