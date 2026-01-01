from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='flight_frontend_index'),
    path('search/', views.search, name='flight_frontend_search'),
]
