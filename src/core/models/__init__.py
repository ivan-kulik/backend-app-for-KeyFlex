__all__ = (
    "Base",
    "User",
    "OAuthAccount",
    "Achievements",
    "StatisticsData",
    "StandardModeStats",
    "ExtendedModeStats",
    "TextModeStats",
    "EnglishModeStats",
    "ExtremeModeStats",
    "UserModeStats",
)

from .base import Base
from .user import User
from .profile import Profile
from .oauth_account import OAuthAccount
from .achievements import Achievements

from .statistics_data import (
    StatisticsData,
    StandardModeStats,
    ExtendedModeStats,
    TextModeStats,
    EnglishModeStats,
    ExtremeModeStats,
    UserModeStats,
)

from enum import Enum


class StatsModelsEnum(Enum):
    standard_mode = StandardModeStats
    extended_mode = ExtendedModeStats
    text_mode = TextModeStats
    english_mode = EnglishModeStats
    extreme_mode = ExtremeModeStats
    user_mode = UserModeStats


class AchievementsEnum(Enum):
    forty_characters_per_minute = 40
    fifty_characters_per_minute = 50
    sixty_characters_per_minute = 60
    seventy_characters_per_minute = 70
    eighty_characters_per_minute = 80
    ninety_characters_per_minute = 90
    one_hundred_characters_per_minute = 100
