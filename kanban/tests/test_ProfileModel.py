from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """ Test user model """

    email = "anais@test.com"
    password = "anaistheverybest"
    name = "Anais Rivera"

    def test_create_user_with_email_and_name_successful(self):
        """ Test: Create new user with email and name """
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password, self.password)

    def test_new_user_email_normalized(self):
        """ Tests normalized email for new user """

        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password,
            name=self.name
        )

        self.assertEqual(user.email, self.email.lower())

    def test_create_new_superuser(self):
        """ Test: Create new suepr user """

        super_user = get_user_model().objects.create_superuser(
            email=self.email,
            password=self.password,
            name=self.name
        )

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
