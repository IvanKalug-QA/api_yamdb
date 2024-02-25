from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import IsAdminOrReadOnly


class CategoryGenreMixin(mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin, viewsets.GenericViewSet):
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
