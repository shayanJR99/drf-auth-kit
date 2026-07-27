from django.contrib.auth import get_user_model

from accounts.models import Profile

from authentication.services.verify_email import EmailVerificationService

from emails.services import EmailService


User = get_user_model()


class RegisterService:
    @staticmethod
    def execute(*, email, password, first_name="", last_name=""):

        user = User.objects.create_user(
            email=email,
            password=password,
        )

        user.profile.first_name = first_name
        user.profile.last_name = last_name

        user.profile.save(
            update_fields=[
                "first_name",
                "last_name",
            ]
        )

        token = EmailVerificationService.create_token(user)

        EmailService.send_verification_email(user, token.token)

        return user
