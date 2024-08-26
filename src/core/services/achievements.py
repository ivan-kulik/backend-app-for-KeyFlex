from core.repositories.achievements import AchievementsRepository


class AchievementsService:
    def __init__(self, achievements_repo: AchievementsRepository):
        self.achievements_repo: AchievementsRepository = achievements_repo()

    async def create_achievements_row(self, profile_id):
        data = {
            "profile_id": profile_id,
        }
        return await self.achievements_repo.add_one(data)

    async def change_achievement_status(self, stats_data):
        pass

    async def get_achievements(self, profile_id: int):
        data = await self.achievements_repo.get_achievements(profile_id=profile_id)

        achievements = {
            title: val for title, val in data.__dict__.items() if type(val) is bool
        }
        return achievements
