from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema
from utils.mixins import SerializerByMethodMixin
from .models import Product
from .serializers import ProductGeneralSerializer, ProductSerializer, ProductFilterSerializer
from .permissions import CustomProductPermission, CustomIdProductPermission


class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [CustomProductPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET': ProductGeneralSerializer,
        'POST': ProductSerializer,
    }
    authentication_classes = [TokenAuthentication]
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


@extend_schema(methods=['PUT'], exclude=True)
class ProductIdView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomIdProductPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET': ProductFilterSerializer,
        'PATCH': ProductSerializer,

    }