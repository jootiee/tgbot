from aiohttp import ClientSession
from typing import Optional
import logging

from data.config import AWG_API


async def get_clients(
    session: ClientSession
) -> Optional[dict]:
    async with session.get(f"{AWG_API}/client/") as rg:
        if (rg.status // 100) == 2:
            return await rg.json()
        else:
            print("Unable to get clients")
            return None


async def create_client(
    name: str,
    session: ClientSession
) -> Optional[str]:
    async with session.post(f"{AWG_API}/client", json={
        "name": name
    }) as rg:
        if (rg.status // 100) == 2:
            return await get_id(name, session)
        logging.error("Unable to create client:", rg.json)


async def enable_client(
    id: str,
    session: ClientSession
) -> bool:
    async with session.post(f'{AWG_API}/client/{id}/enable') as rg:
        if (rg.status // 100) == 2:
            return True
        else:
            logging.error("Unable enable client:", rg.json)
            return False


async def disable_client(
    id: str,
    session: ClientSession
) -> bool:
    async with session.post(f'{AWG_API}/client/{id}/disable') as rg:
        if (rg.status // 100) == 2:
            return True
        else:
            logging.error("Unable disable client:", rg.json)
            return False


async def get_id(
    name: str,
    session: ClientSession
) -> Optional[str]:
    clients = await get_clients(session)
    for client in clients:
        if client['name'] == name:
            return client['id']
    return None


async def get_qr(
    name: str,
    session: ClientSession
) -> Optional[str]:
    awg_id = await get_id(name, session)
    async with session.get(f'{AWG_API}/client/{awg_id}/qrcode.svg') as rg:
        if (rg.status // 100) == 2:
            return await rg.text()
        else:
            logging.error("Unable to get qr code:", rg.json)
            return None


async def get_conf(
    name: str,
    session: ClientSession
) -> Optional[str]:
    awg_id = await get_id(name, session)
    async with session.get(f'{AWG_API}/client/{awg_id}/configuration') as rg:
        if (rg.status // 100) == 2:
            return await rg.text()
        else:
            logging.error("Unable to get qr code:", rg.json)
            return None
