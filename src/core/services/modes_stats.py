from core.models import StatsModelsEnum
from core.repositories import (
    StatsDataRepo,
    ModesStatsRepo,
)
from core.schemas.stats import (
    SymbolsPerMinuteStats,
    AverageAccuracyStats,
    NumberTrainingSessionsStats,
    GetModesStatsData,
)
from core.schemas.user import UserRead


class ModesStatsService:
    def __init__(self, repo: ModesStatsRepo):
        self.repo: ModesStatsRepo = repo()

    async def get_symbols_per_minute_stats(
        self,
        user_reference: str,
    ) -> SymbolsPerMinuteStats:
        stats_id = await StatsDataRepo().get_stats_id(
            user_reference=user_reference,
        )
        symbols_per_minute_stats: dict[str, list[int]] = {}

        for model in StatsModelsEnum:
            symbols_per_minute_stats[model.name] = (
                await self.repo.get_symbols_per_minute_data(
                    model=model.value,
                    stats_id=stats_id,
                )
            )
        return symbols_per_minute_stats

    async def get_average_accuracy_stats(
        self,
        user_reference,
    ) -> AverageAccuracyStats:
        stats_id = await StatsDataRepo().get_stats_id(
            user_reference=user_reference,
        )
        average_accuracy_stats: dict[str, float] = {}

        for model in StatsModelsEnum:
            accuracy_stats = await self.repo.get_accuracy_data(
                model=model.value,
                stats_id=stats_id,
            )
            if len(accuracy_stats):
                average_accuracy = sum(accuracy_stats) / len(accuracy_stats)
                average_accuracy_stats[model.name] = float(f"{average_accuracy:.2f}")

        return average_accuracy_stats

    async def get_number_training_sessions_stats(
        self,
        symbols_per_minute_stats,
    ) -> NumberTrainingSessionsStats:
        number_training_sessions_stats: dict[str, int] = {}

        for repo_title, stats_data in symbols_per_minute_stats.items():
            number_training_sessions_stats[repo_title] = len(stats_data)
        return number_training_sessions_stats

    async def get_modes_stats_data(self, cur_user: UserRead) -> GetModesStatsData:
        symbols_per_minute_stats = await self.get_symbols_per_minute_stats(
            user_reference=cur_user.username,
        )
        average_accuracy_stats = await self.get_average_accuracy_stats(
            user_reference=cur_user.username,
        )
        number_training_sessions_stats = await self.get_number_training_sessions_stats(
            symbols_per_minute_stats=symbols_per_minute_stats,
        )

        return GetModesStatsData(
            symbols_per_minute_stats=symbols_per_minute_stats,
            average_accuracy_stats=average_accuracy_stats,
            number_training_sessions_stats=number_training_sessions_stats,
        )
