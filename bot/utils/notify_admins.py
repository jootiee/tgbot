import logging
from datetime import datetime as dt

from aiogram import Bot

from data.config import ADMIN_ID


async def on_startup(bot: Bot):
    try:
        await bot.send_message(ADMIN_ID, "Bot is running: " + str(dt.strftime(dt.now(), "%Y\\-%m\\-%d %H\\:%M\\:%S")))
    except Exception as err:
        logging.exception(err)


async def on_shutdown(bot: Bot):
    try:
        await bot.send_message(ADMIN_ID, "Bot has stopped: " + str(dt.strftime(dt.now(), "%Y\\-%m\\-%d %H\\:%M\\:%S")))
    except Exception as err:
        logging.exception(err)
