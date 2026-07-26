from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.api.v1.serializers.register import RegisterSerializer
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
