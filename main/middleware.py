import os
from django.http import HttpResponseForbidden

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_admin = os.getenv("ALLOW_ADMIN_ACCESS", "false").lower() == "true"

    def __call__(self, request):
        if request.path.startswith("/admin/") and not self.allow_admin:
            return HttpResponseForbidden("Admin access is disabled in this environment.")
        return self.get_response(request)
