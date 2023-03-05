from api.views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, CustomUserViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register(r'users', CustomUserViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
