from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from authentication.services.verify_email import EmailVerificationService
from emails.api.v1.serializers import MessageSerializer

@extend_schema(
    auth=[]
)
class VerifyEmailAPIView(GenericAPIView):


    def get(self, request, token):

        EmailVerificationService.verify(token)

        return Response(
            {
                "message": "Email verified successfully."
            },
            status=status.HTTP_200_OK
        )