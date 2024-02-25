from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class AddUserserializer(serializers.ModelSerializer):

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
