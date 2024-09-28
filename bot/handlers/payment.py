from aiogram import types, Bot

#TODO: add payment logic
async def purchase(payload: types.Message | types.CallbackQuery):
    if type(payload) is types.CallbackQuery:
        await payload.answer()
        payload = payload.message

    await payload.answer_invoice(
        title='Оплата подписки',
        description='Оплата подписки на 1 месяц.',
        payload='one_month_access',
        currency='XTR',
        prices=[types.LabeledPrice(label='XTR', amount=1)]
    )

async def pre_checkout_query(query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(query.id, ok=True)

async def successful_payment(message: types.Message):
    await message.answer("Оплата проведена успешно\.")