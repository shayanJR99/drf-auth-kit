from django.contrib.auth import get_user_model
from rest_framework import serializers
from .profile import ProfileSerializer

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User

        fields = [
            "email",
            "is_verified",
            "profile",
        ]
