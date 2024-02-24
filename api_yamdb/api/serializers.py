from rest_framework import serializers, validators, status
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework.response import Response

User = get_user_model()


class AddUserserializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, validators=[validators.UniqueValidator(queryset=User.objects.all()), RegexValidator(regex=r'^[\w.@+-]+\Z',message='Enter a valid username.',code='invalid_username')])
    
    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Такое имя запрещено!')
        return value


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username'),
            )
        ]

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Такое имя запрещено!')
        return value


class EditUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")
        read_only_fields = ("role",)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Такое имя запрещено!')
        return value
