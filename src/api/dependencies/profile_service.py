from core.services.profile import ProfileService
from core.repositories.profile import ProfileRepository


def get_profile_service():
    return ProfileService(ProfileRepository)
