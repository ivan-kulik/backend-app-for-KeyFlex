from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, Optional
from datetime import datetime

from .base import Base
from .user import User

if TYPE_CHECKING:
    from .achievements import Achievements


class Profile(Base):
    user_reference: Mapped[str] = mapped_column(
        ForeignKey(User.username),
        unique=True,
    )

    touch_typing: Mapped[bool] = mapped_column(
        default=False,
    )
    keyboard_type: Mapped[Optional[str]] = mapped_column(
        String,
    )
    profession: Mapped[Optional[str]] = mapped_column(
        String,
    )
    location: Mapped[Optional[str]] = mapped_column(
        String,
    )
    register_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.date,
    )
    about_user: Mapped[Optional[str]] = mapped_column(
        String,
    )

    user: Mapped["User"] = relationship(
        back_populates="profile",
    )
    achievements: Mapped["Achievements"] = relationship(
        back_populates="profile",
    )
