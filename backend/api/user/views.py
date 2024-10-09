from pydantic import StrictBool
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import User, UserCreate, UserUpdate
from core.models import db_helper

router = APIRouter(tags=['Users'], prefix='/users')


@router.get('/', response_model=list[User])
async def get_users(
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_users(session=session)

@router.post('/', response_model=User)
async def create_user(
        user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)

@router.get('/{tg_id}/', response_model=User)
async def get_user_by_tg_id(
        tg_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_user_by_tg_id(session=session, tg_id=tg_id)

@router.delete("/{tg_id}/", response_model=StrictBool)
async def delete_user_by_tg_id(
    tg_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.delete_user_by_tg_id(session=session, tg_id=tg_id)
    if not result:
        raise HTTPException(status_code=404, detail='User not found')

@router.patch("/{tg_id}/", response_model=User)
async def update_user_by_tg_id(
    tg_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.update_user_by_tg_id(session=session, tg_id=tg_id, user_in=user_in)
    if not result:
        raise HTTPException(status_code=404, detail='User not found')

    return result
    