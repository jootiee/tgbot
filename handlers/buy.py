from aiogram import types

from loader import dp, db
import keyboards as kb

@dp.callback_query_handler(lambda query: query.data == 'buy')
async def process_query_buy(callback_query: types.CallbackQuery):
    text = "Для приобретения подписки пишите в личку @jootiee\.\nПосле оплаты\, нажмите на кнопку *Я оплатил* снизу"

    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.pay)

 
@dp.callback_query_handler(lambda query: query.data == 'payment')
async def query_payment(callback_query: types.CallbackQuery):
    # TODO
    # await send_payment_info(callback_query.from_user.id, callback_query.from_user.username)

    text = 'Пожалуйста\, подождите\, пока я проверяю вашу оплату\.'

    await callback_query.message.edit_text(text)

    await callback_query.message.edit_reply_markup(reply_markup=kb.gen_inline())

    await db.add_user(user_id=callback_query.from_user.id,
                      state='in_process')
