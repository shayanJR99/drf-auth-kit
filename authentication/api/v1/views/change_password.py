from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from authentication.api.v1.serializers.change_password import ChangePasswordSerializer
from authentication.services.change_password import ChangePasswordService
from emails.api.v1.serializers import MessageSerializer


@method_decorator(ratelimit(key='ip', rate='3/m', method='POST', block=True), name='dispatch')
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: MessageSerializer}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        ChangePasswordService.execute(
            user=request.user,
            new_password=serializer.validated_data["new_password"]
        )

        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK
        )