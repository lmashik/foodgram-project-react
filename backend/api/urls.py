from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    get_jwt_token,
    set_password,
    sign_up
)

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/users/set_password', set_password, name='set_password'),
    path('v1/auth/token/login/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_jwt_token, name='send_conf_code'),
    path('v1/', include(router_v1.urls)),
]
