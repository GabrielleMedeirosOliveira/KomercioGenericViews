from rest_framework import serializers

from .models import Product
from users.models import User


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "is_seller", "date_joined", "is_active", "is_superuser"]
        read_only_fields = ["is_active"]


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0, coerce_to_string=False
    )

    class Meta:
        model = Product
        fields = ["id", "description",
                  "price", "quantity", "is_active", "seller"]
        extra_kwargs = {"description": {'required': True}}
        extra_kwargs = {"price": {'required': True}}
        extra_kwargs = {"quantity": {'required': True}}


class ProductFilterSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["description",
                  "price", "quantity", "is_active", "seller"]


class ProductGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller"]