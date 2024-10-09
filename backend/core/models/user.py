from core.models.base import Base

from sqlalchemy import Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum


class State(str, enum.Enum):
    active = "Active"
    inactive = "Inactive"
    suspended = "Suspended"


class User(Base):
    tg_id: Mapped[int] = mapped_column(
        unique=True, 
        nullable=False,
    )

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    expiration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        Enum(State)
    )

    profile_url: Mapped[str] = mapped_column(
        nullable=False
    )