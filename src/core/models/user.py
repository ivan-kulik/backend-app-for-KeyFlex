from fastapi_users.db import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import List, TYPE_CHECKING

from .base import Base
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from .oauth_account import OAuthAccount
    from .profile import Profile


class User(Base, SQLAlchemyBaseUserTable[UserIdType]):
    username: Mapped[str] = mapped_column(
        String(length=20), unique=True, index=True, nullable=False
    )
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, User)

    def __repr__(self) -> str:
        return f"<User: {self.username!r}>"
