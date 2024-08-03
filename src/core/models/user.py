from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base
from core.types.user_id import UserIdType


class User(Base, SQLAlchemyBaseUserTable[UserIdType]):
    username: Mapped[str] = mapped_column(
        String(length=20), unique=True, index=True, nullable=False
    )
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, User)
