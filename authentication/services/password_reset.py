from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from authentication.models import PasswordResetToken
from emails.services import EmailService

User = get_user_model()


class PasswordResetService:

    @staticmethod
    def request_reset(email: str):
        try:
            user = User.objects.get(email=email)
            print(">>> User found:", user.email)          # ← این خط
        except User.DoesNotExist:
            print(">>> User NOT found")                   # ← این خط
            return

        PasswordResetToken.objects.filter(user=user).delete()

        token = PasswordResetToken.objects.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )
        print(">>> Token created:", token.token)          # ← این خط

        EmailService.send_password_reset_email(user, token.token)
        print(">>> Email send function called")       
        # ← این خط
    @staticmethod
    def reset_password(token: str, new_password: str):
        try:
            reset_token = PasswordResetToken.objects.select_related("user").get(token=token)
        except PasswordResetToken.DoesNotExist:
            raise ValidationError("Invalid or expired token.")

        if reset_token.expires_at < timezone.now():
            reset_token.delete()
            raise ValidationError("Invalid or expired token.")

        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # توکن رو مصرف‌شده حذف کن
        reset_token.delete()

        return user