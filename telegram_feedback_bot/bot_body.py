import logging

import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from database import init_db
from handlers import teacher, parent, student, start

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(teacher.teacher_router)
dp.include_router(parent.parent_router)
dp.include_router(student.student_router)
dp.include_router(start.router)

async def main():
    await init_db()
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info('Бот запущен')
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())