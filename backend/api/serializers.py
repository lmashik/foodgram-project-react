from djoser.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""
    class Meta:
        model = Recipe
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        extra_kwargs = {'password': {'write_only': True}}
