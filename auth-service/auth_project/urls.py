from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    return JsonResponse({
        "service": "Auth Service",
        "status": "running"
    })

urlpatterns = [
    path("", include("django_prometheus.urls")),  # ✅ THIS ENABLES /metrics
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("", api_info),
]
