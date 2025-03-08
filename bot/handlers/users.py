from aiogram import types
import aiohttp
from data.config import API_URL

from datetime import datetime
from utils import messages
from keyboards.inline import gen_inline


async def start(payload: types.Message | types.CallbackQuery, is_subscribed: bool):

        if is_subscribed:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'{API_URL}/users/{payload.from_user.id}/') as rg:
                    if (rg.status // 100) == 2:
                        user = await rg.json()
                        start_date = datetime.strptime(user['start_date'][:19], "%Y-%m-%dT%H:%M:%S")
                        expiration_date = datetime.strptime(user['expiration_date'][:19], "%Y-%m-%dT%H:%M:%S")
                        # profile_url = user['profile_url']
                        text = messages.main_subscribed.format("start_date", "expiration_date", 
                                                               messages.format_duration(start_date, expiration_date),
                                                               "guide_link",
                                                               "profile_url")
                        
        else:
            text=messages.main_unsubscribed
        if payload is types.CallbackQuery:
            await payload.message.answer(text=text,
                                reply_markup=gen_inline(flag='main')
                                )
            await payload.answer()
        else:
            await payload.answer(text=text,
                                reply_markup=gen_inline(flag='main')
                                )



async def help(payload: types.Message | types.CallbackQuery):
    match type(payload):
        case types.Message:
            await payload.answer(text=messages.help,
                                reply_markup=gen_inline(flag='help')
            )

        case types.CallbackQuery:
            await payload.message.answer(text=messages.help,
                                reply_markup=gen_inline(flag='help')
                                                        # status=status)
            )

            await payload.answer()


async def unknown_query(message: types.Message):
    await message.answer(text=messages.unknown_query)
