from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import BoardSerializer
from .models import Board
# Create your views here.


class BoardsView(APIView):
    """ Boards class """
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, user_id):
        """ Returns the boards for the specific user """
        queryset = Board.objects.filter(author_id=user_id)
        serializer = BoardSerializer(queryset, many=True)
        response = {
            "data": serializer.data,
            "message": "Success"
        }
        return Response(
            response,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """ Creates a new board """
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "msg": "Board created successfully",
                "board": serializer.data
            }
            return Response(
                response,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk):
        """ Edits the specific board """
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
