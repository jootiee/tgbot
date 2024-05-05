from aiogram import types

from loader import dp, db
import keyboards as kb

@dp.message_handler()
async def unknown_command(message: types.Message):
    text = 'Неизвестная команда\.'

    status = await db.get_data(field='status',
                               user_id=message.chat.id)

    await message.answer(text,
                         reply_markup=kb.gen_inline(status=status))
