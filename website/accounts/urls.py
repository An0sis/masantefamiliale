from django.urls import path, include

from .views import SignUpView
from .views import SignUpView, profile_page_admin

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls")),
    path("login/", profile_page_admin, name="login"),
    path("logout/", profile_page_admin, name="logout"),
]
