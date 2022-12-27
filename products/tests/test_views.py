from itertools import product
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

from users.models import User
from products.models import Product


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.list_create_update_url = "/api/products/"

        cls.product = {
            "description": "Liquidificador",
            "price": 199,
            "quantity": 30,
        }

        cls.product_2 = {
            "description": "Batedeira",
            "price": 499,
            "quantity": 10,
        }

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

        cls.user_data_seller_2 = {
            "username": "patricia",
            "password": "abc123",
            "first_name": "Patricia",
            "last_name": "Lins",
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

        cls.user_data_login_seller_2 = {
            "username": "patricia",
            "password": "abc123"
        }

        cls.user_data_login_not_seller = {
            "username": "augusto",
            "password": "abc123"
        }

        cls.adm = User.objects.create_superuser(**cls.user_adm)
        cls.token_adm = Token.objects.create(user=cls.adm)

        cls.seller = User.objects.create_user(**cls.user_data_seller)
        cls.token_seller = Token.objects.create(user=cls.seller)

        cls.seller_2 = User.objects.create_user(**cls.user_data_seller_2)
        cls.token_seller_2 = Token.objects.create(user=cls.seller_2)

        cls.not_seller = User.objects.create_user(**cls.user_data_not_seller)
        cls.token_not_seller = Token.objects.create(user=cls.not_seller)

        cls.product_created = Product.objects.create(
            **cls.product_2, seller=cls.seller_2)

        cls.products = [
            Product.objects.create(
                description=f"Produto {product_id}",
                price=99,
                quantity=5,
                seller=cls.seller,
            )
            for product_id in range(1, 5)
        ]

    def test_create_product_with_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response = self.client.post(
            self.list_create_update_url, data=self.product)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 6)
        self.assertIn('id', response.data)
        self.assertIn("description",  response.data)
        self.assertIn("price",  response.data)
        self.assertIn("quantity",  response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("seller", response.data)

        self.assertEqual(len(response.data["seller"].keys()), 8)

    def test_create_product_without_token(self):
        response = self.client.post(
            self.list_create_update_url, data=self.product)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_create_product_with_not_seller(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_not_seller.key)

        response = self.client.post(
            self.list_create_update_url, data=self.product)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "You do not have permission to perform this action."
        )

    def test_create_product_with_adm(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_adm.key)

        response = self.client.post(
            self.list_create_update_url, data=self.product)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "You do not have permission to perform this action."
        )

    def test_create_with_wrong_keys(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response = self.client.post(
            self.list_create_update_url, data={})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["description"][0], "This field is required."
        )
        self.assertEqual(
            response.data["price"][0], "This field is required."
        )
        self.assertEqual(
            response.data["quantity"][0], "This field is required."
        )

    def test_can_list_products(self):
        response = self.client.get(
            self.list_create_update_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn('results', response.data)
        self.assertEqual(len(self.products), len(response.data))
        self.assertEqual(len(response.data['results'][0].keys()), 5)

    def test_can_filter_product(self):
        response = self.client.get(
            f'{self.list_create_update_url}{self.product_created.id}/')

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 5)

    def test_only_owner_can_edit_product(self):
        product = Product.objects.create(**self.product, seller=self.seller)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller.key)

        response = self.client.patch(
            f'{self.list_create_update_url}{product.id}/', data={"price": 250})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(len(response.data.keys()), 6)

    def test_other_user_can_edit_product(self):
        product = Product.objects.create(**self.product, seller=self.seller)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller_2.key)

        response = self.client.patch(
            f'{self.list_create_update_url}{product.id}/', data={"price": 250})

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_can_register_with_negative_number(self):
        product_data = {"description": "Liquidificador",
                        "price": 199,
                        "quantity": -30, }

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token_seller_2.key)

        response = self.client.post(
            self.list_create_update_url, data=product_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn("quantity", response.data)
        self.assertIn(
            "Ensure this value is greater than or equal to 0.", response.data["quantity"])