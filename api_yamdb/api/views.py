from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter


from .permissions import AdminPermission
from .serializers import AddUserserializer, UsersSerializer

User = get_user_model()

CODE_FOR_USER = '256'


class AddUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AddUserserializer
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=False)
    def token(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if not username or not confirmation_code:
            return Response({'error': 'Необходимо предоставить username и confirmation_code'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)

        access = AccessToken.for_user(user)
        token = {
            'token': str(access),
        }

        return Response(token, status=status.HTTP_200_OK)

    def create(self, validated_data):
        try:
            current_user = User.objects.get(
                username=self.request.data.get('username'))     
        except User.DoesNotExist:
            return super().create(validated_data)
        send_mail(
            subject="Код подтверждения",
            from_email="kaluginivan2002@mail.ru",
            recipient_list=[current_user.email],
            message=f'Код для получения токена: {CODE_FOR_USER}',
            fail_silently=False,
        )
        return Response(data={'Сообщение': 'Ваш код успешно отправлен!'})

    def perform_create(self, serializer):
        instance = serializer.save()
        send_mail(
            subject="Код подтверждения",
            from_email="kaluginivan2002@mail.ru",
            recipient_list=[instance.email],
            message='Код для полечения токена: 123',
            fail_silently=False,
        )
        return instance


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [AdminPermission,]
    filter_backends = [SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
