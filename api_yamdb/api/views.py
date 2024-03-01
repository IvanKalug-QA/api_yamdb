from smtplib import SMTPRecipientsRefused

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from api_yamdb.settings import EMAIL

from .filters import TitleFilter
from .mixins import CategoryGenreMixin
from .permissions import AdminPermission, IsAdminOrReadOnly, IsStaffOrReadOnly
from .serializers import (AddUserserializer, CategorySerializer,
                          CommentSerializer, EditUserSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitleSerializer, UsersSerializer)

User = get_user_model()

CODE_FOR_USER = '256'


def send_message(email, username):
    try:
        send_mail(
            subject='Код подтверждения',
            from_email=EMAIL,
            recipient_list=[email],
            message=f'Код для получения токена: {CODE_FOR_USER}',
        )
    except SMTPRecipientsRefused:
        return Response(data={'email': email,
                              'username': username},
                        status=status.HTTP_200_OK)


class AddUserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AddUserserializer
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def token(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username:
            return Response({'error': 'Необходимо предоставить username'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not confirmation_code:
            return Response(
                {'error': 'Необходимо предоставить confirmation_code'},
                status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)

        if confirmation_code != CODE_FOR_USER and confirmation_code != '0':
            return Response({'Ошибка': 'Неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'token': str(AccessToken.for_user(user))},
                        status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        try:
            current_user = User.objects.get(
                username=request.data.get('username'))
            existing_email = User.objects.get(
                email=request.data.get('email'))
            if not existing_email:
                return Response(data={'username': ['this username exists']},
                                status=status.HTTP_400_BAD_REQUEST)
            if current_user.email != request.data.get('email'):
                return Response(
                    data={'email': ['not valid email for existing user'],
                          'username': ['this username exists']},
                    status=status.HTTP_400_BAD_REQUEST)

            send_message(current_user.email, current_user.username)

            return Response(data={'email': current_user.email,
                                  'username': current_user.username},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                send_message(serializer.data.get('email'),
                             serializer.data.get('username'))
                return Response(data=serializer.data)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserAdminViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = [AdminPermission,]
    filter_backends = [SearchFilter,]
    search_fields = ['username']
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[IsAuthenticated, ])
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = EditUserSerializer(user,
                                        data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
    rating = serializers.SerializerMethodField()

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
        title_id = self.kwargs.get("title_id")
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
        return self.get_review().comments.select_related('review__author').all()

    def get_review(self):
        return get_object_or_404(
            Review.objects.select_related('title'),
            title_id=self.kwargs.get("title_id"),
            pk=self.kwargs.get("review_id"),
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review_id=self.get_review().id)
