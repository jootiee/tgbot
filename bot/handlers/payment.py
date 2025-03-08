import aiohttp
from aiogram import types, Bot

from data.config import API_URL


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
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f'{API_URL}/users/',
            json={
                'tg_id': message.chat.id,
                'status': 'Active',
                'profile_url': message.from_user.username
            }
        ) as req:
            if (req.status // 100) == 2:
                await message.answer(
                    text='success\!',
                    # text='success!',
                )
            await message.answer(
                text='error',
            )

    await message.answer("Оплата проведена успешно\.")
