from django.urls import path
from .views import register_user, login_user, user_me
from . import gui_views

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("me/", user_me, name="me"),
    path('gui/accounts/', gui_views.account_list, name='gui_account_list'),
]

