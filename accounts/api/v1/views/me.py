from ..serializers import MeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class MeAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        serializer = MeSerializer(
            request.user
        )

        return Response(
            serializer.data
        )