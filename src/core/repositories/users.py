from sqlalchemy import select, ScalarResult
from core.models import db_helper, User


async def get_by_username(username: str) -> ScalarResult:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.username == username)
        user: ScalarResult = await session.scalar(stmt)
    return user
