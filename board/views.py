from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from .serializers import BoardSerializer
from .models import Board
from profiles.models import UserProfile
# Create your views here.


class ViewPermissions(BasePermission):

    def has_permissions(self, request, view):
        return False


class BoardsView(APIView):
    """ Boards class """
    permission_classes = [
        IsAuthenticated | ViewPermissions
    ]

    def get(self, request, pk):
        """ Returns the boards for the specific user """
        user_exists = UserProfile.objects.filter(id=pk).exists()

        if not user_exists:
            response = {
                "message": "There is no user with the specified id"
            }
            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = Board.objects.filter(author_id=pk)
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

    def delete(self, request, pk):
        """ Deletes the specified board """
        board_exists = Board.objects.filter(id=pk).exists()

        if not board_exists:
            return Response(
                {
                    "msg": "There is no board with the specified id"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        Board.objects.filter(id=pk).delete()

        return Response(
            {
                "msg": "Board deleted successfully"
            },
            status=status.HTTP_200_OK
        )
