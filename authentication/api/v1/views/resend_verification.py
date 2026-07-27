from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from authentication.api.v1.serializers.resend_verification import ResendVerificationSerializer
from authentication.services.verify_email import EmailVerificationService
from emails.api.v1.serializers import MessageSerializer


@extend_schema(auth=[])
class ResendVerificationAPIView(APIView):

    @extend_schema(
        request=ResendVerificationSerializer,
        responses={200: MessageSerializer}
    )
    def post(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        EmailVerificationService.resend(email=serializer.validated_data["email"])

        return Response(
            {
                "message": "If an account with this email exists, a verification email has been sent."
            },
            status=status.HTTP_200_OK
        )