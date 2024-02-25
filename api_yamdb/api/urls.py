from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AddUserViewSet, CategoryViewSet, GenreViewSet,
                    TitleViewSet, UserAdminViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('auth', AddUserViewSet)
router.register('users', UserAdminViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router.urls))
]
