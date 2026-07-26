from django.contrib.auth import get_user_model
from rest_framework import serializers
from .user import UserSerializer
from accounts.models import Profile
User = get_user_model()


class MyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "phone_number",
            "user",
        ]
        read_only_fields = ["id", "user"]