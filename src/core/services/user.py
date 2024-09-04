from core.repositories import UserRepo
from core.models import User
from core.schemas.user import UserUpdate


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo: UserRepo = repo()

    async def update_user_data(
        self,
        cur_user: User,
        user_update_data: UserUpdate,
    ) -> None:
        await self.repo.update_user_data(
            username=cur_user.username,
            user_update_data=user_update_data,
        )

    async def delete_account(self, cur_user: User) -> None:
        await self.repo.delete_account(username=cur_user.username)
