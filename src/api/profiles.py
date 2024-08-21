from fastapi import APIRouter, Depends, status

from typing import Annotated

from core.config import settings
from core.models import User
from core.schemas.profile import ProfileUpdate
from core.services.profile import ProfileService
from api.dependencies.profile_service import get_profile_service
from .routers_helper import routers_helper


router = APIRouter(
    prefix=settings.api.profiles,
    tags=["Profiles"],
)


current_active_verified_user = routers_helper.current_user(
    active=True,
    # verified=True,
)


@router.patch("/update", status_code=status.HTTP_202_ACCEPTED)
async def update_profile(
    user: Annotated[User, Depends(current_active_verified_user)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
    profile_update: ProfileUpdate,
):
    return await profile_service.update_profile(
        cur_user=user,
        profile_update=profile_update,
    )


@router.get("/get_info", status_code=status.HTTP_200_OK)
async def get_profile_data(
    user: Annotated[User, Depends(current_active_verified_user)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
):
    return await profile_service.get_profile_data(
        cur_user=user,
    )
