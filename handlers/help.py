from aiogram import types

from loader import dp, db
import keyboards as kb

@dp.callback_query_handler(lambda query: query.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    text = "По вопросом писать @jootiee\."
    
    await callback_query.message.edit_text(text)

    status = await db.get_data('status',
                               user_id=callback_query.from_user.id)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline(flag='help', 
                                                                              status=status))
