from core.services.profile import ProfileService
from core.repositories.profile import ProfileRepo


def get_profile_service():
    return ProfileService(ProfileRepo)
