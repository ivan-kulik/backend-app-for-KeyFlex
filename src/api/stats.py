from fastapi import APIRouter, status, Depends

from typing import Annotated

from core.config import settings
from core.schemas.stats import AddStatisticsData
from core.services.stats import ModesStatsService
from core.models import User
from .routers_helper import routers_helper

from api.dependencies.stats_service import get_modes_stats_service


router = APIRouter(
    prefix=settings.api.stats,
    tags=["Statistics"],
)

current_active_verified_user = routers_helper.current_user(
    active=True,
    # verified=True,
)


@router.post("/add_stats", status_code=status.HTTP_201_CREATED)
async def add_statistics(
    user: Annotated[User, Depends(current_active_verified_user)],
    add_statistics_data: AddStatisticsData,
    modes_stats_service: Annotated[
        ModesStatsService,
        Depends(get_modes_stats_service),
    ],
):
    await modes_stats_service.add_stats_data(
        add_statistics_data,
        user,
    )


@router.get("/get_all_stats", status_code=status.HTTP_200_OK)
async def get_all_statistics(
    user: Annotated[User, Depends(current_active_verified_user)],
    modes_stats_service: Annotated[
        ModesStatsService,
        Depends(get_modes_stats_service),
    ],
):
    stats_data = await modes_stats_service.get_all_stats(
        cur_user=user,
    )
    return stats_data
