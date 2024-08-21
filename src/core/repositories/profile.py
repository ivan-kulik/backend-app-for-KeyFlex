from sqlalchemy import select

from core.db.db_helper import db_helper
from core.models.profile import Profile
from .base_repository import SQLAlchemyRepository


class ProfileRepository(SQLAlchemyRepository):
    model = Profile

    async def get_profile_data(self, cur_user):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(
                self.model.user_reference == cur_user.username,
            )
            data = await session.scalar(stmt)
            return data

    async def update_profile_data(self, cur_user, profile_update_data):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(
                self.model.user_reference == cur_user.username,
            )
            profile_data = await session.scalar(stmt)
            for name, value in profile_update_data.model_dump(
                exclude_unset=True
            ).items():
                setattr(profile_data, name, value)
            await session.commit()
