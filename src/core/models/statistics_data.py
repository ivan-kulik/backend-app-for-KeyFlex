from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class StatisticsData(Base):
    __tablename__ = "statistics_data"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id),
        unique=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="statistics_data",
    )


class BaseStats:
    __abstract__ = True

    statistics_id: Mapped[int] = mapped_column(
        ForeignKey(StatisticsData.id),
        unique=True,
    )

    accuracy_percentage_for_each_attempt: Mapped[ARRAY] = mapped_column(
        ARRAY(Integer),
    )
    characters_per_minute_for_each_attempt: Mapped[ARRAY] = mapped_column(
        ARRAY(Integer),
    )
    average_accuracy: Mapped[int] = mapped_column(
        Integer,
    )


class StandardModeStats(Base, BaseStats):
    __tablename__ = "standard_mode_stats"


class ExtendedModeStats(Base, BaseStats):
    __tablename__ = "extended_mode_stats"


class TextModeStats(Base, BaseStats):
    __tablename__ = "text_mode_stats"


class EnglishModeStats(Base, BaseStats):
    __tablename__ = "english_mode_stats"


class ExtremeModeStats(Base, BaseStats):
    __tablename__ = "extreme_mode_stats"


class UserModeStats(Base, BaseStats):
    __tablename__ = "user_mode_stats"
