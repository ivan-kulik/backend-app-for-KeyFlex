from fastapi import UploadFile
from io import BytesIO
from pydantic import HttpUrl

from core.models import Profile, User
from core.repositories import (
    ProfileRepo,
    AchievementsRepo,
)
from core.utils.s3_connection import s3_client
from core.schemas.profile import GetProfileData
from core.forms.profile import ProfileUpdateForm
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

    async def create_file_object(self, file: UploadFile) -> BytesIO:
        contents = await file.read()
        fileobj: BytesIO = BytesIO(contents)
        fileobj.seek(0)
        return fileobj

    async def create_object_name(self, cur_user: User) -> str:
        return f"profile_photo: {cur_user.username}"

    async def create_object_url(
        self,
        bucket_url: HttpUrl,
        object_name: str,
    ) -> HttpUrl:
        return f"{bucket_url}/{object_name}"

    async def change_profile_photo(
        self, cur_user: User, profile_photo_file: UploadFile
    ):
        file_object: BytesIO = await self.create_file_object(file=profile_photo_file)
        object_name: str = await self.create_object_name(cur_user=cur_user)
        await s3_client.upload_file(
            object_name=object_name,
            file_object=file_object,
        )
        return await self.create_object_url(
            bucket_url=s3_client.bucket_url,
            object_name=object_name,
        )

    async def get_profile_update_data(self, profile_update: ProfileUpdateForm):
        profile_update_data: dict = {
            key: value for key, value in vars(profile_update).items() if value
        }
        return profile_update_data

    async def update_profile(self, cur_user: User, profile_update: ProfileUpdateForm):
        profile_update_data: dict = await self.get_profile_update_data(
            profile_update=profile_update,
        )

        if profile_photo := profile_update_data.pop("profile_photo", None):
            profile_photo_url = await self.change_profile_photo(
                cur_user=cur_user,
                profile_photo_file=profile_photo,
            )
            profile_update_data["profile_photo_url"] = profile_photo_url

        await self.repo.update_profile_data(
            cur_user=cur_user,
            profile_update_data=profile_update_data,
        )

    async def get_profile_data(self, cur_user: User):
        data = await self.repo.get_profile_data(
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
