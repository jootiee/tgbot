from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    chat_id: int
    message_id: int


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    