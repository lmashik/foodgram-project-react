from django.core.validators import RegexValidator
from django.db import models

from users.models import User

from recipes.validators import validate_time


class Tag(models.Model):
    """Модель тега рецепта."""
    name = models.CharField(
        verbose_name='Tag name',
        max_length=200,
        unique=True
    )
    colour = models.CharField(
        verbose_name='Colour',
        max_length=7,
        unique=True,
        default='#E26C2D',
        validators=(RegexValidator(r'^\#[0-9A-Fa-f]'),)
    )
    slug = models.SlugField(
        verbose_name='Identifier',
        max_length=200,
        unique=True,
        validators=(RegexValidator(r'^[-a-zA-Z0-9_]+$'),)
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(verbose_name='Ingredient name', max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=200
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(verbose_name='Recipe name', max_length=200)
    text = models.TextField(verbose_name='Recipe description')
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        on_delete=models.CASCADE
    )
    image = models.ImageField(verbose_name='Recipe image')
    cooking_time = models.IntegerField(
        verbose_name='Cooking time', validators=(validate_time,)
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredients',
        related_name='Recipes',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='Recipes',
    )

    def __str__(self):
        """Строковое представление объекта модели."""
        return self.name[:30]

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Recipe ingredient amount')

