import random
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from users.serializers import RegisterSerializer, LoginSerializer, ImageSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import UserModel, Image, Confirm
from django.shortcuts import render


class RegisterViewSet(GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    host_user = 'settings.EMAIL_HOST_USER'

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = UserModel.objects.create_user(**serializer.validated_data)
        user.is_active = False
        code = Confirm.objects.create(user=user, code=random.randint(1000000, 10000000))
        email = request.data.get('email')
        send_mail('Account Details',
                  str(code.code),
                  self.host_user,
                  [email],
                  fail_silently=False)
        user.save()
        return Response(data={"status":"the code was sent to the mail!"})

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class LoginViewSet(GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response(
                {
                    "status": status.HTTP_200_OK,
                    "user": user.username,
                    "token": str(refresh),
                    "access_token": str(access)
                }
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class ConfirmationAPIView(ListAPIView):
    @staticmethod
    def post(request):
        code = request.data.get('code')
        confirm = get_object_or_404(Confirm, code=code)
        user = confirm.user
        user.is_active = True
        user.save()
        confirm.delete()
        return Response(data={'status':'User confirmed!'})

class ImageAPIView(APIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def post(self,request):
        image = Image.objects.create(image=request.data)
        return Response(data={'image':'uploaded'})
