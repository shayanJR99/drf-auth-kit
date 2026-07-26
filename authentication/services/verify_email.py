from django.utils import timezone

from authentication.models import EmailVerificationToken


class EmailVerificationService:
    @staticmethod
    def create_token(user):

        token = EmailVerificationToken.objects.create(
            user=user, expires_at=timezone.now() + timezone.timedelta(hours=24)
        )

        return token

    @staticmethod
    def verify(token):

        try:
            verification = EmailVerificationToken.objects.select_related("user").get(
                token=token
            )

        except EmailVerificationToken.DoesNotExist:
            from rest_framework.exceptions import ValidationError

            raise ValidationError("Invalid token")

        if verification.expires_at < timezone.now():
            from rest_framework.exceptions import ValidationError

            raise ValidationError("Token expired")

        user = verification.user

        user.is_verified = True

        user.save(update_fields=["is_verified"])

        verification.delete()

        return user
