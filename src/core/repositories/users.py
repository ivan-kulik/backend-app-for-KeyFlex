from sqlalchemy import select

from core.models import db_helper, User


async def get_by_username(username: str):
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.username == username)
        user = await session.scalar(stmt)
    return user
