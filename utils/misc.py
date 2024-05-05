from aiogram import types

async def update_message(message: types.Message, new_text: str):
    await message.edit_text(new_text)