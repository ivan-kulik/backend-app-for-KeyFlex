from core.repositories import ModesStatsRepository, stats_repos
from core.schemas.stats import AddStatisticsData

from core.models import User


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

    async def collect_all_stats(self, user_reference: str):
        stats_id = await self.modes_stats_repo.get_stats_id(
            user_reference=user_reference
        )

        symbols_per_minute_stats = []
        average_accuracy_stats = []
        classes_number = []

        for repo in stats_repos.values():
            stats_repo = repo(stats_id)

            symbols = await stats_repo.get_symbols_per_minute_stats()
            average_accuracy = await stats_repo.calculate_average_accuracy()

            symbols_per_minute_stats.append(symbols)
            average_accuracy_stats.append(average_accuracy)
            classes_number.append(len(symbols))

        return symbols_per_minute_stats, average_accuracy_stats, classes_number

    async def get_all_stats(self, cur_user: User):
        symbols_per_minute_stats, average_accuracy_stats, classes_number = (
            await self.collect_all_stats(user_reference=cur_user.username)
        )
        return {
            "mainStats": {
                "standard_mode": symbols_per_minute_stats[0],
                "extended_mode": symbols_per_minute_stats[1],
                "text_mode": symbols_per_minute_stats[2],
                "english_mode": symbols_per_minute_stats[3],
                "extreme_mode": symbols_per_minute_stats[4],
                "user_mode": symbols_per_minute_stats[5],
            },
            "average_accuracy": {
                "standard_mode": average_accuracy_stats[0],
                "extended_mode": average_accuracy_stats[1],
                "text_mode": average_accuracy_stats[2],
                "english_mode": average_accuracy_stats[3],
                "extreme_mode": average_accuracy_stats[4],
                "user_mode": average_accuracy_stats[5],
            },
            "classes": {
                "standard_mode": classes_number[0],
                "extended_mode": classes_number[1],
                "text_mode": classes_number[2],
                "english_mode": classes_number[3],
                "extreme_mode": classes_number[4],
                "user_mode": classes_number[5],
            },
        }
