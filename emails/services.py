from django.core.mail import send_mail

from django.conf import settings


class EmailService:
    @staticmethod
    def send_verification_email(user, token):

        verification_url = f"{settings.BACKEND_URL}/api/v1/auth/verify-email/{token}/"

        send_mail(
            subject="Verify your email",
            message=f"Verify your account: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
