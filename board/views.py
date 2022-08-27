from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BoardSerializer
# Create your views here.

class BoardsView(APIView):

    def get(self, request, user_id):
        pass

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )