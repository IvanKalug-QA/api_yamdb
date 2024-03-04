from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class AddUserserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Такое имя запрещено!")
        return value


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Такое имя запрещено!")
        return value


class AuthUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug")


class SlugToDictField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        result = {"name": obj.name, "slug": obj.slug}
        return result


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugToDictField(
        many=True, slug_field="slug", queryset=Genre.objects.all(),
    )
    category = SlugToDictField(
        slug_field="slug", queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description",
                  "genre", "category")

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg("score")).get("score__avg")

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError("Empty_genre")
        return value


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = ("id", "name", "year", "rating", "description",
                  "genre", "category")

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg("score")).get("score__avg")


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field="username", read_only=True)
    score = serializers.IntegerField(min_value=1,
                                     max_value=10)

    def get_title(self):
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title

    def validate(self, data):
        if self.context.get("request").method != "POST":
            return data
        if Review.objects.filter(title=self.get_title(),
                                 author=self.context.get("request").user
                                 ).exists():
            raise serializers.ValidationError("нельзя оставить отзыв дважды.")
        return data

    class Meta:
        model = Review
        fields = (
            "id",
            "pub_date",
            "text",
            "author",
            "score",
        )


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field="username",
                                          read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "pub_date",
            "text",
            "author",
        )
