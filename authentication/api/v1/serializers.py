from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(write_only=True, min_length=8)

    password1 = serializers.CharField(write_only=True)

    def validate_email(self, value):

        from django.contrib.auth import get_user_model

        User = get_user_model()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already exists.")

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate(email=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
