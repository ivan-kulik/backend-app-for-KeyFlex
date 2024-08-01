from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
)
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str] = mapped_column(
        String(length=20), unique=True, index=True, nullable=False
    )
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
