from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.api.v1.serializers.login import (
    LoginSerializer,
    TokenResponseSerializer,
)
from drf_spectacular.utils import extend_schema


from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='dispatch')
@extend_schema(auth=[])
class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    @extend_schema(responses=TokenResponseSerializer)
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
