# users/decorators.py
from django.shortcuts import redirect
from functools import wraps

def user_verified(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправление на страницу входа
        if not request.user.is_verified:
            return redirect('verification_required')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
