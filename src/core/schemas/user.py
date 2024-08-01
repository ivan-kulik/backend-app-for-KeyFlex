from fastapi_users import schemas
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
import datetime


class UserRead(schemas.BaseUser[int]):
    username: str
    registration_date: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    registration_date: datetime.datetime = datetime.datetime.utcnow()


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
