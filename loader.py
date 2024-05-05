import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.ex_bridge import EXBridge
from utils.database import Database
from utils.poller import Poller


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN,
          parse_mode=types.message.ParseMode.MARKDOWN_V2,
          disable_web_page_preview=True)

storage = MemoryStorage()

ex = EXBridge(PATH_EX=config.PATH_EX,
              DIR_EX=config.DIR_EX)

db = Database(PATH_DATABASE=config.PATH_DATABASE,
              ex=ex)

poller = Poller(bot=bot)


dp = Dispatcher(bot, storage=storage)