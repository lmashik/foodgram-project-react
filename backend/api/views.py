from api.serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer, CustomUserSerializer
)
from djoser.views import UserViewSet
from djoser.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


# class CustomUserViewSet(UserViewSet):
#
#     def get_serializer_class(self):
#         if self.action in ('list', 'retrieve', 'create'):
#             return CustomUserSerializer
#         return UserSerializer
