from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        exctrocraks = {"password": {'write_only': True}}

    def validate_password(self, password):
        if not password.isalnum():
            raise ValidationError('Password should consist only letters and numbers!')
        return password



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["token"]


class VerificationSerializer(serializers.Serializer):
    title = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()