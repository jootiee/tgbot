__all__ = ['IsSubscribedMiddleware']

import aiohttp
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

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
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            username = event.from_user.username
        elif isinstance(event, Message):
            user_id = event.chat.id
            username = event.chat.username
        else:
            return await handler(event, data)
            
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}/users/{user_id}/') as rg:
                if (rg.status // 100) == 2:
                    user = await rg.json()
                    data['is_subscribed'] = user['active']
                else:
                    async with session.post(f'{API_URL}/users/', json={"id": user_id,
                                                                      "username": username}) as rg:
                        print(API_URL)
                        if (rg.status // 100) == 2:
                            print("user is created")
                        else:
                            print("unable to create user")
                    data['is_subscribed'] = False
        return await handler(event, data)