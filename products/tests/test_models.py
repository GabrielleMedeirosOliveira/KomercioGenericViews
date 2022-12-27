from django.test import TestCase
from products.models import Product
from users.models import User


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_data = {
            "description": "Forno Microondas",
            "price": 499.00,
            "quantity": 25,
            "is_active": True
        }

        cls.user_data_1 = {
            "username": "ricardo",
            "first_name": "Ricardo",
            "last_name": "Souza",
            "is_seller": True
        }

        cls.user = User.objects.create_user(**cls.user_data_1)
        cls.product = Product.objects.create(
            **cls.product_data, seller=cls.user)

    def test_model_atributes(self):
        product = Product.objects.get(id=self.product.id)
        price_max_digits = product._meta.get_field("price").max_digits
        price_decimal = product._meta.get_field("price").decimal_places

        self.assertEqual(price_max_digits, 10)
        self.assertEqual(price_decimal, 2)


class RelationsProductsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product_data = {
            "description": "Forno Microondas",
            "price": 499.00,
            "quantity": 25,
            "is_active": True
        }

        cls.user_data_1 = {
            "username": "ricardo",
            "first_name": "Ricardo",
            "last_name": "Souza",
            "is_seller": True
        }

        cls.user_data_2 = {
            "username": "fernando",
            "first_name": "Fernando",
            "last_name": "Silva",
            "is_seller": True
        }

        cls.user1 = User.objects.create_user(**cls.user_data_1)
        cls.user2 = User.objects.create_user(**cls.user_data_2)
        cls.product = Product.objects.create(
            **cls.product_data, seller=cls.user1)

    def test_one_product_only_for_one_seller(self):
        self.assertIn(self.product, self.user1.products.filter(
            description="Forno Microondas"))

        self.user2.products.add(self.product)
        self.assertNotIn(self.product, self.user1.products.filter(
            description="Forno Microondas"))
        self.assertIn(self.product, self.user2.products.filter(
            description="Forno Microondas"))