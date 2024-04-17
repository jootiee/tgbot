from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# def gen(flag='other'):
    # reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)

    # if flag == 'main':
        # return reply_kb.add('Приобрести подписку', 'Статус подписки').add('Помощь')
    # if flag == 'help':
        # return reply_kb.add('Главное меню')
    # if flag == 'other':
        # return reply_kb.add('Главное меню').add('Помощь')

def gen_inline(flag='other', active_subscription=False, admin=False):
    reply_kb = InlineKeyboardMarkup(row_width=2)

    if flag == 'main':
        return reply_kb.add((InlineKeyboardButton(text='Статус подписки',       callback_data='status') 
                             if active_subscription else 
                             InlineKeyboardButton(text='Приобрести подписку',   callback_data='buy')),
                             InlineKeyboardButton(text='Помощь',                callback_data='help')
                             #TODO: добавить админку
        )
        
    if flag == 'help':
        return reply_kb.add(InlineKeyboardButton( text='Главное меню',           callback_data='main_menu')
        )
    if flag == 'other':
        return reply_kb.add(InlineKeyboardButton( text='Главное меню',           callback_data='main_menu'), 
                            InlineKeyboardButton( text='Помощь',                 callback_data='help')
        )



pay = InlineKeyboardMarkup(row_width=1)
pay.add(                    InlineKeyboardButton( text='Я оплатил',              callback_data='payment'),
                            InlineKeyboardButton( text='Главное меню',           callback_data='main_menu')
)

pay_confirm = InlineKeyboardMarkup(row_width=2)
pay_confirm.add(            InlineKeyboardButton( text='Подтвердить',            callback_data='payment_accept'),
                            InlineKeyboardButton( text='Отказать',               callback_data='payment_decline')
)