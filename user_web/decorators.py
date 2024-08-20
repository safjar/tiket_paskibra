from functools import wraps
from django.shortcuts import redirect
from .models import Profile

def user_profile_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile  # Mengakses profil langsung dari user
            if profile.is_fully_filled():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('profile')  # Ganti dengan nama URL yang sesuai
        except Profile.DoesNotExist:
            return redirect('profile')  # Ganti dengan nama URL yang sesuai

    return _wrapped_view