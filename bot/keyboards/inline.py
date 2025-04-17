from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

BUTTONS = {'admin_panel_main':      {"text": 'Админ панель',           "callback_data": 'admin_panel_main'},
           'admin_panel_stats':     {"text": 'Статистика сервера',     "callback_data": 'admin_panel_stats'},
           'admin_panel_suspend':   {"text": 'Приостановить подписку', "callback_data": 'admin_panel_suspend'},
           'admin_panel_resume':    {"text": 'Возобновить подписку',   "callback_data": 'admin_panel_resume'},
           'admin_panel_new':       {"text": 'Выдать подписку',        "callback_data": 'admin_panel_new'},
           'admin_panel_all_users': {"text": 'Список пользователей',   "callback_data": 'admin_panel_all_users'},

           'qr':                    {"text": 'QR-код профиля',        "callback_data": 'qr'},
           'conf_file':             {"text": 'Файл профиля',        "callback_data": 'conf'},
           'buy':                   {"text": 'Приобрести подписку',    "callback_data": 'buy'},
           'help':                  {"text": 'Помощь',                 "callback_data": 'help'},
           'main_menu':             {"text": 'Главное меню',           "callback_data": 'main_menu'},
           'main_menu_active':      {"text": 'Главное меню',           "callback_data": 'status'},
           'payment':               {"text": 'Я оплатил',              "callback_data": 'payment'},
           }


def gen_inline(
    flag='other', admin=False
) -> InlineKeyboardMarkup:
    reply_kb = InlineKeyboardBuilder()
    match flag:
        case "main":
            if admin:
                reply_kb.button(**BUTTONS['admin_panel_main'])
            reply_kb.button(**BUTTONS['buy'])
            reply_kb.button(**BUTTONS['help'])

        case 'help':
            reply_kb.button(**BUTTONS['main_menu'])

        case 'subscribed':
            reply_kb.button(**BUTTONS['qr'])
            reply_kb.button(**BUTTONS['conf_file'])
            reply_kb.button(**BUTTONS['help'])
            reply_kb.adjust(2, 1)

        case 'admin_main':
            reply_kb.button(**BUTTONS['admin_panel_stats'])
            reply_kb.button(**BUTTONS['admin_panel_all_users'])
            reply_kb.button(**BUTTONS['admin_panel_new'])
            reply_kb.button(**BUTTONS['admin_panel_resume'])
            reply_kb.button(**BUTTONS['admin_panel_suspend'])
            reply_kb.button(**BUTTONS['main_menu'])
        case _:
            reply_kb.button(**BUTTONS['main_menu'])

    return reply_kb.as_markup()
