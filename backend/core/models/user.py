from core.models.base import Base

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        unique=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    awg_id: Mapped[str] = mapped_column(
        nullable=True
    )
