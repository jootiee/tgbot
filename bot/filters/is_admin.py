from typing import Union, List
from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from data.config import ADMIN_ID


class IsAdmin(BaseFilter):
    async def __call__(
        self,
        event: Union[Message, CallbackQuery], bot: Bot
    ) -> bool:
        user_id = event.from_user.id

        return user_id == int(ADMIN_ID)
