from sqlalchemy import select, insert

from .base_repository import SQLAlchemyRepository
from core.models import (
    StandardModeStats,
    ExtendedModeStats,
    TextModeStats,
    EnglishModeStats,
    ExtremeModeStats,
    UserModeStats,
    User,
    StatisticsData,
)
from ..db.db_helper import db_helper


class StatsRepository(SQLAlchemyRepository):
    model = StatisticsData

    async def add_one(self, username):
        async with db_helper.session_factory() as session:
            stmt = (
                insert(self.model).values(user_reference=username).returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


class StatsDataRepository(SQLAlchemyRepository):
    async def add_stats(self, stats_data: dict, cur_user: User):
        async with db_helper.session_factory() as session:
            stmt = select(StatisticsData).where(
                StatisticsData.user_reference == cur_user.username
            )
            res = await session.execute(stmt)
            stats_data["stats_id"] = res.scalar().id
            await self.add_one(stats_data)


class StandardModeStatsRepository(StatsDataRepository):
    model = StandardModeStats


class ExtendedModeStatsRepository(StatsDataRepository):
    model = ExtendedModeStats


class TextModeStatsRepository(StatsDataRepository):
    model = TextModeStats


class EnglishModeStatsRepository(StatsDataRepository):
    model = EnglishModeStats


class ExtremeModeStatsRepository(StatsDataRepository):
    model = ExtremeModeStats


class UserModeStatsRepository(StatsDataRepository):
    model = UserModeStats


stats_repos = {
    "standard": StandardModeStatsRepository,
    "extended": ExtendedModeStatsRepository,
    "text": TextModeStatsRepository,
    "english": EnglishModeStatsRepository,
    "extreme": ExtremeModeStatsRepository,
    "user": UserModeStatsRepository,
}
