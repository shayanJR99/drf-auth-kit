from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        verification_url = f"{settings.BACKEND_URL}/api/v1/auth/verify-email/{token}/"
        send_mail(
            subject="Verify your email",
            message=f"Please verify your account by clicking the link below:\n\n{verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    @staticmethod
    def send_welcome_email(user):
        send_mail(
            subject="Welcome!",
            message=f"Hi,\n\nYour email has been successfully verified.\nWelcome to the app!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )