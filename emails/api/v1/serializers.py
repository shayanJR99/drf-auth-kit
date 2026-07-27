from rest_framework import serializers

from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()