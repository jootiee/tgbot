from aiogram.types import Message, CallbackQuery, BufferedInputFile
from typing import Optional, Union
import aiohttp
from cairosvg import svg2png
import io


from utils import messages
from utils.api import awg
from keyboards.inline import gen_inline


async def start(
    payload: Union[Message, CallbackQuery],
    expires_at: Optional[str] = None,
):
    is_subscribed = expires_at is not None
    if is_subscribed:
        text = messages.gen_main_subscribed(expires_at)
    else:
        text = messages.main_unsubscribed

    if isinstance(payload, CallbackQuery):
        await payload.answer()
        payload = payload.message

    await payload.answer(
        text=text,
        reply_markup=gen_inline(flag='subscribed' if is_subscribed else 'main')
    )


async def help(
    payload: Union[Message, CallbackQuery]
):
    if isinstance(payload, CallbackQuery):
        await payload.answer()
        payload = payload.message

    await payload.answer(
        text=messages.help,
        reply_markup=gen_inline(flag='help')
    )


async def get_qr(
    payload: CallbackQuery
):
    await payload.answer()

    async with aiohttp.ClientSession() as session:
        svg_data = await awg.get_qr(str(payload.from_user.id), session)
    # TODO: send photo from storing channel
    if svg_data is not None:
        filename = f"{payload.from_user.id}.png"
        await payload.answer()
        await payload.message.answer_photo(
            photo=BufferedInputFile(svg2png(svg_data), filename=filename),
            reply_markup=gen_inline()
        )
        return

    await payload.message.answer(
        text=messages.NOT_FOUND,
        reply_markup=gen_inline()
    )


async def get_conf(
    payload: CallbackQuery
):
    await payload.answer()

    async with aiohttp.ClientSession() as session:
        conf_data = await awg.get_conf(str(payload.from_user.id), session)
    # TODO: send config file from storing channel
    if conf_data is not None:
        await payload.message.answer_document(
            document=BufferedInputFile(conf_data.encode(
                "utf-8"), filename="configuration.conf"),
            reply_markup=gen_inline()
        )
        return

    await payload.message.answer(
        text=messages.NOT_FOUND,
        reply_markup=gen_inline()
    )


async def unknown_query(
    message: Message
):
    await message.answer(
        text=messages.UNKNOWN_QUERY,
        reply_markup=gen_inline()
    )
