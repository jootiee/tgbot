from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def gen(flag='other'):
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if flag == 'main':
        return reply_kb.add('Приобрести подписку', 'Статус подписки').add('Помощь')
    if flag == 'help':
        return reply_kb.add('Главное меню')
    if flag == 'other':
        return reply_kb.add('Главное меню').add('Помощь')


pay = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Я оплатил', callback_data='payment'),
                                            InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

pay_confirm = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Подтвердить', callback_data='payment_accept'),
                                                    InlineKeyboardButton(text='Отказать',    callback_data='payment_decline')
                                                    )