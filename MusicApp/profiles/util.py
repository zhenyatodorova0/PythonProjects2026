#помощна функция

from profiles.models import Profile

def get_profile() -> Profile | None:
    return Profile.objects.first() #this ensures there will be only 1 profile
