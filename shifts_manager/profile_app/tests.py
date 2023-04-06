from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your tests here.
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "test_name",
            "email": "test@test.com",
            "password": "TestPassword!123"
        }

        response = self.client.post(reverse("profile-registration"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "Registration Successful")


        data = {
            "username": "test_name_2",
            "email": "test@test.com",
            "password": "TestPassword!123"
        }

        response = self.client.post(reverse("profile-registration"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Profile with this email already exists.")


class LoginTestCase(APITestCase):

    def setUp(self):
        self.profile = User.objects.create_user(
            username="test_user",
            password="test_pass"
        )

    def test_login(self):
        data = {
            "username": "test_user",
            "password": "test_pass"
        }

        response = self.client.post(reverse("profile-login"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.json())

    def test_logout(self):
        self.token = Token.objects.get(user__username="test_user")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('profile-logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
