from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from rest_framework.test import APIClient
from rest_framework import status

from board.models import Board

CREATE_BOARD_URL = reverse("boards:boards")

def create_user(**params):
    """ Function to create users easily """
    return get_user_model().objects.create_user(**params)

class ModelTest(TestCase):
    """ Test Boards model """

    def setUp(self):
        self.user = create_user(
            email="ann30@outlook.com",
            password="AnnHdz30",
            name="Anais"
        )
        self.payload = {
            "title": "anais@hotmail.com",
            "author": self.user.id
        }
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_board_successfull(self):
        """ Test: Create a board successfully """
        res = self.client.post(CREATE_BOARD_URL, self.payload)
        
        self.assertIn("board_id", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_get_boards_from_user_successfull(self):
    #     """ Test: Get boards from user """
    #     board = self.client.post(CREATE_BOARD_URL, self.payload)

