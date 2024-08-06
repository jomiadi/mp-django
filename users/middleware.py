# users/middleware.py
from django.shortcuts import redirect

class CheckVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated and not request.user.is_verified:
            return redirect('verification_required')
        response = self.get_response(request)
        return response
