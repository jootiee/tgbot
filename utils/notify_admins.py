import logging

from aiogram import Dispatcher

from data.config import ID_ADMIN


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ID_ADMIN, "Бот запущен")
    except Exception as err:
        logging.exception(err)