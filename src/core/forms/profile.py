from typing import Optional
from fastapi.param_functions import Form
from fastapi import UploadFile, File


class ProfileUpdateForm:
    def __init__(
        self,
        profile_photo: Optional[UploadFile] = File(None),
        touch_typing: Optional[bool] = Form(None),
        keyboard_type: str = Form(""),
        profession: str = Form(""),
        location: str = Form(""),
        about_user: str = Form(""),
    ):
        self.profile_photo = profile_photo
        self.touch_typing = touch_typing
        self.keyboard_type = keyboard_type
        self.profession = profession
        self.location = location
        self.about_user = about_user
