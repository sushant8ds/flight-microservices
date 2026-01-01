from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django_prometheus.exports import ExportToDjangoView

def api_info(request):
    return JsonResponse({
        "service": "Booking Service",
        "status": "✓ Running",
        "metrics": "/metrics"
    })

urlpatterns = [
    # 🔥 PROMETHEUS — MUST BE FIRST
    path("metrics", ExportToDjangoView, name='prometheus-django-metrics'),

    # APIs
    path("api/", include("bookings.urls")),
    path("info/", api_info),

    # Admin
    path("admin/", admin.site.urls),

    # ❌ FRONTEND ABSOLUTELY LAST
    path("", include("booking_frontend.urls")),
]
