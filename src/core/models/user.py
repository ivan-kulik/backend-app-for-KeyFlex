from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, TYPE_CHECKING

from .base import Base
from core.types.user_id import UserIdType
from core.utils.user_database import CustomSQLAlchemyUserDatabase

if TYPE_CHECKING:
    from .oauth_account import OAuthAccount
    from .profile import Profile
    from .statistics_data import StatisticsData


class User(Base, SQLAlchemyBaseUserTable[UserIdType]):
    username: Mapped[str] = mapped_column(
        String(length=20), unique=True, index=True, nullable=False
    )

    oauth_accounts: Mapped[List["OAuthAccount"]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    profile: Mapped["Profile"] = relationship(
        back_populates="user",
    )
    statistics_data: Mapped["StatisticsData"] = relationship(
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: AsyncSession):
        return CustomSQLAlchemyUserDatabase(
            session,
            User,
        )

    def __repr__(self) -> str:
        return f"<User: {self.username!r}>"
