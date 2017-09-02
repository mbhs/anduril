from groups.models import Group, ClubGroup, AcademicGroup, ExternalGroup, AdministrativeGroup
from core.models import User, UserProfile


def allowed_groups(user: User):
    """Return the types of groups a user is allowed to request."""

    if user.is_superuser or user.is_staff:
        return [ClubGroup, AcademicGroup, ExternalGroup, AdministrativeGroup]
    elif user.profile.type in (UserProfile.TEACHER, UserProfile.STAFF):
        return [ClubGroup, AcademicGroup, ExternalGroup]
    elif user.profile.type in (UserProfile.STUDENT,):
        return [ClubGroup]
    return []
