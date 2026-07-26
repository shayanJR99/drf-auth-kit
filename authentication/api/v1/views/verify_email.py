from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.services.verify_email import EmailVerificationService


class VerifyEmailAPIView(APIView):

    def get(self, request, token):

        EmailVerificationService.verify(
            token
        )

        return Response(
            {
                "message": "Email verified successfully."
            },
            status=status.HTTP_200_OK
        )