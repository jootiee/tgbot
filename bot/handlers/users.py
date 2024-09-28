from aiogram import types

from utils.messages import message_greet, message_help, message_unknown_query
from keyboards.inline import gen_inline

async def start(payload: types.Message | types.CallbackQuery):
    match type(payload):
        case types.Message:
            await payload.answer(text=message_greet,
                                reply_markup=gen_inline(flag='main')
                                )
        case types.CallbackQuery:
            await payload.message.answer(text=message_greet,
                                reply_markup=gen_inline(flag='main')
                                )
            
            await payload.answer()

async def help(payload: types.Message | types.CallbackQuery):
    match type(payload):
        case types.Message:
            await payload.answer(text=message_help,
                                reply_markup=gen_inline(flag='help')
                                                        # status=status)
            )
        case types.CallbackQuery:
            await payload.message.answer(text=message_help,
                                reply_markup=gen_inline(flag='help')
                                                        # status=status)
            )

            await payload.answer()



async def unknown_query(message: types.Message):
    await message.answer(text=message_unknown_query)
