from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = {'admin_panel_main':      InlineKeyboardButton(text='Админ панель',           callback_data='admin_panel_main'),
           'admin_panel_stats':     InlineKeyboardButton(text='Статистика сервера',     callback_data='admin_panel_stats'),
           'admin_panel_suspend':   InlineKeyboardButton(text='Приостановить подписку', callback_data='admin_panel_suspend'),
           'admin_panel_resume':    InlineKeyboardButton(text='Возобновить подписку',   callback_data='admin_panel_resume'),
           'admin_panel_new':       InlineKeyboardButton(text='Выдать подписку',        callback_data='admin_panel_new'),
           'admin_panel_all_users': InlineKeyboardButton(text='Список пользователей',   callback_data='admin_panel_all_users'),
           'payment_accept':        InlineKeyboardButton(text='Подтвердить',            callback_data='payment_accept'),
           'payment_decline':       InlineKeyboardButton(text='Отказать',               callback_data='payment_decline'),

           'status':                InlineKeyboardButton(text='Статус подписки',        callback_data='status'),
           'buy':                   InlineKeyboardButton(text='Приобрести подписку',    callback_data='buy'),
           'help':                  InlineKeyboardButton(text='Помощь',                 callback_data='help'), 
           'main_menu':             InlineKeyboardButton(text='Главное меню',           callback_data='main_menu'),
           'main_menu_active':      InlineKeyboardButton(text='Главное меню',           callback_data='status'),
           'payment':               InlineKeyboardButton(text='Я оплатил',              callback_data='payment'),
}

def gen_inline(flag='other', status='inactive', admin=False):
    reply_kb = InlineKeyboardMarkup(row_width=1)

    if flag == 'main':
        if admin:
            reply_kb.add(BUTTONS['admin_panel_main'])
        else:
            if status == 'active':
                reply_kb.add(BUTTONS['status'])
            if status != 'in_process':
                reply_kb.add(BUTTONS['buy'])
        reply_kb.add(BUTTONS['help'])

    elif flag == 'help':
        reply_kb.add(BUTTONS['main_menu_active']
                     if status == 'active' else
                     BUTTONS['main_menu'])

    elif flag == 'status':
        reply_kb.add(BUTTONS['help'])

    elif flag == 'admin_main':
        reply_kb.add(BUTTONS['admin_panel_stats'],
                     BUTTONS['admin_panel_all_users'],
                     BUTTONS['admin_panel_new'],
                     BUTTONS['admin_panel_resume'],
                     BUTTONS['admin_panel_suspend'],
                     BUTTONS['main_menu'])
    else:
        reply_kb.add(BUTTONS['main_menu_active']
                     if status == 'active' else
                     BUTTONS['main_menu'], 
                     BUTTONS['admin_panel_main'] 
                     if admin else
                     BUTTONS['help']
        )
    
    return reply_kb



pay = InlineKeyboardMarkup(row_width=1).add(BUTTONS['payment'],
                                            BUTTONS['main_menu'])

#############################
# ADMIN

pay_confirm = InlineKeyboardMarkup(row_width=2).add(BUTTONS['payment_accept'],
                                                    BUTTONS['payment_decline'])