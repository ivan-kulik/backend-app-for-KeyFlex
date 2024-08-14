from typing import ClassVar, TYPE_CHECKING
from sqlalchemy.orm import declared_attr, relationship, Mapped

if TYPE_CHECKING:
    from core.models.statistics_data import StatisticsData


class RelationshipMixin:
    __relation_name__: ClassVar[str]

    @declared_attr
    def statistics_data(cls) -> Mapped["StatisticsData"]:
        return relationship(
            back_populates=cls.__relation_name__,
        )
