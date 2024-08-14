from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.mixins import RelationshipMixin
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
    standard_mode: Mapped["StandardModeStats"] = relationship(
        back_populates="statistics_data",
    )
    extended_mode: Mapped["ExtendedModeStats"] = relationship(
        back_populates="statistics_data",
    )
    text_mode: Mapped["TextModeStats"] = relationship(
        back_populates="statistics_data",
    )
    english_mode: Mapped["EnglishModeStats"] = relationship(
        back_populates="statistics_data",
    )
    extreme_mode: Mapped["ExtremeModeStats"] = relationship(
        back_populates="statistics_data",
    )
    user_mode: Mapped["UserModeStats"] = relationship(
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


class StandardModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "standard_mode_stats"

    __relation_name__ = "standard_mode"


class ExtendedModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "extended_mode_stats"

    __relation_name__ = "extended_mode"


class TextModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "text_mde_stats"

    __relation_name__ = "text_mode"


class EnglishModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "english_mode_stats"

    __relation_name__ = "english_mode"


class ExtremeModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "extreme_mode_stats"

    __relation_name__ = "extreme_mode"


class UserModeStats(
    Base,
    BaseStats,
    RelationshipMixin,
):
    __tablename__ = "user_mode_stats"

    __relation_name__ = "user_mode"
