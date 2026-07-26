from django.utils import timezone
from authentication.models import EmailVerificationToken
from emails.services import EmailService


class EmailVerificationService:
    @staticmethod
    def create_token(user):
        token = EmailVerificationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timezone.timedelta(hours=24)
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

        # ارسال ایمیل خوش‌آمدگویی
        EmailService.send_welcome_email(user)
    
        verification.delete()
        return user
    
    @staticmethod
    def resend(email: str):
        from django.contrib.auth import get_user_model
        from rest_framework.exceptions import ValidationError
        from emails.services import EmailService

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # برای امنیت، پیام یکسان می‌دیم (نمی‌گیم کاربر وجود نداره)
            raise ValidationError("If an account with this email exists, a verification email has been sent.")

        if user.is_verified:
            raise ValidationError("This email is already verified.")

        # توکن‌های قبلی رو پاک کن (اختیاری ولی بهتره)
        EmailVerificationToken.objects.filter(user=user).delete()

        # ساخت توکن جدید
        token = EmailVerificationService.create_token(user)

        # ارسال ایمیل
        EmailService.send_verification_email(user, token.token)

        return user
