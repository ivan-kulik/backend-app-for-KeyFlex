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
    "standard": StandardModeStatsRepository,
    "extended": ExtendedModeStatsRepository,
    "text": TextModeStatsRepository,
    "english": EnglishModeStatsRepository,
    "extreme": ExtremeModeStatsRepository,
    "user": UserModeStatsRepository,
}
