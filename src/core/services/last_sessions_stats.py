from core.repositories import (
    StatsDataRepo,
    LastSessionsStatsRepo,
)
from core.schemas.stats import (
    LastSessionsSymbolsPerMinuteStats,
    LastSessionsAccuracyStats,
    GetLastSessionsStatsData,
)
from core.schemas.user import UserRead


class LastSessionsStatsService:
    def __init__(self, repo: LastSessionsStatsRepo):
        self.repo: LastSessionsStatsRepo = repo()

    async def get_symbols_per_minute_values(self, stats_data):
        symbols_per_minute_values: list[int] = [row[0] for row in stats_data]
        return symbols_per_minute_values

    async def get_symbols_per_minute_stats(
        self,
        symbols_per_minute_values,
    ) -> LastSessionsSymbolsPerMinuteStats:
        return {
            "the_best_result": max(symbols_per_minute_values),
            "the_worst_result": min(symbols_per_minute_values),
            "average_result": float(
                f"{sum(symbols_per_minute_values) / len(symbols_per_minute_values):.2f}",
            ),
        }

    async def get_accuracy_stats(
        self,
        stats_data,
    ) -> LastSessionsAccuracyStats:
        accuracy: list[float] = [row[1] for row in stats_data]

        return {
            "the_best_result": max(accuracy),
            "the_worst_result": min(accuracy),
            "average_result": float(
                f"{sum(accuracy) / len(accuracy):.2f}",
            ),
        }

    async def get_modes_types(self, stats_data):
        modes_types = [row[3] for row in stats_data]
        return modes_types

    async def get_most_popular_mode(self, modes_types) -> str:
        the_most_popular_mode = max(modes_types, key=modes_types.count)
        return the_most_popular_mode

    async def get_spm_best_mode(self, stats_data) -> str:
        spm_best_mode: str = max(stats_data, key=lambda i: i[0])[3]
        return spm_best_mode

    async def get_accuracy_best_mode(self, stats_data) -> str:
        accuracy_best_mode: str = max(
            stats_data,
            key=lambda i: i[1],
        )[3]
        return accuracy_best_mode

    async def get_last_sessions_stats_data(self, cur_user: UserRead):
        stats_id = await StatsDataRepo().get_stats_id(
            user_reference=cur_user.username,
        )
        stats_data = await self.repo.get_last_sessions_data(
            stats_id=stats_id,
        )

        symbols_per_minute_values = await self.get_symbols_per_minute_values(
            stats_data=stats_data,
        )
        symbols_per_minute_stats = await self.get_symbols_per_minute_stats(
            symbols_per_minute_values=symbols_per_minute_values,
        )

        accuracy_stats = await self.get_accuracy_stats(
            stats_data=stats_data,
        )

        modes_types = await self.get_modes_types(stats_data=stats_data)
        the_most_popular_mode = await self.get_most_popular_mode(
            modes_types=modes_types,
        )

        spm_best_mode = await self.get_spm_best_mode(
            stats_data=stats_data,
        )
        accuracy_best_mode = await self.get_accuracy_best_mode(
            stats_data=stats_data,
        )

        return GetLastSessionsStatsData(
            symbols_per_minute_values=symbols_per_minute_values,
            modes_types=modes_types,
            symbols_per_minute_stats=symbols_per_minute_stats,
            accuracy_stats=accuracy_stats,
            the_most_popular_mode=the_most_popular_mode,
            smp_best_mode=spm_best_mode,
            accuracy_best_mode=accuracy_best_mode,
        )
