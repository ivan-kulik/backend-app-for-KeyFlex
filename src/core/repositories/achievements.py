from sqlalchemy import select, insert

from core.utils.db_helper import db_helper
from core.models import Achievements


class AchievementsRepo:
    model = Achievements

    async def create_achievements_row(self, initial_data):
        async with db_helper.session_factory() as session:
            stmt = insert(self.model).values(**initial_data)
            await session.execute(stmt)
            await session.commit()

    async def get_achievements(self, profile_id: int):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(
                self.model.profile_id == profile_id,
            )
            data = await session.scalar(stmt)
        return data

    async def change_achievements_status(
        self,
        profile_id: int,
        achievements_to_update_status: list[str],
    ):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(
                self.model.profile_id == profile_id,
            )
            achievements_data = await session.scalar(stmt)

            for achievement in achievements_to_update_status:
                setattr(achievements_data, achievement, True)
            await session.commit()
