__all__ = (
    "ProfileRepository",
    "AchievementsRepository",
    "stats_repos",
)

from .profile import ProfileRepository
from .achievements import AchievementsRepository
from .stats import (
    ModesStatsRepository,
    StandardModeStatsRepository,
    ExtendedModeStatsRepository,
    TextModeStatsRepository,
    EnglishModeStatsRepository,
    ExtremeModeStatsRepository,
    UserModeStatsRepository,
)


stats_repos = {
    "standard_mode": StandardModeStatsRepository,
    "extended_mode": ExtendedModeStatsRepository,
    "text_mode": TextModeStatsRepository,
    "english_mode": EnglishModeStatsRepository,
    "extreme_mode": ExtremeModeStatsRepository,
    "user_mode": UserModeStatsRepository,
}
