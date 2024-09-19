from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import date

from .achievements import Achievements


class GetProfileData(BaseModel):
    name: str
    profile_photo_url: Optional[HttpUrl]
    touch_typing: bool
    keyboard_type: Optional[str]
    profession: Optional[str]
    location: Optional[str]
    register_date: date
    about_user: Optional[str]
    achievements: Achievements
