from aiogram.types import Message, CallbackQuery
import aiohttp
from data.config import API_URL

from datetime import datetime
from utils import messages
from keyboards.inline import gen_inline


async def start(payload: Message | CallbackQuery, is_subscribed: bool):
        if is_subscribed:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{API_URL}/users/{payload.from_user.id}/') as rg:
                    if (rg.status // 100) == 2:
                        user = await rg.json()
                        expiration_date = user['expiration_date']
                        profile_url = user['profile_url']

                        text = messages.gen_main_subscribed(
                            expiration_date, 
                            profile_url
                        )

        else:
            text = messages.main_unsubscribed
        
        if isinstance(payload, CallbackQuery):
            await payload.message.answer(text=text,
                                reply_markup=gen_inline(flag='main')
                                )
            await payload.answer()
        else:
            await payload.answer(text=text,
                                reply_markup=gen_inline(flag='main')
                                )


async def help(payload: Message | CallbackQuery):
    if isinstance(payload, CallbackQuery):
        await payload.message.answer(text=messages.help,
                            reply_markup=gen_inline(flag='help')
                                                    # status=status)
        )

        await payload.answer()
    else:
        await payload.answer(text=messages.help,
                            reply_markup=gen_inline(flag='help')
        )


async def unknown_query(message: Message):
    print(message)
    await message.answer(text=messages.unknown_query)
