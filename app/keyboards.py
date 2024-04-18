from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def gen_inline(flag='other', active_subscription=False, admin=False):
    reply_kb = InlineKeyboardMarkup(row_width=1)

    if flag == 'main':
        return reply_kb.add((InlineKeyboardButton(text='Статус подписки',       callback_data='status') 
                             if active_subscription else 
                             InlineKeyboardButton(text='Приобрести подписку',   callback_data='buy')),
                             InlineKeyboardButton(text='Помощь',                callback_data='help')
                             #TODO: добавить админку
        )
        
    if flag == 'help':
        return reply_kb.add(InlineKeyboardButton( text='Главное меню',           callback_data='status')
                            if active_subscription else
                            InlineKeyboardButton( text='Главное меню',           callback_data='main_menu')
        )
    if flag == 'status':
        return reply_kb.add(InlineKeyboardButton( text='Помощь',                 callback_data='help'))
    if flag == 'other':
        return reply_kb.add(InlineKeyboardButton( text='Главное меню',           callback_data='status')
                            if active_subscription else
                            InlineKeyboardButton( text='Главное меню',           callback_data='main_menu'), 
                            InlineKeyboardButton( text='Помощь',                 callback_data='help')
        )



pay = InlineKeyboardMarkup(row_width=1)
pay.add(                    InlineKeyboardButton( text='Я оплатил',              callback_data='payment'),
                            InlineKeyboardButton( text='Главное меню',           callback_data='main_menu')
)

#############################
# ADMIN

pay_confirm = InlineKeyboardMarkup(row_width=2)
pay_confirm.add(            InlineKeyboardButton( text='Подтвердить',            callback_data='payment_accept'),
                            InlineKeyboardButton( text='Отказать',               callback_data='payment_decline')
)

