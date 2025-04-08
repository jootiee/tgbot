from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    id: int
    username: str
    active: Optional[bool] = False


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    active: Optional[bool] = False
    profile_url: Optional[str]
    start_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    start_date: Optional[datetime]
    expiration_date: Optional[datetime]
    profile_url: Optional[str]
    