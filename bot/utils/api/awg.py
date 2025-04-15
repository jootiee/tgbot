from aiohttp import ClientSession
from typing import Optional
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
        print("Unable to create client:", rg.json)


async def enable_client(
    id: str,
    session: ClientSession
) -> bool:
    async with session.post(f'{AWG_API}/client/{id}/enable') as rg:
        if (rg.status // 100) == 2:
            return True
        else:
            print("Unable enable client:", rg.json)
            return False


async def disable_client(
    id: str,
    session: ClientSession
) -> bool:
    async with session.post(f'{AWG_API}/client/{id}/disable') as rg:
        if (rg.status // 100) == 2:
            return True
        else:
            print("Unable disable client:", rg.json)
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
            print("Unable to get qr code:", rg.json)
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
            print("Unable to get qr code:", rg.json)
            return None

# if __name__ == "__main__":
#     import asyncio
#     from aiohttp import ClientSession
#     AWG_API = "http://localhost:51821/api/wireguard"

#     async def main():
#         async with ClientSession() as session:
#             id = "269317391"
#             res = await get_conf(id, session)

#     asyncio.run(main())
