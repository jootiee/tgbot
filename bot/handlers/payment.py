import aiohttp
from aiogram import types, Bot, filters

import datetime as dt
from data.config import API_URL
from utils.bridge import gen_url
from utils import messages
from keyboards.inline import gen_inline

async def buy_info(
    payload: types.CallbackQuery
):
    await payload.answer(text=messages.buy_info,
                                 reply_markup=gen_inline())

# TEST PAYMENT
async def cmd_buy(
    message: types.Message,
):
    if len(message.text.split()) == 1 or not message.text.split()[1].isdigit():
        await message.answer("Через пробел необходимо указать целое число \- желаемую длительность подписки в днях\. Попробуйте еще раз\.")
        return
    amount = int(message.text.split()[1])
    prices = [types.LabeledPrice(label="XTR", amount=amount)]
    await message.answer_invoice(
        title="Test payment",
        description=f"Тестовая оплата подписки на {amount} дней.",
        prices=prices,
        payload=f"{amount}_days",
        currency="XTR"
    )
    
async def pre_checkout_query(
    query: types.PreCheckoutQuery, 
    bot: Bot
):
    await bot.answer_pre_checkout_query(query.id, ok=True)

async def successful_payment(
    message: types.Message, 
    bot: Bot
):
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            url=f'{API_URL}/users/{message.chat.id}',
            json={
                'id': message.chat.id,
                'username': message.chat.username,
                'status': 'Active',
                'profile_url': gen_url(),
                'start_date': dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%dT%H:%M:%S.000Z"),
                'expiration_date': dt.datetime.strftime(dt.datetime.now() + dt.timedelta(days=30), "%Y-%m-%dT%H:%M:%S.000Z")
            }
        ) as req:
            if (req.status // 100) == 2:
                await message.answer(
                    text='success\!',
                )
            else:
                await message.answer(
                    text='error',
                )

    await message.answer("Оплата проведена успешно\.")
    
    await bot.refund_star_payment(
        user_id=message.from_user.id,
        telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id
    )

    await message.answer("Возврат произведен успешно\.")