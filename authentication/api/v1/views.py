from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, VerifyEmailSerializer, RegisterSerializer
from authentication.services.verify_email import EmailVerificationService
from authentication.services.register import RegisterService


class RegisterAPIView(APIView):
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        data.pop("password1")

        RegisterService.execute(**data)

        return Response(
            {"message": "Account created successfully."}, status=status.HTTP_201_CREATED
        )


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


class LoginAPIView(APIView):
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=200)
