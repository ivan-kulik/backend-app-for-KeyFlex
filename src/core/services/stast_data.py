from core.models import (
    StatisticsData,
    StatsModelsEnum,
)
from core.repositories import (
    StatsDataRepo,
    AchievementsRepo,
)
from .achievements import AchievementsService
from core.schemas.stats import AddStatisticsData
from core.schemas.user import UserRead


achievements_service: AchievementsService = AchievementsService(
    AchievementsRepo,
)


class StatsDataService:
    def __init__(self, repo: StatsDataRepo):
        self.repo: StatsDataRepo = repo()

    async def create_stats_data_row(self, cur_user: UserRead) -> None:
        data = {
            "user_reference": cur_user.username,
        }
        await self.repo.add_one(model=StatisticsData, data=data)

    async def add_stats_data(
        self,
        stats_data: AddStatisticsData,
        cur_user: UserRead,
    ) -> None:
        stats_data: dict = stats_data.model_dump()

        mode_type: str = stats_data.pop("mode_type")
        stats_model = StatsModelsEnum[mode_type].value

        stats_id = await self.repo.get_stats_id(
            user_reference=cur_user.username,
        )
        stats_data["stats_id"] = stats_id
        await self.repo.add_one(model=stats_model, data=stats_data)

        await achievements_service.change_achievement_status(
            user_reference=cur_user.username,
            symbols_per_minute=stats_data["symbols_per_minute"],
        )
