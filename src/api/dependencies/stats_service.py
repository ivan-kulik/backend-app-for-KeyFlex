from core.services.stats import ModesStatsService
from core.repositories.stats import ModesStatsRepository


def get_modes_stats_service():
    return ModesStatsService(ModesStatsRepository)
