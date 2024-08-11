from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTable,
)
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .base import Base
from .user import User
from core.types.user_id import UserIdType


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[UserIdType], Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer, ForeignKey(User.id, ondelete="cascade"), nullable=False
        )
