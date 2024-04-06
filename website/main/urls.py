from django.urls import path, include
from django.contrib import admin

from . import views
from accounts.views import LoginView

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("", views.familypage, name="family")
]