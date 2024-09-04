from fastapi import APIRouter, Depends
from typing import Annotated

from core.config import settings
from core.models import User

# from .routers_helper import routers_helper
from core.services import UserService
from core.schemas.user import UserUpdate
from api.dependencies import current_active_user, get_user_service

router = APIRouter(
    prefix=settings.api.users,
    tags=["Users"],
)

# # /me and /{id}
# router.include_router(
#     router=routers_helper.get_users_router(
#         UserRead,
#         UserUpdate,
#     ),
# )


# api/users/me - PATCH
# api/users/me - DELETE


@router.patch("/me")
async def update_user_data(
    cur_user: Annotated[User, Depends(current_active_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_update: UserUpdate,
) -> None:
    await user_service.update_user_data(
        cur_user=cur_user,
        user_update_data=user_update,
    )


@router.delete("/me")
async def delete_account(
    cur_user: Annotated[User, Depends(current_active_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    await user_service.delete_account(cur_user=cur_user)
