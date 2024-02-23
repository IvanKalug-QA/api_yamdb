from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination


from .permissions import AdminPermission
from .serializers import AddUserserializer, UsersSerializer, EditUserSerializer

User = get_user_model()

CODE_FOR_USER = '256'


def send_message(to):
    return send_mail(
        subject="Код подтверждения",
        from_email="kaluginivan2002@mail.ru",
        recipient_list=[to],
        message=f'Код для получения токена: {CODE_FOR_USER}',
        fail_silently=False,
    )


class AddUserMixin(CreateModelMixin, GenericViewSet):
    pass


class AddUserViewSet(AddUserMixin):
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

        if confirmation_code != CODE_FOR_USER:
            return Response({'Ошибка': 'Неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"token": AccessToken.for_user(user)},
                        status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        if self.request.data.get('username') == 'me':
            return Response(data={'Error': 'Такое имя запрещено!'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            current_user = User.objects.get(
                username=self.request.data.get('username'))
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_message(serializer.data.get('email'))
                return Response(data=serializer.data)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if (not self.request.data.get('username')
                or not self.request.data.get('email')):
            return Response(data={'Error': 'нет обязательного поля username'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif current_user.email != self.request.data.get('email'):
            return Response(data={'Сообщение': 'Не верный email'},
                            status=status.HTTP_400_BAD_REQUEST)
        send_message(current_user.email)
        return Response(data={'Сообщение': 'Ваш код успешно отправлен!'})


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
        if self.request.method == 'GET':
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
