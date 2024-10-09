from typing import Type
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserUpdate
from core.models import User


async def get_users(
        session: AsyncSession
) -> list[User]:
    req = select(User).order_by(User.id)
    result: Result = await session.execute(req)
    users = result.scalars().all()
    return list(users)

async def get_user_by_tg_id(
        session: AsyncSession,
        tg_id: int
) -> User | None:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one()
    return user

async def create_user(
        session: AsyncSession,
        user_in: UserCreate
) -> User:
    user = User(
        tg_id=user_in.tg_id,
        status=user_in.status,
        profile_url=user_in.profile_url
    )
    session.add(user)
    await session.commit()
    return user

async def delete_user_by_tg_id(
        session: AsyncSession,
        tg_id: int
) -> bool:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()
    if user is None:
        return False
    await session.delete(user)
    await session.commit()
    return True

async def update_user_by_tg_id(
        session: AsyncSession,
        tg_id: int,
        user_in: UserUpdate,
) -> User | None:
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()
    if user is None:
        return user
    for name, value in user_in.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(user, name, value)
    await session.commit()
    await session.refresh(user)
    return user