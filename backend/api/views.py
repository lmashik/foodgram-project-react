from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer, RecipeSerializer, ShortRecipeSerializer,
    SubscriptionSerializer, TagSerializer,
)
from api.utils import create_pdf_shopping_cart
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorites, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    """Представление для пользователей."""

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

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        subscriptions_authors = User.objects.filter(
            subscriptions__subscriber=user
        )
        pages = self.paginate_queryset(subscriptions_authors)
        serializer = SubscriptionSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


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
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy',):
            return (IsAuthorOrReadOnly(),)
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.request.user.is_anonymous:
            is_favorite, is_in_shopping_cart = False, False
        else:
            is_favorite = self.request.query_params.get('is_favorited')
            is_in_shopping_cart = self.request.query_params.get(
                'is_in_shopping_cart'
            )
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if is_favorite == 1:
            queryset = queryset.filter(favorites__user=self.request.user)
        if is_in_shopping_cart == 1:
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        return queryset

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = User.objects.get(pk=request.user.pk)
        recipe = get_object_or_404(Recipe, pk=pk)
        is_favorite = Favorites.objects.filter(
            user=user, recipe=recipe
        ).exists()
        if request.method == 'POST':
            if is_favorite:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not is_favorite:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    # def favorites(self, request):
    #     user = request.user
    #     recipes = Recipe.objects.filter(favorites__user=user)
    #     serializer = ShortRecipeSerializer(recipes, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        user = User.objects.get(pk=request.user.pk)
        recipe = get_object_or_404(Recipe, pk=pk)
        is_in_shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists()
        if request.method == 'POST':
            if is_in_shopping_cart:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not is_in_shopping_cart:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        recipes = Recipe.objects.filter(shopping_cart__user=user)
        ingredients = recipes.values(
            'recipeingredient__ingredient__name',
            'recipeingredient__ingredient__measurement_unit',
        ).annotate(
            amount=Sum('recipeingredient__amount')
        ).order_by()

        ingredients_list = [
            f"{item['recipeingredient__ingredient__name']}: "
            f"{item['amount']} "
            f"{item['recipeingredient__ingredient__measurement_unit']}"
            for item in ingredients
        ]

        return FileResponse(
            create_pdf_shopping_cart(ingredients_list),
            as_attachment=True,
            filename='ShoppingCart.pdf'
        )
