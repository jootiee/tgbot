from typing import Type
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import MessageCreate, MessageUpdate
from core.models import Message

async def get_message_by_chat_id(
        session: AsyncSession,
        chat_id: int
) -> Message | None:
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    user = result.scalar_one()
    return user

async def create_message(
        session: AsyncSession,
        message_in: MessageCreate
) -> Message:
    message = Message(**message_in.model_dump())
    session.add(message)
    await session.commit()
    return message

async def delete_message_by_chat_id(
        session: AsyncSession,
        chat_id: int
) -> bool:
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    message = result.scalar_one_or_none()
    if message is None:
        return False
    await session.delete(message)
    await session.commit()
    return True

async def update_message_by_chat_id(
        session: AsyncSession,
        chat_id: int,
        message_in: MessageUpdate,
) -> Type[Message] | None:
    result = await session.execute(select(Message).where(Message.chat_id == chat_id))
    message = result.scalar_one_or_none()
    if message is None:
        return message 
    for name, value in message_in.model_dump(exclude_unset=False).items():
        setattr(message, name, value)
    await session.commit()
    return message