__all__ = [
    "register_user_handlers",
]

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import BotCommand, ContentType

from filters import IsAdmin
from handlers.admin import get_clients, add_client, refund, buy_test
from handlers.users import start, help, unknown_query, get_qr, get_conf
from handlers.payment import buy_info, cmd_buy, pre_checkout_query, successful_payment


def create_commands():
    bot_commands = [
        ('start', 'Начать диалог с ботом'),
        ('help', 'Вывести справку о работе бота'),
        ('buy', 'Приобрести подписку на n дней')
    ]
    return [BotCommand(command=cmd[0], description=cmd[1]) for cmd in bot_commands]


def register_user_handlers(router: Router):
    router.message.register(
        start,
        Command(commands=['start'])
    )
    router.callback_query.register(
        start,
        F.data == 'main_menu'
    )

    router.message.register(
        help,
        Command(commands=['help'])
    )
    router.callback_query.register(
        help,
        F.data == 'help'
    )

    router.callback_query.register(
        buy_info,
        F.data == 'buy'
    )

    router.message.register(
        cmd_buy,
        Command(commands=['buy'])
    )

    router.pre_checkout_query.register(
        pre_checkout_query
    )

    router.message.register(
        successful_payment,
        F.content_type == ContentType.SUCCESSFUL_PAYMENT
    )

    router.callback_query.register(
        get_qr,
        F.data == 'qr'
    )

    router.callback_query.register(
        get_conf,
        F.data == 'conf'
    )

    router.message.register(
        get_clients,
        Command(commands=['clients']),
        IsAdmin()
    )

    router.message.register(
        add_client,
        Command(commands=['add']),
        IsAdmin()
    )

    router.message.register(
        refund,
        Command(commands=['refund']),
        IsAdmin()
    )

    router.message.register(
        buy_test,
        Command(commands=['buy_test']),
        IsAdmin()
    )

    router.message.register(
        unknown_query,
        F.content_type != ContentType.REFUNDED_PAYMENT
    )
