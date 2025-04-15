from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    id: int
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    awg_id: Optional[str]
    expires_at: Optional[datetime] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    expires_at: Optional[datetime]
    awg_id: Optional[str]
