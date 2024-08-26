from pydantic import BaseModel

from typing import Optional
from datetime import date

from .achievements import Achievements


class ProfileUpdate(BaseModel):
    touch_typing: Optional[bool] = None
    keyboard_type: Optional[str] = None
    profession: Optional[str] = None
    location: Optional[str] = None
    about_user: Optional[str] = None


class GetProfileData(BaseModel):
    name: str
    touch_typing: bool
    keyboard_type: str
    profession: str
    location: str
    register_date: date
    about_user: str
    achievements: Achievements
