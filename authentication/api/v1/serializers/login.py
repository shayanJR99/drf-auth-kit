from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate(email=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_verified:
            raise serializers.ValidationError("Email is not verified.")

        attrs["user"] = user

        return attrs


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()