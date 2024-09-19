from pydantic import BaseModel

from typing import Optional
from datetime import date

from .achievements import Achievements


class GetProfileData(BaseModel):
    name: str
    touch_typing: bool
    keyboard_type: Optional[str]
    profession: Optional[str]
    location: Optional[str]
    register_date: date
    about_user: Optional[str]
    achievements: Achievements
