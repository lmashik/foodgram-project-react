from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, RecipeViewSet, IngredientViewSet

router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router_v1.urls)),
]
