import aiohttp
import logging
from aiogram import types, Bot, filters

import datetime as dt
from data.config import DB_API
from utils import messages
from utils.api import db, awg
from keyboards.inline import gen_inline


async def buy_info(
    payload: types.CallbackQuery
):
    await payload.answer()
    await payload.message.answer(
        text=messages.buy_info,
        reply_markup=gen_inline()
    )


async def cmd_buy(
    message: types.Message,
    bot: Bot,
    expiration_date: str | None = None,
):
    is_subscribed = expiration_date is not None
    if is_subscribed:
        await message.reply(
            text=messages.PAYMENT_UNAVAILABLE_ALREADY_SUBSCRIBED,
            reply_markup=gen_inline()
        )
        return

    parts = message.text.split()
    is_test = False

    if len(parts) >= 2 and parts[1] == "test":
        is_test = True
        if len(parts) < 3 or not parts[2].isdigit():
            await message.answer(
                text="Для тестовой оплаты укажите: /buy test {количество_дней}",
                reply_markup=gen_inline()
            )
            return
        amount = int(parts[2])
    elif len(parts) >= 2 and parts[1].isdigit():
        amount = int(parts[1])
    else:
        await message.answer(
            event=message,
            text=messages.PAYMENT_WRONG_INPUT,
            reply_markup=gen_inline()
        )
        return

    prices = [types.LabeledPrice(label="XTR", amount=amount)]
    payload = f"test_{amount}_days" if is_test else f"{amount}_days"

    message = await message.answer_invoice(
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
    is_test = message.successful_payment.invoice_payload.startswith("test_")

    async with aiohttp.ClientSession() as session:
        awg_id = await awg.create_client(
            name=str(message.chat.id),
            session=session
        )

        success = await db.update_user(
            id=message.chat.id,
            username=message.chat.username,
            awg_id=awg_id,
            expires_at=dt.datetime.strftime(dt.datetime.now() + dt.timedelta(
                days=message.successful_payment.total_amount + 1), "%Y-%m-%dT%H:%M:%S.000Z"),
            session=session
        )

    await message.answer(
        text=messages.PAYMENT_PROCESSED_SUCCESS if success else messages.PAYMENT_PROCESSED_FAIL,
        reply_markup=gen_inline()
    )

    if is_test:
        refund = await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id
        )

        if refund is True:
            logging.info(
                f"Возврат произведен успешно: {message.successful_payment.telegram_payment_charge_id}")
        else:
            logging.error(
                f"Возврат не удался: {message.successful_payment.telegram_payment_charge_id}")
