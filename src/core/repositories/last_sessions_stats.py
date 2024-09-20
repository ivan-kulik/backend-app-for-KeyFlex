from sqlalchemy import select, literal, union_all

from core.utils.db_helper import db_helper
from core.config import settings
from core.models import StatsModelsEnum


class LastSessionsStatsRepo:
    async def get_last_sessions_data(self, stats_id: int):
        queries = []

        for model in StatsModelsEnum:
            query = (
                select(
                    model.value.symbols_per_minute,
                    model.value.accuracy_percentage,
                    model.value.added_at,
                    literal(model.name).label("source_table"),
                )
                .where(model.value.stats_id == stats_id)
                .order_by(model.value.added_at.desc())
                .limit(settings.amount_of_stats.last_sessions_stats)
            )
            queries.append(query)

        combined_query = union_all(*queries)
        subquery = combined_query.subquery()
        final_query = (
            select(subquery)
            .order_by(subquery.c.added_at.desc())
            .limit(settings.amount_of_stats.last_sessions_stats)
        )

        async with db_helper.session_factory() as session:
            res = await session.execute(final_query)

        last_sessions_stats = res.fetchall()
        return last_sessions_stats
