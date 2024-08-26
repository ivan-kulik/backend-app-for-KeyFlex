from core.models import Profile, User
from core.repositories.profile import ProfileRepository
from . import achievements_service
from core.schemas.profile import GetProfileData


class ProfileService:
    def __init__(
        self,
        profile_repo: ProfileRepository,
    ):
        self.profile_repo: ProfileRepository = profile_repo()

    async def create_profile(self, username: str):
        data = {
            "user_reference": username,
        }
        profile: Profile = await self.profile_repo.add_one(data)
        await achievements_service.create_achievements_row(
            profile.id,
        )
        return profile

    async def update_profile(self, cur_user: User, profile_update: dict):
        await self.profile_repo.update_profile_data(
            cur_user=cur_user,
            profile_update_data=profile_update,
        )

    async def get_profile_data(self, cur_user: User):
        data = await self.profile_repo.get_profile_data(
            cur_user=cur_user,
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
