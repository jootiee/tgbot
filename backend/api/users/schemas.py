from pydantic import BaseModel, ConfigDict

from core.models.users import State


class UserBase(BaseModel):
    tg_id: int
    status: State = State.inactive
    profile_url: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    