from aiohttp import ClientSession
from typing import Optional
from data.config import DB_API


async def get_user(
    id: int,
    session: ClientSession
) -> Optional[dict]:
    async with session.get(f'{DB_API}/users/{id}/') as rg:
        if (rg.status // 100) == 2:
            user = await rg.json()
            return user
        return None


async def create_user(
    id: int,
    username: str,
    session: ClientSession
) -> bool:
    async with session.post(f'{DB_API}/users/', json={
        "id": id,
        "username": username}
    ) as rg:
        if (rg.status // 100) == 2:
            return True
        return False


async def update_user(
    id: int,
    username: str,
    awg_id: str,
    expires_at: str,
    session: ClientSession
) -> bool:
    async with session.patch(f'{DB_API}/users/{id}/', json={
        "id": id,
        "username": username,
        "awg_id": awg_id,
        "expires_at": expires_at}
    ) as rg:
        if (rg.status // 100) == 2:
            return True
        return False
