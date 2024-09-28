import logging
from datetime import datetime as dt

from aiogram import Dispatcher

from data.config import ADMIN_ID


# async def on_startup(dp: Dispatcher):
async def on_startup():
    pass
    # try:
        # await dp.bot.send_message(ADMIN_ID, "Bot is running" + str(dt.now()))
    # except Exception as err:
        # logging.exception(err)

async def on_shutdown():
    pass