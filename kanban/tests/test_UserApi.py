from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

REGISTER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")


def create_user(**params):
    """ Function to create users easily """
    return get_user_model().objects.create_user(**params)


class PublicAuthApiTests(TestCase):

    payload = {
        "email": "anais@hotmail.com",
        "password": "ann1234",
        "name": "testing"
    }

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test: Create user with payload successfully """

        res = self.client.post(REGISTER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertTrue(user.check_password(self.payload["password"]))

        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """ Test: Create user with credentials already used """
        create_user(**self.payload)

        res = self.client.post(REGISTER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """ Test: Create token for user """

        create_user(**self.payload)

        res = self.client.post(LOGIN_URL, self.payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test: Token isnt created with invalid credentials """
        create_user(**self.payload)

        invalid_payload = {
            "email": "ann@outlook.com",
            "password": "ann12345"
        }

        res = self.client.post(LOGIN_URL, invalid_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test: Wont create token if no user """

        res = self.client.post(LOGIN_URL, self.payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password(self):
        """ Test: Email and password required """
        res = self.client.post(LOGIN_URL, {
            "email": "dumb",
            "password": ""
        })

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
