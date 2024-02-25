from django.urls import include, path
from rest_framework.routers import SimpleRouter

<<<<<<< HEAD
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
=======
from .views import AddUserViewSet, UserAdminViewSet

router = SimpleRouter()

router.register('auth', AddUserViewSet)
router.register('users', UserAdminViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
>>>>>>> 4436f67de89ed336177881d97ea006424f4cd000
]
