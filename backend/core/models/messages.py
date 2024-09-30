from backend.core.models.base import Base

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column

# if TYPE_CHECKING:
    # from backend.core.models.user import User

class Messages(Base):
    chat_id: Mapped[int] = mapped_column(
        nullable=False
    )

    message_id: Mapped[int] = mapped_column(
        nullable=False
    )