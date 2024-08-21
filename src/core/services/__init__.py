__all__ = ("achievements_service",)

from .achievements import AchievementsService
from core.repositories import AchievementsRepository


achievements_service: AchievementsService = AchievementsService(
    AchievementsRepository,
)
