from sqlalchemy import select

from core.db.db_helper import db_helper
from .base_repository import SQLAlchemyRepository
from core.models import Achievements


class AchievementsRepository(SQLAlchemyRepository):
    model = Achievements

    async def get_achievements(self, profile_id):
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(self.model.profile_id == profile_id)
            data = await session.scalar(stmt)
        return data

    async def change_achievements_status(self):
        pass
