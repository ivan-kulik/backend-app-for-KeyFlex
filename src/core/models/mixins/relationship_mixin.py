from typing import Generic, ClassVar, TypeVar
from sqlalchemy.orm import declared_attr, relationship, Mapped


RelationClassName = TypeVar("RelationClassName")


class RelationshipMixin(Generic[RelationClassName]):
    __relation_name__: ClassVar[str]

    @declared_attr
    def statistics_data(cls) -> Mapped[RelationClassName]:
        return relationship(
            back_populates=cls.__relation_name__,
        )
