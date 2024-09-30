from backend.core.models.base import Base

from typing import TYPE_CHECKING
from sqlalchemy import Enum, Datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

# if TYPE_CHECKING:
    # from backend.core.models.event import Event

class State(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspened"


class User(Base):
    tg_id: Mapped[int] = mapped_column(
        unique=True, 
        nullable=False)

    start_date: Mapped[datetime] = mapped_column(
        Datetime(timezone=True)
    )

    expiration_date: Mapped[datetime] = mapped_column(
        Datetime(timezone=True)
    )

    status: Mapped[str] = mapped_column(
        Enum(State)
    )

    profile_url: Mapped[str] = mapped_column(
        nullable=False
    )