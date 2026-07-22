from functools import wraps
from django.shortcuts import redirect
from .models import Profile


def admin_or_teacher(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        try:
            profile = Profile.objects.get(user=request.user)

            if profile.role in ["Admin", "Teacher"]:
                return view_func(request, *args, **kwargs)

        except Profile.DoesNotExist:
            pass

        return redirect("dashboard")

    return wrapper