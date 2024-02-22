from rest_framework import serializers
from django.contrib.auth import get_user_model

from reviews.models import ROOT

User = get_user_model()


class AddUserserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROOT)

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")
