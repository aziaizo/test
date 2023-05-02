from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    password1 = serializers.CharField(min_length=8)

    class Meta:
        model = UserModel
        fields = ["username", "email", "password", "password1"]
    #     # exctrocraks = {"password": {'write_only': True}}

    @staticmethod
    def validate_password(password, password1):
        if not password.isalnum():
            raise ValidationError('Password should consist only letters and numbers!')
        elif password != password1:
            raise ValidationError('password no confirmed!')
        return password


    @staticmethod
    def validate_username(username):
        try:
            UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return username
        raise ValidationError('User already exists!')




class LoginSerializer(serializers.Serializer):
    class Meta:
        model = UserModel
        fields = ["token"]

    username = serializers.CharField()
    password = serializers.CharField()





class ImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        fields = ["image"]



