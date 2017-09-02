from groups.models import Group
from core.models import User, UserProfile


def allowed_groups(user: User):
    """Return the types of groups a user is allowed to request."""

    if user.is_superuser or user.is_staff:
        return [Group.CLUB, Group.ACADEMIC, Group.EXTERNAL, Group.ADMINISTRATIVE]
    elif user.profile.type in (UserProfile.TEACHER, UserProfile.STAFF):
        return [Group.CLUB, Group.ACADEMIC, Group.EXTERNAL]
    elif user.profile.type in (UserProfile.STUDENT,):
        return [Group.CLUB]
    return []
