from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.db.db_helper import db_helper
from core.models import User
from core.schemas.user import UserUpdate


class UserRepo:
    model = User

    async def update_user_data(
        self,
        username: str,
        user_update_data: UserUpdate,
    ) -> None:
        async with db_helper.session_factory() as session:
            # FIXME: update or delete on table "users" violates foreign key constraint "fk_profiles_user_reference_users" on table "profiles"
            stmt = (
                select(self.model)
                .options(
                    joinedload(self.model.profile),
                )
                .where(self.model.username == username)
            )
            user_data = await session.scalar(stmt)

            user_data.profile.user_reference = user_update_data.username
            user_data.username = user_update_data.username

            await session.commit()

    async def delete_account(self, username: str) -> None:
        async with db_helper.session_factory() as session:
            stmt = select(self.model).where(self.model.username == username)
            await session.delete(stmt)
            await session.commit()
