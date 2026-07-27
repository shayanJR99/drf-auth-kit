from ..serializers import MyProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from drf_spectacular.utils import extend_schema


class MyProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile