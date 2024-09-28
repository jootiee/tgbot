__all__ = [
    "register_user_handlers",
]

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import BotCommand, ContentType
from handlers.users import start, help, unknown_query
from handlers.payment import purchase, pre_checkout_query, successful_payment


def create_commands():
    bot_commands = [
        ('start', 'Начать диалог с ботом'),
        ('help', 'Вывести справку о работе бота'),
    ]
    return [BotCommand(command=cmd[0], description=cmd[1]) for cmd in bot_commands]


def register_user_handlers(router: Router):
    router.message.register(start, Command(commands=['start']))
    router.callback_query.register(start, F.data == 'main_menu')

    router.message.register(help, Command(commands=['help']))
    router.callback_query.register(help, F.data == 'help')

    router.message.register(purchase, Command(commands=['buy']))
    router.callback_query.register(purchase, F.data == "buy")

    router.pre_checkout_query.register(pre_checkout_query)
    router.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)

    router.message.register(unknown_query)