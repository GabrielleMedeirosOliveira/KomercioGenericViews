from django.test import TestCase
from users.models import User
from products.models import Product


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "ricardo",
            "first_name": "Ricardo",
            "last_name": "Souza",
            "is_seller": True
        }

        cls.user = User.objects.create_user(**cls.user_data)

    def test_model_atributes_max_length(self):
        user = User.objects.get(username="ricardo")
        username = user._meta.get_field("username").max_length
        first_name = user._meta.get_field("first_name").max_length
        last_name = user._meta.get_field("last_name").max_length

        self.assertEqual(username, 20)
        self.assertEqual(first_name, 50)
        self.assertEqual(last_name, 50)

    def test_model_atribute_unique(self):
        user = User.objects.get(username="ricardo")
        username = user._meta.get_field("username").unique

        self.assertTrue(username)


class RelationsUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "username": "ricardo",
            "first_name": "Ricardo",
            "last_name": "Souza",
            "is_seller": True
        }

        cls.product_data = {
            "description": "Forno Microondas",
            "price": 499.00,
            "quantity": 25,
            "is_active": True
        }

        cls.user = User.objects.create_user(**cls.user_data)
        cls.product = [Product.objects.create(
            **cls.product_data, seller=cls.user) for _ in range(15)]

    def test_user_can_have_mutiples_products(self):
        self.assertEqual(len(self.product), self.user.products.count())

        for product in self.product:
            self.assertEqual(self.user, product.seller)