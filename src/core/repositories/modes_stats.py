from sqlalchemy import select

from core.db.db_helper import db_helper
from core.config import settings


class ModesStatsRepo:
    async def get_symbols_per_minute_data(self, model, stats_id):
        async with db_helper.session_factory() as session:
            stmt = (
                select(model.symbols_per_minute)
                .where(model.stats_id == stats_id)
                .order_by(model.id.desc())
                .limit(settings.amount_of_stats.modes_stats)
            )
            data = await session.scalars(stmt)
        return data.all()

    async def get_accuracy_data(self, model, stats_id):
        async with db_helper.session_factory() as session:
            stmt = (
                select(model.accuracy_percentage)
                .where(model.stats_id == stats_id)
                .order_by(model.id.desc())
                .limit(settings.amount_of_stats.modes_stats)
            )
            data = await session.scalars(stmt)
        return data.all()
