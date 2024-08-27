# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import OutstandingToken

from .models import User, OneTimePassword


# Templates Tests
# class UserTestsCase(TestCase):
#     def setUp(self):
#         self.user_data = {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'testpassword123',
#             'password2': 'testpassword123',
#         }

#     def test_register_view(self):
#         response = self.client.get(reverse('register'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'register.html')

#     def test_user_registration(self):
#         response = self.client.post(
#             reverse('register'), {**self.user_data})
#         self.assertEqual(response.status_code, 302)

#         user = User.objects.get(username=self.user_data['username'])
#         self.assertIsNotNone(user)

#     def test_login_view(self):
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')

#     def test_user_login(self):
#         user = User.objects.create_user(
#             username='testuser', password='testpassword123')
#         response = self.client.post(reverse('login'), {
#             'username': 'testuser',
#             'password': 'testpassword123',
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.wsgi_request.user.is_authenticated)

#     def test_logout_view(self):
#         user = User.objects.create_user(
#             username=self.user_data['username'], password=self.user_data['password'])
#         self.client.login(
#             username=self.user_data['username'], password=self.user_data['password'])

#         response = self.client.post(reverse('logout'))
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(response.wsgi_request.user.is_authenticated)
#         self.assertTemplateUsed(response, 'accounts/logged_out.html')


# Api Tests
class UserApiTestCase(APITestCase):
    def setUp(self):
        self.base_url = "/auth/"
        self.client.post(f"{self.base_url}register/", {"email": "test@test.net", "first_name": "Te",
                         "last_name": "St", "password": "tester00", "password2": "tester00"})

        # get opt code
        otp = OneTimePassword.objects.get(
            user=User.objects.get(email="test@test.net"))
        # use otp code to verify user email
        self.client.get(f"{self.base_url}register/verify?code={otp.code}")

        response = self.client.post(
            self.base_url +
            "login/", {"email": "test@test.net", "password": "tester00"}
        )

        # Proof that the user logged in correctly
        self.assertEqual(response.status_code, 200)

        self.token = response.data["access_token"]
        self.refresh_token = response.data["refresh_token"]

        return super().setUp()

    def test_user_register_view(self):
        url = f"{self.base_url}register/"

        data = {
            "email": "tester01@tester.net",
            "first_name": "Test",
            "last_name": "Ter",
            "password": "tester00",
            "password2": "tester00",
        }

        # Register
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(email="tester01@tester.net")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Ter")
        self.assertEqual(response.data, "Successfully registered!")
        self.assertEqual(user.is_active, False)

        # Register Verify
        code = OneTimePassword.objects.get(user=user).code
        response = self.client.get(f"{url}verify?code={code}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "Email verified successfully!")
        user = User.objects.get(email="tester01@tester.net")
        self.assertEqual(user.is_active, True)

    def test_user_register_view_fail(self):
        url = f"{self.base_url}register/"

        data = {
            "email": "XXXXXXXXXXXXXXXXXXX",
            "first_name": "Test",
            "last_name": "Ter",
            "password": "tester00",
            "password2": "tester00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        data = {
            "email": "tester01@tester.net",
            "first_name": "Test",
            "last_name": "Ter",
            "password": "XXXXXXXX",
            "password2": "tester00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_user_login_view(self):
        url = f"{self.base_url}login/"

        data = {"email": "test@test.net", "password": "tester00"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_user_login_view_fail(self):
        url = f"{self.base_url}login/"

        data = {"email": "XXXXXXXXXXXXX", "password": "XXXXXXXX"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        data = {"email": "XXXXXXXXXXXXXXXXXXX", "password": "XXXXXXXX"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_user_logout_view(self):
        url = f"{self.base_url}logout/"
        url_login = f"{self.base_url}login/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.post(url, {"refresh_token": self.refresh_token})
        self.assertEqual(response.status_code, 204)

        # Logout All
        data = {"email": "test@test.net", "password": "tester00"}
        rp = self.client.post(url_login, data)
        rp = self.client.post(url_login, data)
        rp = self.client.post(url_login, data)
        self.assertEqual(rp.status_code, 200)

        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + rp.data["access_token"])
        response = self.client.delete(
            url, {"refresh_token": rp.data["refresh_token"]})
        self.assertEqual(response.status_code, 204)

        user_id = User.objects.get(email="test@test.net").id
        oustanding_tokens_count = OutstandingToken.objects.filter(
            user_id=user_id).count()
        self.assertEqual(oustanding_tokens_count, 0)

    def test_user_logout_view_fail(self):
        url = f"{self.base_url}logout/"
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.delete(url, {})
        self.assertEqual(response.status_code, 400)

    def test_user_profile_view(self):
        url = f"{self.base_url}profile/view/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "test@test.net")
        self.assertEqual(response.data["full_name"], "St, Te")

    def test_user_profile_view_fail(self):
        url = f"{self.base_url}profile/view/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_user_profile_update_view(self):
        url = f"{self.base_url}profile/update/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        data = {"first_name": "StMod"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.get(id=1).first_name, "StMod")

    def test_user_profile_update_view_fail(self):
        url = f"{self.base_url}profile/update/"
        data = {"full_name": "StMod, Ter"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.put(url, {"email": "emailFake"})
        self.assertEqual(response.status_code, 400)
