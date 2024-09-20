from sqlalchemy import select, insert

from core.utils.db_helper import db_helper
from core.models.profile import Profile


class ProfileRepo:
    model = Profile

    async def get_profile_id(self, user_reference: str):
        async with db_helper.session_factory() as session:
            stmt = select(self.model.id).where(
                self.model.user_reference == user_reference,
            )
            res = await session.scalar(stmt)
        return res

    async def create_profile(self, initial_data):
        async with db_helper.session_factory() as session:
            stmt = insert(self.model).values(**initial_data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
        return res.scalar_one()

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
            for name, value in profile_update_data.items():
                setattr(profile_data, name, value)
            await session.commit()
