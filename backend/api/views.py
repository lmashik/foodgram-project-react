from api.serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer, CustomUserSerializer
)
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscription, User
from rest_framework import viewsets, permissions
from rest_framework.decorators import action


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


class CustomUserViewSet(UserViewSet):

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk=None):
        if request.method == 'post':
            Subscription.objects.create(
                subscriber=request.user.pk, author=User.objects.get(pk=pk).pk
            )
        if request.method == 'delete':
            Subscription.objects.get(
                subscriber=request.user.pk, author=User.objects.get(pk=pk).pk
            ).delete()
