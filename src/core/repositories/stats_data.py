from sqlalchemy import select, insert

from core.db.db_helper import db_helper
from core.models import StatisticsData


class StatsDataRepo:
    model = StatisticsData

    async def get_stats_id(self, user_reference: str) -> int:
        async with db_helper.session_factory() as session:
            stmt = select(self.model.id).where(
                self.model.user_reference == user_reference
            )
            stats_id = await session.scalar(stmt)
        return stats_id

    async def add_one(self, model, data):
        async with db_helper.session_factory() as session:
            stmt = insert(model).values(**data)
            await session.execute(stmt)
            await session.commit()
