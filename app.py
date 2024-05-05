import asyncio

from loader import bot, storage, db, poller, logging
from utils.poller import Poller


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    await asyncio.sleep(10)
    await on_startup_notify(dp)
    poller.edit_data(await db.get_data())
    asyncio.create_task(poller.check())
    logging.info('Polling started')
    

async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)