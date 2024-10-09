from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from core.models.user import State


class UserBase(BaseModel):
    tg_id: int
    status: State = State.inactive
    profile_url: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    start_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    start_date: Optional[datetime]
    expiration_date: Optional[datetime]
    