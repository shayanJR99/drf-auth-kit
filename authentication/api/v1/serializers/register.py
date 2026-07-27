from rest_framework import serializers

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
