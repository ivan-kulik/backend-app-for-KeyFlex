from core.repositories.stats import stats_repos, StatsRepository
from core.schemas.stats import AddStatisticsData


class StatsService:
    def __init__(self, repo: StatsRepository):
        self.repo = repo()

    async def add_stats(self, username: str):
        # await self.repo.add_one(data)
        await self.repo.add_one(username)


class StatsDataService:
    async def add_stats_data(self, stats_data: AddStatisticsData, cur_user):
        stats_data: dict = stats_data.model_dump()
        mode_type: str = stats_data.pop("mode_type")

        stats_repo = stats_repos.get(mode_type)
        stats_id = await stats_repo().add_stats(stats_data, cur_user)
        return stats_id
