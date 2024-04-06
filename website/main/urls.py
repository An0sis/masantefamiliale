from django.urls import path, include
from django.contrib import admin

from . import views
from accounts.views import LoginView

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.profile_page_admin, name="login")
]