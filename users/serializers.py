from unittest.mock import seal
from rest_framework import serializers

from .models import User


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "is_seller", "date_joined", "is_active", "is_superuser", "password"]

        extra_kwargs = {"is_seller": {'required': True}}
        read_only_fields = ["is_active"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AccountLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "is_seller", "date_joined", "is_active", "is_superuser", "password"]
        read_only_fields = ["date_joined", "is_active", "is_superuser"]


class AccountInactivatedSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "is_seller", "date_joined", "is_active", "is_superuser", "password"]
        extra_kwargs = {"is_active": {'required': True}}    