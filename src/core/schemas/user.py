from fastapi_users import schemas
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
import datetime

from core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    username: str
    registration_date: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
