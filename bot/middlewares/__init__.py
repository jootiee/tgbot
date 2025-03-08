__all__ = ['IsSubscribedMiddleware']

import aiohttp
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from data.config import API_URL
from utils import messages 


class IsSubscribedMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/users/{event.from_user.id}/') as rg:
                user = await rg.json()
                if (rg.status // 100) == 2:
                    # passing data to handlers
                    user = await rg.json()
                    data['is_subscribed'] = user['status'] == 'Active'
                else:
                    # TODO: create new user
                    data['is_subscribed'] = False
        return await handler(event, data)