from api.serializers import (IngredientSerializer, ReadOnlyRecipeSerializer,
                             RecipeSerializer, SubscriptionSerializer,
                             TagSerializer)
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription, User


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
    # serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyRecipeSerializer
        return RecipeSerializer


class CustomUserViewSet(UserViewSet):

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        user = User.objects.get(pk=request.user.pk)
        author = get_object_or_404(User, pk=id)
        is_subscribed = Subscription.objects.filter(
            author=author, subscriber=user
        ).exists()
        if request.method == 'POST':
            if is_subscribed or user == author:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(subscriber=user, author=author)
            return Response(status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            if not is_subscribed:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.get(subscriber=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        subscriptions = Subscription.objects.filter(subscriber=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
