from rest_framework import viewsets

from recipes.models import Tag, Recipe, Ingredient
from api.serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientSerializer
)


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
