from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .profile import Profile


class Achievements(Base):
    __tablename__ = "achievements"

    profile_id: Mapped[int] = mapped_column(
        ForeignKey(
            Profile.id,
            ondelete="CASCADE",
        ),
        unique=True,
        index=True,
    )

    forty_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    fifty_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    sixty_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    seventy_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    eighty_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    ninety_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    one_hundred_characters_per_minute: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="achievements",
    )
