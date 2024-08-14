from typing import Optional

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import UP
from sqlalchemy import func, select


class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)
