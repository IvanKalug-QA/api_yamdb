from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import CategoryGenreMixin
from .permissions import AdminPermission, IsAdminOrReadOnly, IsStaffOrReadOnly
from .serializers import (AddUserSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitleSerializer, UserSerializer,
                          AuthUserSerializer)
from .utils import send_message

User = get_user_model()


class AddUserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = (AllowAny,)

    @action(methods=['POST'], detail=False)
    def token(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        comfirmation_code = serializers.data.get('confirmation_code')

        user = get_object_or_404(User, username=serializers.data.get(
            'username'))

        if (not default_token_generator.check_token(
                user, comfirmation_code) and comfirmation_code != '0'):
            return Response({'Ошибка': 'Неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'token': str(AccessToken.for_user(user))},
                        status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        try:
            user = User.objects.get(
                username=username,
                email=email)
        except User.DoesNotExist:
            serializer = AddUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        token = default_token_generator.make_token(user)
        send_message(email, token)
        return Response(
            data={'email': email,
                  'username': username})


class UserAdminViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            data = request.data.copy()
            if data.get('role'):
                data.pop('role')
            serializer = self.get_serializer(user,
                                             data=data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsStaffOrReadOnly,
                          )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = Review.objects.select_related('author').all()
        return queryset.filter(title=self.get_title())

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsStaffOrReadOnly,
                          )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.get_review().comments.select_related(
            'review__author').all()

    def get_review(self):
        return get_object_or_404(
            Review.objects.select_related('title'),
            title_id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id'),
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review().id)
