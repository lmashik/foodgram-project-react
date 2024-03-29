from django.core.validators import MinValueValidator
from django.db import transaction
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorites, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag,
)
from rest_framework import serializers
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_subscribed = Subscription.objects.filter(
            author=obj,
            subscriber=request.user
        ).exists()
        return is_subscribed


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CustomPrimaryKeyField(serializers.RelatedField):
    """
    Кастомное поле для дальнейшего использования
    в сериализаторе рецептов.

    Позволяет при записи передавать id объектов.
    """
    def to_internal_value(self, data):
        model = self.Meta.model
        try:
            return model.objects.get(pk=data)
        except Exception as error:
            raise TypeError(f'Incorrect_type: {error}.')


class TagRelatedField(CustomPrimaryKeyField, TagSerializer):
    """
    Кастомное поле для тегов для использования
    в сериализаторе рецептов.

    Позволяет при записи передавать id объектов,
    а при чтении показывать полную информацию о теге.
    """
    pass


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        extra_kwargs = {'id': {'read_only': True}}


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов с указанием количества для рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )
    name = serializers.CharField(
        source='ingredient.name',
        required=False,
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        required=False,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов (подробный, чтение и запись)."""
    tags = TagRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient',
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(validators=(MinValueValidator(1),))

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Cooking time must be a positive integer.'
            )
        if len(data['recipeingredient']) == 0:
            raise serializers.ValidationError(
                'A recipe cannot be created without ingredients.'
            )
        for ingredient in data['recipeingredient']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Ingredient quantity must be a positive integer.'
                )
        id_list = [
            ingredient['ingredient']['id'].id
            for ingredient in data['recipeingredient']
        ]
        if len(id_list) > len(set(id_list)):
            raise serializers.ValidationError(
                'Ingredients cannot be repeated.'
            )
        return data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_favorite = Favorites.objects.filter(
            recipe=obj, user=request.user
        ).exists()
        return is_favorite

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_in_shopping_cart = ShoppingCart.objects.filter(
            recipe=obj, user=request.user
        ).exists()
        return is_in_shopping_cart

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')
        recipe = Recipe.objects.create(**validated_data)

        self.write_to_intermediate_model(recipe, tags, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipeingredient')

        instance.tags.clear()
        instance.ingredients.clear()

        self.write_to_intermediate_model(instance, tags, ingredients)
        return super().update(instance, validated_data)

    @staticmethod
    def write_to_intermediate_model(recipe, tags, ingredients):
        recipe.tags.set(tags)
        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    amount=ingredient.get('amount'),
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(
                        pk=ingredient.get('ingredient').get('id').id
                    )
                ) for ingredient in ingredients
            ]
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов (краткий, чтение)."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(CustomUserSerializer):
    """Сериализатор для подписок."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.BooleanField(default=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = fields

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        request = self.context['request']
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
