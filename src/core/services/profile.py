from core.models import Profile, User
from core.repositories import (
    ProfileRepo,
    AchievementsRepo,
)
from core.schemas.profile import GetProfileData
from .achievements import AchievementsService


achievements_service: AchievementsService = AchievementsService(
    AchievementsRepo,
)


class ProfileService:
    def __init__(self, repo: ProfileRepo):
        self.repo: ProfileRepo = repo()

    async def create_profile(self, username: str):
        data = {
            "user_reference": username,
        }
        profile_id: Profile = await self.repo.create_profile(
            initial_data=data,
        )
        await achievements_service.create_achievements_row(
            profile_id,
        )

    async def update_profile(self, cur_user: User, profile_update: dict):
        await self.repo.update_profile_data(
            user_reference=cur_user.username,
            profile_update_data=profile_update,
        )

    async def get_profile_data(self, cur_user: User):
        data = await self.repo.get_profile_data(
            user_reference=cur_user.username,
        )
        achievements = await achievements_service.get_achievements(
            profile_id=data.id,
        )

        profile_data = GetProfileData(
            name=data.user_reference,
            touch_typing=data.touch_typing,
            keyboard_type=data.keyboard_type,
            profession=data.profession,
            location=data.location,
            register_date=data.register_date,
            about_user=data.about_user,
            achievements=achievements,
        )
        return profile_data
