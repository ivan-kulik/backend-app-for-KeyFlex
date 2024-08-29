from core.repositories import (
    ProfileRepo,
    AchievementsRepo,
)
from core.models import AchievementsEnum


class AchievementsService:
    def __init__(self, repo: AchievementsRepo):
        self.repo: AchievementsRepo = repo()

    async def create_achievements_row(self, profile_id):
        data = {
            "profile_id": profile_id,
        }
        await self.repo.create_achievements_row(
            initial_data=data,
        )

    async def get_achievements_to_update_status(self, symbols_per_minute: int):
        achievements_to_update_status = []
        for achieve in AchievementsEnum:
            if symbols_per_minute <= achieve.value:
                break
            achievements_to_update_status.append(achieve.name)
        return achievements_to_update_status

    async def change_achievement_status(
        self,
        user_reference: str,
        symbols_per_minute: int,
    ):
        achievements_to_update_status = await self.get_achievements_to_update_status(
            symbols_per_minute=symbols_per_minute,
        )
        profile_id = await ProfileRepo().get_profile_id(
            user_reference=user_reference,
        )
        await self.repo.change_achievements_status(
            profile_id=profile_id,
            achievements_to_update_status=achievements_to_update_status,
        )

    async def get_achievements(self, profile_id: int):
        data = await self.repo.get_achievements(profile_id=profile_id)

        achievements = {
            title: val for title, val in data.__dict__.items() if type(val) is bool
        }
        return achievements
