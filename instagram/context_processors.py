
from django.contrib.auth.models import User
from .models import Profile

def profile(request):
    try:
        user = User.objects.get(pk=request.user.pk)
    except User.DoesNotExist:
        user = None

    if user:
        profile = Profile.objects.get(user=user)
        return {'current_profile': profile}
    else:
        # load a default user for testing
        profile = Profile.objects.all()[0]
        return {'profile': profile}