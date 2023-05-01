from django.contrib.auth import authenticate
from django.middleware.csrf import logger
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, LoginSerializer,VerificationSerializer
from django.core.mail import send_mail
from django.conf import settings

class RegisterViewSet(GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request) :
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        user.save()
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class LoginViewSet(GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
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



@api_view(['POST'])
def send_email(request):
    if request.method == 'POST':
        serializer = VerificationSerializer(data=request.data)
        title = request.data.get('title')
        email = request.data.get('email')
        message = request.data.get('message')
        send_mail(
            'Account Details',
            message,
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False)
    return Response(data={'message':'send'})