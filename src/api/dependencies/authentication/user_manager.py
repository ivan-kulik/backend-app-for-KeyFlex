from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from core.authentication.user_manager import UserManager
from .users import get_users_db


async def get_user_manager(
    users_db: Annotated[
        SQLAlchemyUserDatabase,
        Depends(get_users_db),
    ]
):
    yield UserManager(users_db)
