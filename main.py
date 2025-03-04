import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.apsched import check_outdated
from app.database.models import async_main
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


bot = Bot(token='')
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone ="Europe/Moscow")

async def main():
    await async_main()
    dp.include_router(router)
    scheduler.add_job(check_outdated, misfire_grace_time=360, trigger ='cron', hour = 8, minute = 30, start_date = datetime.now())
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
        bot.session.close()
        scheduler.shutdown()
    except RuntimeError:
        print(f"RuntimeError: looping loops :)")
