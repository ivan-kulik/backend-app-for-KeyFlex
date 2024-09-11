from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.db_helper import db_helper
from core.models import User


async def get_users_db(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    yield User.get_db(session=session)
