from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token


from users.models import User


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = "/api/accounts/"

        cls.login_url = "/api/login/"

        cls.update_url = "/api/accounts/"

        cls.user_adm = {
            "username": "adm1",
            "password": "adm123",
            "first_name": "Adm1",
            "last_name": "Super"
        }

        cls.user_data_seller = {
            "username": "ricardo",
            "password": "abc123",
            "first_name": "Ricardo",
            "last_name": "Souza",
            "is_seller": True
        }

        cls.user_data_not_seller = {
            "username": "augusto",
            "password": "abc123",
            "first_name": "Augusto",
            "last_name": "Lopes",
            "is_seller": False
        }

        cls.user_data_login_seller = {
            "username": "ricardo",
            "password": "abc123"
        }

        cls.user_data_login_not_seller = {
            "username": "augusto",
            "password": "abc123"
        }

    def test_register_user_seller(self):
        response = self.client.post(self.register_url, self.user_data_seller)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertTrue(
            response.data["is_seller"])

    def test_register_user_not_seller(self):
        response = self.client.post(
            self.register_url, self.user_data_not_seller)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertFalse(
            response.data["is_seller"])

    def test_register_wrong_keys(self):
        response = self.client.post(self.register_url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["username"][0], "This field is required."
        )
        self.assertEqual(
            response.data["password"][0], "This field is required."
        )
        self.assertEqual(
            response.data["password"][0], "This field is required."
        )
        self.assertEqual(
            response.data["first_name"][0], "This field is required."
        )
        self.assertEqual(
            response.data["last_name"][0], "This field is required."
        )

    def test_login_user_seller(self):
        response = self.client.post(self.register_url, self.user_data_seller)
        response = self.client.post(
            self.login_url, self.user_data_login_seller)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("token", response.data)

    def test_login_user_not_seller(self):
        response = self.client.post(
            self.register_url, self.user_data_not_seller)
        response = self.client.post(
            self.login_url, self.user_data_login_not_seller)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("token", response.data)

    def test_login_wrong_keys(self):
        response = self.client.post(
            self.register_url, self.user_data_not_seller)
        response = self.client.post(
            self.login_url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["username"][0], "This field is required."
        )
        self.assertEqual(
            response.data["password"][0], "This field is required."
        )

    def test_list_users(self):
        response = self.client.get(self.register_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_update_by_not_owner(self):
        user_owner = User.objects.create_user(**self.user_data_seller)
        token_owner = Token.objects.create(user=user_owner)
        user_not_owner = User.objects.create_user(**self.user_data_not_seller)
        token_not_owner = Token.objects.create(user=user_not_owner)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token_not_owner.key)

        response = self.client.patch(
            f'{self.update_url}{user_owner.id}/', data={"last_name": "Nogueira"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_by_owner(self):
        user_owner = User.objects.create_user(**self.user_data_seller)
        token = Token.objects.create(user=user_owner)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f'{self.update_url}{user_owner.id}/', data={"last_name": "Nogueira"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_is_active_with_not_adm(self):
        user = User.objects.create_user(**self.user_data_seller)
        token = Token.objects.create(user=user)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.patch(
            f'{self.update_url}{user.id}/management/', data={"is_active": False})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_is_active_with_adm(self):
        adm = User.objects.create_superuser(**self.user_adm)
        token = Token.objects.create(user=adm)

        user_seller = User.objects.create_user(**self.user_data_seller)

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key)

        deactive_user = {"is_active": False}

        response = self.client.patch(
            f'{self.update_url}{user_seller.id}/management/', data=deactive_user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"],
                         deactive_user["is_active"])