from core.models import User
from core.repositories import ModesStatsRepository, stats_repos
from core.schemas.stats import (
    AddStatisticsData,
    GetModesStatsData,
    GetLastSessionsStatsData,
)


class ModesStatsService:
    def __init__(self, modes_stats_repo: ModesStatsRepository):
        self.modes_stats_repo = modes_stats_repo()

    async def create_stats_data_row(self, username: str):
        data = {
            "user_reference": username,
        }
        return await self.modes_stats_repo.add_one(data)

    async def add_stats_data(self, stats_data: AddStatisticsData, cur_user):
        stats_data: dict = stats_data.model_dump()
        mode_type: str = stats_data.pop("mode_type")

        stats_id = await self.modes_stats_repo.get_stats_id(
            user_reference=cur_user.username
        )
        stats_repo = stats_repos.get(mode_type)

        await stats_repo(stats_id).add_stats(stats_data)

    async def collect_modes_stats_data(self, user_reference: str):
        stats_id = await self.modes_stats_repo.get_stats_id(
            user_reference=user_reference
        )

        symbols_per_minute_stats: dict[str, list[int]] = {}
        average_accuracy_stats: dict[str, float] = {}
        number_training_sessions_stats: dict[str, int] = {}

        for repo_title, repo in stats_repos.items():
            stats_repo = repo(stats_id)

            symbols = await stats_repo.get_symbols_per_minute_stats()
            average_accuracy = await stats_repo.calculate_average_accuracy()

            symbols_per_minute_stats[repo_title] = symbols
            average_accuracy_stats[repo_title] = average_accuracy
            number_training_sessions_stats[repo_title] = len(symbols)

        return (
            symbols_per_minute_stats,
            average_accuracy_stats,
            number_training_sessions_stats,
        )

    async def get_modes_stats_data(self, cur_user: User):
        (
            symbols_per_minute_stats,
            average_accuracy_stats,
            number_training_sessions_stats,
        ) = await self.collect_modes_stats_data(user_reference=cur_user.username)

        return GetModesStatsData(
            symbols_per_minute_stats=symbols_per_minute_stats,
            average_accuracy_stats=average_accuracy_stats,
            number_training_sessions_stats=number_training_sessions_stats,
        )

    async def get_last_sessions_stats_data(self, cur_user):
        stats_data = await self.modes_stats_repo.get_last_sessions_data(
            user_reference=cur_user.username
        )
        symbols_per_minute: list[int] = [row[0] for row in stats_data]
        accuracy: list[float] = [row[1] for row in stats_data]

        symbols_per_minute_stats = {
            "the_best_result": max(symbols_per_minute),
            "the_worst_result": min(symbols_per_minute),
            "average_result": f"{sum(symbols_per_minute) / len(symbols_per_minute):.2f}",
        }
        accuracy_stats = {
            "the_best_result": max(accuracy),
            "the_worst_result": min(accuracy),
            "average_result": f"{sum(accuracy) / len(accuracy):.2f}",
        }
        the_most_popular_mode: str = max(
            stats_data,
            key=lambda i: stats_data.count(i[3]),
        )[3]
        mode_with_the_highest_symbols_per_minute_result: str = max(
            stats_data,
            key=lambda i: i[0],
        )[3]
        mode_with_the_highest_accuracy_result: str = max(
            stats_data,
            key=lambda i: i[1],
        )[3]

        return GetLastSessionsStatsData(
            symbols_per_minute_stats=symbols_per_minute_stats,
            accuracy_stats=accuracy_stats,
            the_most_popular_mode=the_most_popular_mode,
            mode_with_the_highest_symbols_per_minute_result=mode_with_the_highest_symbols_per_minute_result,
            mode_with_the_highest_accuracy_result=mode_with_the_highest_accuracy_result,
        )
