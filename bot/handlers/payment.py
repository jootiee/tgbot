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
    is_subscribed: bool
):
    if is_subscribed:
        await message.answer("Вы не можете купить подписку, так как она у вас уже активна\.")
        return  

    parts = message.text.split()
    is_test = False
        
    if len(parts) >= 2 and parts[1] == "test":
        is_test = True
        if len(parts) < 3 or not parts[2].isdigit():
            await message.answer("Для тестовой оплаты укажите: /buy test {количество_дней}")
            return
        amount = int(parts[2])
    elif len(parts) >= 2 and parts[1].isdigit():
        amount = int(parts[1])
    else:
        await message.answer("Через пробел необходимо указать целое число \- желаемую длительность подписки в днях\. Попробуйте еще раз\.")
        return

    prices = [types.LabeledPrice(label="XTR", amount=amount)]
    payload = f"test_{amount}_days" if is_test else f"{amount}_days"

    await message.answer_invoice(
        title="Test payment" if is_test else "Subscription payment",
        description=f"{'Тестовая оплата' if is_test else 'Оплата'} подписки на {amount} дней.",
        prices=prices,
        payload=payload,
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
    # with open('transactions.txt', 'w') as f:
    #     f.write(f"{message.successful_payment.telegram_payment_charge_id} - {message.successful_payment.total_amount}\n")
    is_test = message.successful_payment.invoice_payload.startswith("test_")

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            url=f'{API_URL}/users/{message.chat.id}',
            json={
                'id': message.chat.id,
                'username': message.chat.username,
                'active': True,
                'profile_url': gen_url(),
                'start_date': dt.datetime.strftime(dt.datetime.now(), "%Y-%m-%dT%H:%M:%S.000Z"),
                'expiration_date': dt.datetime.strftime(dt.datetime.now() + dt.timedelta(days=message.successful_payment.total_amount + 1), "%Y-%m-%dT%H:%M:%S.000Z")
            }
        ) as req:
            if (req.status // 100) == 2:
                await message.answer("Оплата проведена успешно\.", reply_markup=gen_inline())
            else:
                await message.answer("Возникла ошибка при попытке оплаты\. Обратитесь в поддержку\.", reply_markup=gen_inline())

        if is_test:
            refund = await bot.refund_star_payment(
                user_id=message.from_user.id,
                telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id
            )


            if refund is True:
                # await message.answer("Возврат произведен успешно\.")
                print("Возврат произведен успешно.")
            else:
                # await message.answer("Возврат не удался\.")
                print("Возврат не удался.")
    