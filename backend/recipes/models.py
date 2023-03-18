from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тега рецепта."""
    name = models.CharField(
        verbose_name='Tag name',
        max_length=200,
        unique=True,
    )
    colour = models.CharField(
        verbose_name='Colour',
        max_length=7,
        unique=True,
        default='#E26C2D',
        validators=(
            RegexValidator(
                r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                'Colour must be in HEX-format.'
            ),
        ),
    )
    slug = models.SlugField(
        verbose_name='Identifier',
        max_length=200,
        unique=True,
        validators=(
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                'Slug must be in r"^[-a-zA-Z0-9_]+$" format'
            ),
        ),
        db_index=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        verbose_name='Ingredient name',
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_measurement_unit_for_name',
            ),
        )

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        verbose_name='Recipe name',
        max_length=200,
        db_index=True
    )
    text = models.TextField(verbose_name='Recipe description')
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        verbose_name='Recipe image',
        upload_to='',
    )
    cooking_time = models.IntegerField(
        verbose_name='Cooking time',
        validators=(
            MinValueValidator(
                1,
                'Cooking time must not be less than 1 minute'
            ),
        ),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredients',
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes',
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name[:30]


class RecipeIngredient(models.Model):
    """Модель ингредиента с количеством (в привязке к рецепту)."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        related_name='recipeingredient',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        related_name='recipeingredient',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(verbose_name='Recipe ingredient amount')

    class Meta:
        verbose_name = 'Ingredient amount'

    def __str__(self):
        """Строковое представление объекта модели."""
        return (f'{self.ingredient.name[:30]}: {self.amount} '
                f'{self.ingredient.measurement_unit}')


class Favorites(models.Model):
    """Модель Избранного."""
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='User favorite recipe',
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Favorites'
        verbose_name_plural = 'Favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_favorites',
            ),
        )

    def __str__(self):
        """Строковое представление объекта модели."""
        return (
            f'{self.recipe.name} in {self.user.last_name} '
            f'{self.user.first_name}s favorites'
        )


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe in shopping cart',
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping cart'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_shopping_cart',
            ),
        )

    def __str__(self):
        """Строковое представление объекта модели."""
        return f'{self.recipe} in {self.user}s shopping cart'
