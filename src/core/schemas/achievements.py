from pydantic import BaseModel
from typing import Optional


class Achievements(BaseModel):
    forty_characters_per_minute: Optional[bool]
    fifty_characters_per_minute: Optional[bool]
    sixty_characters_per_minute: Optional[bool]
    seventy_characters_per_minute: Optional[bool]
    eighty_characters_per_minute: Optional[bool]
    ninety_characters_per_minute: Optional[bool]
    one_hundred_characters_per_minute: Optional[bool]
