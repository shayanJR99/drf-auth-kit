from django.urls import path

from .views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView
from accounts.api.v1.views import MyProfileAPIView
from .views import ResendVerificationAPIView
from .views import (
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path(
        "verify-email/<uuid:token>/", VerifyEmailAPIView.as_view(), name="verify-email"
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", MyProfileAPIView.as_view(), name="me"),
    path(
        "resend-verification/",
        ResendVerificationAPIView.as_view(),
        name="resend-verification",
    ),
    path(
        "password-reset/", PasswordResetRequestAPIView.as_view(), name="password-reset"
    ),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
