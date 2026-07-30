from django.urls import path
from .views import LoginView, ProfileView, RegisterView, VerifyOTPView

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
    ),

   path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

]