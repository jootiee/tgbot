import logging
from aiogram import Bot
from datetime import datetime as dt

from data.config import ADMIN_ID
from utils import messages


async def on_startup(bot: Bot):
    try:
        await bot.send_message(
            ADMIN_ID,
            messages.STARTUP
        )
    except Exception as err:
        logging.exception(err)


async def on_shutdown(bot: Bot):
    try:
        await bot.send_message(
            ADMIN_ID,
            messages.SHUTDOWN
        )
    except Exception as err:
        logging.exception(err)
