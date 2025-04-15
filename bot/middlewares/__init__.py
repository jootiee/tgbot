__all__ = ['IsSubscribedMiddleware']

import aiohttp
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

from utils.api import db


class IsSubscribedMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            username = event.from_user.username
        elif isinstance(event, Message):
            user_id = event.chat.id
            username = event.chat.username
        else:
            return await handler(event, data)

        async with aiohttp.ClientSession() as session:
            user = await db.get_user(user_id, session)
            if user is None:
                await db.create_user(user_id, username, session)
            else:
                data['expires_at'] = user['expires_at']

        return await handler(event, data)
