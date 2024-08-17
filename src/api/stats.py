from fastapi import APIRouter, status, Depends

from typing import Annotated

from core.config import settings
from core.schemas.stats import AddStatisticsData
from core.services.stats import StatsDataService
from core.models import User
from .routers_helper import routers_helper

from api.dependencies.stats_service import get_stats_data_service


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
    add_statistics_data: AddStatisticsData,
    user: Annotated[User, Depends(current_active_verified_user)],
    stats_data_service: Annotated[StatsDataService, Depends(get_stats_data_service)],
):
    stats_id = await stats_data_service.add_stats_data(
        add_statistics_data,
        user,
    )
    return stats_id
