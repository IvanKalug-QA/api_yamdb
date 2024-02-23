from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AddUserViewSet, UserAdminViewSet

router = SimpleRouter()

router.register('auth', AddUserViewSet)
router.register('users', UserAdminViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
