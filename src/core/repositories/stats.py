from sqlalchemy import select, union_all, literal

from core.db.db_helper import db_helper
from core.models import (
    StandardModeStats,
    ExtendedModeStats,
    TextModeStats,
    EnglishModeStats,
    ExtremeModeStats,
    UserModeStats,
    StatisticsData,
)
from core.models import stats_models
from core.schemas.stats import AddStatisticsData
from .base_repository import SQLAlchemyRepository


class ModesStatsRepository(SQLAlchemyRepository):
    model = StatisticsData

    async def get_stats_id(self, user_reference: str) -> int:
        async with db_helper.session_factory() as session:
            stmt = select(self.model.id).where(
                self.model.user_reference == user_reference
            )
            stats_id = await session.scalar(stmt)
        return stats_id

    async def get_last_sessions_data(self, user_reference: str):
        queries = []
        stats_id = await self.get_stats_id(user_reference)
        for model_name, model in stats_models.items():
            query = (
                select(
                    model.symbols_per_minute,
                    model.accuracy_percentage,
                    model.added_at,
                    literal(model_name).label("source_table"),
                )
                .where(model.stats_id == stats_id)
                .order_by(model.added_at.desc())
                .limit(10)
            )
            queries.append(query)

        combined_query = union_all(*queries)
        subquery = combined_query.subquery()
        final_query = select(subquery).order_by(subquery.c.added_at.desc()).limit(10)

        async with db_helper.session_factory() as session:
            res = await session.execute(final_query)

        last_attempts_stats = res.fetchall()
        return last_attempts_stats


class BaseStatsRepository(SQLAlchemyRepository):
    def __init__(self, stats_id: int):
        self.stats_id = stats_id

    async def add_stats(self, stats_data: AddStatisticsData):
        stats_data["stats_id"] = self.stats_id
        return await self.add_one(stats_data)

    async def get_symbols_per_minute_stats(self, amount: int = 75):
        async with db_helper.session_factory() as session:
            stmt = (
                select(self.model.symbols_per_minute)
                .where(self.model.stats_id == self.stats_id)
                .order_by(self.model.id.desc())
                .limit(amount)
            )
            data = await session.scalars(stmt)
        return data.all()

    async def get_accuracy_stats(self, amount: int = 75):
        async with db_helper.session_factory() as session:
            stmt = (
                select(self.model.accuracy_percentage)
                .where(self.model.stats_id == self.stats_id)
                .order_by(self.model.id.desc())
                .limit(amount)
            )
            data = await session.scalars(stmt)
        return data.all()

    async def calculate_average_accuracy(self):
        data = await self.get_accuracy_stats()
        if len(data):
            average_accuracy = sum(data) / len(data)
            return float(f"{average_accuracy:.2f}")


class StandardModeStatsRepository(BaseStatsRepository):
    model = StandardModeStats


class ExtendedModeStatsRepository(BaseStatsRepository):
    model = ExtendedModeStats


class TextModeStatsRepository(BaseStatsRepository):
    model = TextModeStats


class EnglishModeStatsRepository(BaseStatsRepository):
    model = EnglishModeStats


class ExtremeModeStatsRepository(BaseStatsRepository):
    model = ExtremeModeStats


class UserModeStatsRepository(BaseStatsRepository):
    model = UserModeStats
