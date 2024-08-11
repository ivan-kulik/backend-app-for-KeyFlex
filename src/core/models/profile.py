from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class Profile(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id),
    )

    touch_typing: Mapped[str] = mapped_column(
        String,
    )
    keyboard_type: Mapped[str] = mapped_column(
        String,
    )
    profession: Mapped[str] = mapped_column(
        String,
    )
    location: Mapped[str] = mapped_column(
        String,
    )
    about_user: Mapped[str] = mapped_column(
        String,
    )

    user: Mapped["User"] = relationship(
        back_populates="profile",
    )
