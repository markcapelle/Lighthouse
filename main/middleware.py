import os
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_admin = os.getenv("ALLOW_ADMIN_ACCESS", "false").lower() == "true"

    def __call__(self, request):
        if request.path.startswith("/admin/") and not self.allow_admin:
            return HttpResponseForbidden("Admin access is disabled in this environment.")
        return self.get_response(request)


class ForcePasswordChangeMiddleware:
    """
    Blocks all pages until the user completes the forced password change.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            profile = getattr(user, "profile", None)

            if profile and profile.force_password_change:
                allowed_paths = {
                    reverse("forced_password_change"),
                    reverse("logout"),
                }

                # Prevent bypassing the forced password change
                if request.path not in allowed_paths:
                    return redirect("forced_password_change")

        return self.get_response(request)
