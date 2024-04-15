from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup

# inline_btn_buy = InlineKeyboardButton(text='Приобрести подписку', callback_data='button_buy')
# inline_btn_status = InlineKeyboardButton(text='Статус подписки', callback_data='button_subscription_status')
# inline_btn_help = InlineKeyboardButton(text='Помощь', callback_data='button_help')
# inline_btn_back_to_menu = InlineKeyboardButton(text='Назад', callback_data='button_main_menu')

# inline_kb_main_menu = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_buy, inline_btn_status], [inline_btn_help]])

# #inline_kb_main_menu.add(inline_btn_buy, inline_btn_status)
# #inline_kb_main_menu.add(inline_btn_help)
# #inline_kb_main_menu = inline_kb_main_menu.as_markup()

# inline_kb_other = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_back_to_menu]])


reply_kb_main = ReplyKeyboardMarkup(resize_keyboard=True)

reply_kb_main.add('Приобрести подписку', 'Статус подписки').add('Помощь')