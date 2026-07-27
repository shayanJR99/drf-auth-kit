from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authentication.api.v1.serializers.password_reset import (
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from authentication.services.password_reset import PasswordResetService
from emails.api.v1.serializers import MessageSerializer


from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
@method_decorator(ratelimit(key='ip', rate='3/m', method='POST', block=True), name='dispatch')
@extend_schema(auth=[])
class PasswordResetRequestAPIView(APIView):

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={200: MessageSerializer}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        PasswordResetService.request_reset(email=serializer.validated_data["email"])

        return Response(
            {"message": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
@extend_schema(auth=[])
class PasswordResetConfirmAPIView(APIView):

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={200: MessageSerializer}
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        PasswordResetService.reset_password(
            token=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"]
        )

        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )