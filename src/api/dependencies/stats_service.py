from core.services.stats import StatsService, StatsDataService
from core.repositories.stats import StatsRepository


def get_stats_service():
    return StatsService(StatsRepository)


def get_stats_data_service():
    return StatsDataService()
