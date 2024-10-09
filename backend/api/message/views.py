
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Message, MessageCreate, MessageUpdate 
from core.models import db_helper

router = APIRouter(tags=['Messages'], prefix='/messages')


@router.get('/{chat_id}/', response_model=Message)
async def get_message_by_chat_id(
        chat_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_message_by_chat_id(session=session, chat_id=chat_id)

@router.post('/', response_model=Message)
async def create_message(
        message_in: MessageCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_message(session=session, message_in=message_in)


@router.delete("/{chat_id}/", response_model=None)
async def delete_message_by_chat_id(
    chat_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.delete_message_by_chat_id(session=session, chat_id=chat_id)
    if not result:
        raise HTTPException(status_code=404, detail='Message not found')

@router.patch("/{chat_id}/", response_model=Message)
async def update_message_by_chat_id(
    chat_id: int,
    message_in: MessageUpdate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    result = await crud.update_message_by_chat_id(session=session, chat_id=chat_id, message_in=message_in)
    if not result:
        raise HTTPException(status_code=404, detail='Message not found')

    return result
    