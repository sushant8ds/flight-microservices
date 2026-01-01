from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='auth_frontend_index'),
    path('accounts/', views.accounts_list, name='auth_frontend_accounts'),
]
