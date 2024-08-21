from abc import ABC, abstractmethod

from sqlalchemy import insert

from core.db.db_helper import db_helper


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict):
        async with db_helper.session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
