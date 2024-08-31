from api.routers_helper import routers_helper


current_active_verified_user = routers_helper.current_user(
    active=True,
    verified=True,
)
