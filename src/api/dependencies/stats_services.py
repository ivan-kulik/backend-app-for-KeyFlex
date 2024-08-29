from core.repositories import (
    StatsDataRepo,
    ModesStatsRepo,
    LastSessionsStatsRepo,
)
from core.services import (
    StatsDataService,
    ModesStatsService,
    LastSessionsStatsService,
)


def get_stats_data_service() -> StatsDataService:
    return StatsDataService(StatsDataRepo)


def get_modes_stats_service() -> ModesStatsService:
    return ModesStatsService(ModesStatsRepo)


def get_last_sessions_stats_service() -> LastSessionsStatsService:
    return LastSessionsStatsService(LastSessionsStatsRepo)
