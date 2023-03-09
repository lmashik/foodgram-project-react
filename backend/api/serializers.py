import base64
from djoser.serializers import UserSerializer
from recipes.models import (
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag,
    Favorites,
    ShoppingCart,
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription, User
from rest_framework_recursive.fields import RecursiveField
from drf_extra_fields.fields import Base64ImageField


# class Base64DecoderField(serializers.Field):
#     """Кастомное поле сериализатора для картинок."""
#     def to_representation(self, value):
#         return value
#
#     def to_internal_value(self, data):
#         data = data.split(sep=',')[1]
#         try:
#             data = base64.b64decode(data)
#         except ValueError:
#             raise serializers.ValidationError('Для этого цвета нет имени')
#         # with open('../media/1' + 'DATE-' + '.png', 'wb') as file:
#         #     file.write(data)
#         return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'


# class IngredientAmountSerializer(serializers.ModelSerializer):
#     """Сериализатор для ингредиентов с указанием количества."""
#     class Meta:
#         model = IngredientAmount
#         fields = '__all__'


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""
    is_subscribed = serializers.SerializerMethodField(default=False)

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

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_subscribed = Subscription.objects.filter(
            author=obj,
            subscriber=request.user
        ).exists()
        return is_subscribed


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов с количеством."""
    class Meta:
        model = IngredientAmount
        fields = ('ingredient', 'amount',)


class ReadOnlyRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов (для чтения)."""
    # ingredients = IngredientAmountSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        ingredients = IngredientAmount.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_favorite = Favorites.objects.filter(
            recipes=obj, user=request.user
        ).exists()
        return is_favorite

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_in_shopping_cart = ShoppingCart.objects.filter(
            recipes=obj, user=request.user
        ).exists()
        return is_in_shopping_cart


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов (для записи)."""
    ingredients = IngredientAmountSerializer(
        # source='ingredients__set',
        many=True
    )
    # tags = TagSerializer(many=True)
    author = CustomUserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            IngredientAmount.objects.create(
                ingredient=current_ingredient,
                # recipe=recipe,
                amount=current_ingredient.amount,
            )
        return recipe


class SubscriptionSerializer(CustomUserSerializer):
    """Сериализатор для подписок."""
    author = CustomUserSerializer()
    # recipes = RecipeSerializer(source='recipes', many=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    # is_subscribed = serializers.SerializerMethodField()
    # subscriber = CustomUserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ('author', 'recipes', 'recipes_count',)
        # fields = (
        #     'pk',
        #     'username',
        #     'email',
        #     'first_name',
        #     'last_name',
        #     'is_subscribed',
        #     'recipes',
        #     'recipes_count',
        # )

        # extra_kwargs = {'subscriber': {'write_only': True}}

        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('author', 'subscriber'),
                message='Already have a subscription',
            ),
        )

    # def validate(self, attrs):
    #
    def validate_author(self, some_user):
        user = self.context.get('request').user
        if user == some_user:
            raise serializers.ValidationError(
                'Self subscription is not possible'
            )
        return some_user

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        # ingredients = IngredientAmount.objects.filter(recipe=obj)
        # return IngredientAmountSerializer(ingredients, many=True).data
        recipes = Recipe.objects.filter(author=obj.author)
        return ReadOnlyRecipeSerializer(recipes, many=True).data

    # def get_is_subscribed(self, obj):
    #     return self.is_subscribed
        # print(self)
        # # request = self.context['request']
        # return Subscription.objects.filter(
        #     author=obj,
        #     subscriber=self.instance.user
        # ).exists()

    # def to_representation(self):
    #     representation = super().to_representation(self)
