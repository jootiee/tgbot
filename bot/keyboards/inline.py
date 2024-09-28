from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

BUTTONS = {'admin_panel_main':      {"text": 'Админ панель',           "callback_data": 'admin_panel_main'},
           'admin_panel_stats':     {"text": 'Статистика сервера',     "callback_data": 'admin_panel_stats'},
           'admin_panel_suspend':   {"text": 'Приостановить подписку', "callback_data": 'admin_panel_suspend'},
           'admin_panel_resume':    {"text": 'Возобновить подписку',   "callback_data": 'admin_panel_resume'},
           'admin_panel_new':       {"text": 'Выдать подписку',        "callback_data": 'admin_panel_new'},
           'admin_panel_all_users': {"text": 'Список пользователей',   "callback_data": 'admin_panel_all_users'},
           'payment_accept':        {"text": 'Подтвердить',            "callback_data": 'payment_accept'},
           'payment_decline':       {"text": 'Отказать',               "callback_data": 'payment_decline'},

           'status':                {"text": 'Статус подписки',        "callback_data": 'status'},
           'buy':                   {"text": 'Приобрести подписку',    "callback_data": 'buy'},
           'help':                  {"text": 'Помощь',                 "callback_data": 'help'}, 
           'main_menu':             {"text": 'Главное меню',           "callback_data": 'main_menu'},
           'main_menu_active':      {"text": 'Главное меню',           "callback_data": 'status'},
           'payment':               {"text": 'Я оплатил',              "callback_data": 'payment'},
}


def gen_inline(flag='other', status='inactive', admin=False):
    reply_kb = InlineKeyboardBuilder()
    reply_kb.adjust(1)

    if flag == 'main':
        if admin:
            reply_kb.button(**BUTTONS['admin_panel_main'])
        else:
            if status == 'active':
                reply_kb.button(**BUTTONS['status'])
                
            if status != 'in_process':
                reply_kb.button(**BUTTONS['buy'])
        reply_kb.button(**BUTTONS['help'])

    elif flag == 'help':
        if status == "active":
            reply_kb.button(**BUTTONS['main_menu_active'])                 
        else:
            reply_kb.button(**BUTTONS['main_menu'])

    elif flag == 'status':
        reply_kb.button(**BUTTONS['help'])

    elif flag == 'admin_main':
        reply_kb.button(**BUTTONS['admin_panel_stats'])
        reply_kb.button(**BUTTONS['admin_panel_all_users'])
        reply_kb.button(**BUTTONS['admin_panel_new'])
        reply_kb.button(**BUTTONS['admin_panel_resume'])
        reply_kb.button(**BUTTONS['admin_panel_suspend'])
        reply_kb.button(**BUTTONS['main_menu'])
    else:
        if status == "active":
            reply_kb.button(**BUTTONS['main_menu_active'])
        else:
            reply_kb.button(**BUTTONS['main_menu'])
        if admin == True:
            reply_kb.button(**BUTTONS['admin_panel_main'])
        else:
            reply_kb.button(**BUTTONS['help'])
    
    return reply_kb.as_markup()

