from aiogram.types import Message, LabeledPrice
from aiogram.utils import markdown
from keyboards.inline import gen_inline
from utils import messages
from utils.api import db, awg
import logging
import datetime as dt
import aiohttp


async def buy_test(
    message: Message,
):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer(
            text="Для тестовой оплаты укажите\\: /buy_test \\{количество_дней\\}",
            reply_markup=gen_inline()
        )
        return
    amount = int(parts[1])

    prices = [LabeledPrice(label="XTR", amount=1)]
    payload = f"test_{amount}_days"

    message = await message.answer_invoice(
        title="Test payment",
        description=f"Тестовая оплата подписки на {amount} дней.",
        prices=prices,
        payload=payload,
        currency="XTR"
    )


async def get_clients(
    payload: Message
):
    async with aiohttp.ClientSession() as session:
        clients = await db.get_users(session=session)

    if clients is None:
        await payload.answer(
            text=messages.ADMIN_GET_CLIENTS_FAILURE,
            reply_markup=gen_inline(flag='admin')
        )
        return

    for client in clients:
        await payload.answer(
            text=messages.ADMIN_CLIENT_INFO.format(
                client["id"],
                client["username"],
                messages.pretty_date(client["expires_at"]),
                client["awg_id"].replace("-", "\\-")
            )
        )


async def add_client(
    payload: Message
):
    parts = payload.text.split()
    if len(parts) != 4:
        await payload.answer(
            text=messages.ADMIN_ADD_CLIENT_WRONG_INPUT,
            reply_markup=gen_inline(flag='admin')
        )

    async with aiohttp.ClientSession() as session:
        awg_id = await awg.create_client(
            name=parts[1],
            session=session
        )

        success = await db.update_user(
            id=int(parts[1]),
            username=parts[2],
            awg_id=awg_id,
            expires_at=dt.datetime.strftime(dt.datetime.now() + dt.timedelta(
                days=int(parts[3]) + 1), "%Y-%m-%dT%H:%M:%S.000Z"),
            session=session
        )

    if success:
        await payload.answer(
            text=messages.ADMIN_ADD_CLIENT_SUCCESS.format(awg_id),
            reply_markup=gen_inline(flag='admin')
        )
    else:
        await payload.answer(
            text=messages.ADMIN_ADD_CLIENT_FAILURE.format(parts[1], parts[2]),
            reply_markup=gen_inline(flag="admin")
        )


async def refund(
    payload: Message
):
    parts = payload.text.split()

    if len(parts) != 2:
        await payload.answer(
            text=messages.ADMIN_REFUND_PAYMENT_WRONG_INPUT,
            reply_markup=gen_inline(flag='admin')
        )
        return

    success = await payload.bot.refund_star_payment(
        user_id=payload.from_user.id,
        telegram_payment_charge_id=parts[1]
    )

    if success:
        await payload.answer(
            text=messages.ADMIN_REFUND_PAYMENT_SUCCESS.format(parts[1]),
            reply_markup=gen_inline(flag='admin')
        )

        logging.info(
            f"Возврат произведен успешно: {parts[1].replace("-", "\\-")}"
        )
    else:
        logging.error(
            f"Возврат не удался: {parts[1].replace("-", "\\-")}"
        )
