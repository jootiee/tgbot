import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart

from middlewares import IsSubscribedMiddleware, MessageTrackerMiddleware
from data.config import BOT_TOKEN
from utils.notify_admins import on_startup, on_shutdown
from handlers import register_user_handlers, create_commands


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='MarkdownV2'))
    dp = Dispatcher()
    router = Router()
    router.message.middleware(IsSubscribedMiddleware())
    router.callback_query.middleware(IsSubscribedMiddleware())
    dp.include_router(router)

    await bot.set_my_commands(commands=create_commands())
    # TODO:
    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)

    register_user_handlers(router)
    

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s - [%(levelname)s] - [%(name)s] - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    asyncio.run(main())