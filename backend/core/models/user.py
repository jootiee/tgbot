from core.models.base import Base

from sqlalchemy import Enum, DateTime
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

    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    expiration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    active: Mapped[bool] = mapped_column(
        nullable=False
    )

    profile_url: Mapped[str] = mapped_column(
        nullable=True
    )