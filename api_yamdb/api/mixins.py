from rest_framework import filters, mixins, viewsets
from rest_framework.serializers import ValidationError

from .permissions import IsAdminOrReadOnly


class CategoryGenreMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class ValidateUsernameMixin:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Такое имя запрещено!')
        return value
