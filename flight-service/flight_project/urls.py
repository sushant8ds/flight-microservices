from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    return JsonResponse({
        "service": "Flight Service",
        "status": "✓ Running",
        "endpoints": {
            "api": "/api/",
            "metrics": "/metrics/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path("", include("django_prometheus.urls")),  # /metrics
    path("admin/", admin.site.urls),
    path("api/", include("flights.urls")),
    path("", include("flight_frontend.urls")),
    path("info/", api_info),
]
