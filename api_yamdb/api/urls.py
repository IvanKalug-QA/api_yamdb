from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AddUserViewSet, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet,
                    UserAdminViewSet)

app_name = 'api'

router = SimpleRouter()

router.register('auth', AddUserViewSet)
router.register('users', UserAdminViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
