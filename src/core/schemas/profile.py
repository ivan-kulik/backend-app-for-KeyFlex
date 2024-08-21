from pydantic import BaseModel

from typing import Optional


class ProfileUpdate(BaseModel):
    touch_typing: Optional[bool] = None
    keyboard_type: Optional[str] = None
    profession: Optional[str] = None
    location: Optional[str] = None
    about_user: Optional[str] = None
