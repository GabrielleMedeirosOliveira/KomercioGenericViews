from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from .models import User
from .serializers import AccountSerializer, AccountLoginSerializer, AccountUpdateSerializer, AccountInactivatedSerializer
from .permissions import CustomUserOwnerPermission, CustomAdmPermission


class AccountView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
class ListAccountsBydateView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    def get_queryset(self):
        ordered_date = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:ordered_date]


class LoginView(APIView):
    queryset = User
    serializer_class = AccountLoginSerializer

    def post(self, request: Request) -> Response:
        serializer = AccountLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return Response({'detail': 'invalid username or password'}, status.HTTP_403_FORBIDDEN)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


@extend_schema(methods=['PUT'], exclude=True)
class UpdateUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomUserOwnerPermission]
    queryset = User.objects.all()
    serializer_class = AccountUpdateSerializer


@extend_schema(methods=['PUT'], exclude=True)
class InactivatedUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomAdmPermission]
    queryset = User.objects.all()
    serializer_class = AccountInactivatedSerializer