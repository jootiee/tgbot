from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from data import config
import keyboards as kb

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.delete()

    status = await db.get_data('status',
                               user_id=message.chat.id)

    text = "Привет\.\n\nСтоимость подписки\:\nОдин месяц \- _50 рублей_;\nТри месяца \- _135 рублей_;\nПолгода \- _240 рублей_\;\nГод \- _420 рублей_\.\n\nЧтобы купить подписку\, нажми на кнопку снизу ⬇️"


    await message.answer(text, 
                         parse_mode=types.message.ParseMode.MARKDOWN_V2,
                         reply_markup=kb.gen_inline(flag='main', 
                                                    status=status,
                                                    admin=(message.chat.id == config.ID_ADMIN)))


@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def query_main_menu(callback_query: types.CallbackQuery):
    text = "Привет\.\n\nСтоимость подписки\:\nОдин месяц \- _50 рублей_;\nТри месяца \- _135 рублей_;\nПолгода \- _240 рублей_\;\nГод \- _420 рублей_\.\n\nЧтобы купить подписку\, нажми на кнопку снизу ⬇️"

    await callback_query.message.edit_text(text)

    status = await db.get_data(field='status',
                               user_id=callback_query.from_user.id)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(flag='main',
                                                                              status=status,
                                                                              admin=callback_query.from_user.id == config.ID_ADMIN))
