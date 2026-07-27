from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:

    @classmethod
    def _send_templated_email(
        cls, subject: str, template_name: str, context: dict, recipient_list: list[str]
    ):
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list,
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

    @classmethod
    def send_verification_email(cls, user, token):
        verification_url = f"{settings.BACKEND_URL}/api/v1/auth/verify-email/{token}/"
        context = {
            "user": user,
            "verification_url": verification_url,
        }
        cls._send_templated_email(
            subject="Verify your email",
            template_name="emails/verification.html",
            context=context,
            recipient_list=[user.email],
        )

    @classmethod
    def send_welcome_email(cls, user):
        context = {"user": user}
        cls._send_templated_email(
            subject="Welcome!",
            template_name="emails/welcome.html",
            context=context,
            recipient_list=[user.email],
        )

    @classmethod
    def send_password_reset_email(cls, user, token):
        # reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}/"
        reset_url = f"{settings.BACKEND_URL}/reset-password/{token}/"
        context = {
            "user": user,
            "reset_url": reset_url,
        }
        cls._send_templated_email(
            subject="Password Reset Request",
            template_name="emails/password_reset.html",
            context=context,
            recipient_list=[user.email],
        )