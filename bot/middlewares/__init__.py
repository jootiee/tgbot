__all__ = ['IsSubscribedMiddleware']

import aiohttp
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

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
        if type(event) is CallbackQuery:
            event = event.message
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/users/{event.chat.id}/') as rg:
                user = await rg.json()
                if (rg.status // 100) == 2:
                    # # passing data to handlers
                    user = await rg.json()
                    data['is_subscribed'] = user['status'] == 'Active'
                else:
                    async with session.post(f'{API_URL}/users/', json={"id": event.chat.id,
                                                                       "username": event.chat.username}) as rg:
                        # # TODO: log instead of print
                        if (rg.status // 100) == 2:
                            print("user is created")
                        else:
                            print("unable to create user")
                    data['is_subscribed'] = False
        return await handler(event, data)