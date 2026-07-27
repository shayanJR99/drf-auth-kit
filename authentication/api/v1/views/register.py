from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from authentication.api.v1.serializers.register import RegisterSerializer
from authentication.services.register import RegisterService
from emails.api.v1.serializers import MessageSerializer


@extend_schema(
    auth=[]
)
class RegisterAPIView(CreateAPIView):

    serializer_class = RegisterSerializer
    @extend_schema(
    responses={
        201: MessageSerializer
    }
)
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        data.pop("password1")

        RegisterService.execute(**data)

        return Response(
            {
                "message": "Account created successfully."
            },
            status=status.HTTP_201_CREATED
        )