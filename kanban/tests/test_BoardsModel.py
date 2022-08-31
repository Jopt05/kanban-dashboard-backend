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
            "title": "Anais Blog",
            "author": self.user.id
        }
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_board_successfull(self):
        """ Test: Create a board successfully """
        res = self.client.post(CREATE_BOARD_URL, self.payload)

        self.assertIn("id", res.data["board"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_board_error(self):
        """ Test: Error on board creation """
        wrong_payload = {
            "title": "",
            "author": self.user.id
        }

        res = self.client.post(CREATE_BOARD_URL, wrong_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_boards_from_user_successfull(self):
        """ Test: Get boards from user """
        res = self.client.post(CREATE_BOARD_URL, self.payload)

        res_get = self.client.get(
            reverse(
                "boards:boards",
                kwargs={
                    "pk": self.user.id
                }
            )
        )

        self.assertIn(res.data["board"], res_get.data["data"])

    def test_delete_board_from_user_successful(self):
        """ Test: Delete board from user """
        res = self.client.post(CREATE_BOARD_URL, self.payload)

        board_id = res.data["board"]["id"]

        res_delete = self.client.delete(
            reverse(
                "boards:boards",
                kwargs={
                    "pk": board_id
                }
            )
        )

        self.assertEqual(res_delete.status_code, status.HTTP_200_OK)
        self.assertIn("successfully", res_delete.data["msg"])
