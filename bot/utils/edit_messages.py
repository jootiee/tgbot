import aiohttp
from typing import Optional, Union, Dict, Any
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from data.config import API_URL

async def send_or_edit_message(
    event: Union[Message, CallbackQuery],
    text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
    parse_mode: str = "MarkdownV2"
) -> Dict[str, Any]:
    """
    Handles message flow:
    - Deletes user message if it's a new message
    - Edits bot's previous message or sends a new one if no previous message exists
    Returns the sent/edited message.
    """
    chat_id = event.from_user.id if isinstance(event, CallbackQuery) else event.chat.id
    
    # Delete user's message if it's a new message (not a callback)
    if isinstance(event, Message):
        try:
            await event.delete()
        except Exception as e:
            print(f"Failed to delete user message: {e}")
    
    # Try to get existing message_id from database
    message_id = None
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/messages/{chat_id}/") as rg:
                if rg.status == 200:
                    data = await rg.json()
                    message_id = data.get("message_id")
        except Exception as e:
            print(f"Error fetching message: {e}")
    
    # Edit existing message or send a new one
    if message_id:
        # Get the bot instance
        bot = event.bot if isinstance(event, Message) else event.message.bot
        
        # Try to edit the existing message
        try:
            result = await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return result
        except Exception as e:
            print(f"Error editing message: {e}")
            # If editing fails (e.g., message is too old), we'll send a new one
    
    # Send new message if we don't have a previous one or editing failed
    if isinstance(event, CallbackQuery):
        result = await event.message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    else:
        result = await event.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    
    # Store message in database
    message_id = result.message_id
    async with aiohttp.ClientSession() as session:
        try:
            # Try to update existing message or create new one
            message_data = {
                "chat_id": chat_id,
                "message_id": message_id
            }
            
            # First try to update existing entry
            async with session.patch(f"{API_URL}/messages/{chat_id}/", json=message_data) as response:
                if response.status != 200:
                    # If update fails, create a new entry
                    async with session.post(f"{API_URL}/messages/", json=message_data) as create_response:
                        if create_response.status != 200 and create_response.status != 201:
                            print(f"Failed to store message: {await create_response.text()}")
        except Exception as e:
            print(f"Error storing message: {e}")
    
    return result
