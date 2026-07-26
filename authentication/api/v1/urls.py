from django.urls import path
from .views import RegisterAPIView, VerifyEmailAPIView, LoginAPIView
from accounts.api.v1.views import MeAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email/<uuid:token>/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", MeAPIView.as_view(), name="me"),
]
